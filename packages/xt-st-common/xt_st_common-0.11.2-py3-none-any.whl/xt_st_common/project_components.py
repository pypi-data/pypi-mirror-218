import json
from io import BytesIO
from pathlib import Path
from random import randint
from typing import List, Literal, Optional, Tuple, Union  # , Optional

import pandas as pd
import streamlit as st

# from mpl_toolbox_ui.common.config import Settings
from xt_st_common.database import (
    Project,
    delete_project,
    get_project,
    get_project_cache,
    get_projects,
    project_duplicate_exists,
    save_project,
)
from xt_st_common.project_models import ProjectState
from xt_st_common.session import get_user_email
from xt_st_common.storage import FileRef, storage_client
from xt_st_common.utils import (
    get_encoding_and_dialect,
    get_state,
    seperate_users,
    set_state,
)

# from bson.objectid import ObjectId

# mapping for language options for streamlit code formatter. For other available options
# see: https://github.com/react-syntax-highlighter/react-syntax-highlighter/blob/master/AVAILABLE_LANGUAGES_PRISM.MD
CODE_FORMAT_MAPPING = {
    "json": "json",
    "yaml": "yaml",
    "yml": "yaml",
    "toml": "toml",
    "md": "markdown",
}

REPLACE_FILE_HELP_TXT = (
    "The new file can have a different name but must have the same extension."
    "Warning: Uploading a new file that is significantly different to the original "
    "can have catastrophic results."
)

FOLDER_SHARED_KEY = "project_folder_select"
PROJECT_SHARED_KEY = "project_select"


def has_project_write_access(project: Project):
    return project.owner.lower() == get_user_email().lower() or get_user_email().lower() in (
        user.lower() for user in project.users
    )


def state_reset():
    for s in ProjectState:
        if s in [ProjectState.PROJECT_TO_DELETE, ProjectState.FILE_TO_DELETE]:
            set_state(s, None)
        else:
            set_state(s, "")


def get_selected_project() -> Optional[Project]:
    project = get_state("selected_project", None)
    if project is None:
        return None
    if not isinstance(project, Project):
        raise ValueError("Selected project is not the correct type")
    return project


def get_selected_folder() -> str:
    return get_state("project_folder_select", "")


def get_selected_project_or_error() -> Project:
    project = get_selected_project()
    if project is None:
        raise ValueError("No project was selected")
    return project


def set_selected_project(project: Optional[Project]):
    if project is not None and not isinstance(project, Project):
        raise ValueError("Setting selected project to a type other than project")
    st.session_state.selected_project = project


def submit_delete_project(project: Project):
    """Callback function to set state in order to enable a delete on the next run."""
    # display a warning if the user entered an existing name

    if project is None:
        set_state(ProjectState.PROJECT_WARNING_MESSAGE, "No project is selected")
    elif project.owner.lower() != get_user_email().lower():
        set_state(
            ProjectState.PROJECT_WARNING_MESSAGE,
            f"Delete of project **{project.name}** failed: You are not the owner.",
        )
    else:
        set_state(
            ProjectState.PROJECT_DELETE_CONFIRM,
            (
                "Deleting will remove all files that are part of project: "
                + f"**'{project.name}'**. Are you sure you want to continue?"
            ),
        )
        set_state(ProjectState.PROJECT_TO_DELETE, project)


def action_delete(project: Project):
    if project.id is not None and project.owner.lower() == get_user_email().lower():
        delete_project(project.id)
    set_state(
        ProjectState.PROJECT_SUCCESS_MESSAGE,
        f"Project **'{project.name}'** deleted successfully",
    )


def submit_delete_folder(folder: str):
    """Callback function to set state in order to enable a delete on the next run."""
    # display a warning if the user entered an existing name
    project = st.session_state.selected_project
    if project is None:
        set_state(ProjectState.UPLOAD_WARNING_MESSAGE, "No project is selected")
    elif not has_project_write_access(project):
        set_state(
            ProjectState.UPLOAD_WARNING_MESSAGE,
            f"You don't have write access to project: {project.name}",
        )
        return
    elif folder is None:
        set_state(ProjectState.UPLOAD_WARNING_MESSAGE, "No folder is selected")
    else:
        set_state(
            ProjectState.UPLOAD_DELETE_CONFIRM,
            (
                "Deleting will remove all files that are part of this folder: "
                + f"**'{folder}'**. Are you sure you want to continue?"
            ),
        )
        set_state(ProjectState.FOLDER_TO_DELETE, folder)


def action_delete_folder(folder):
    project = get_selected_project_or_error()
    project.delete_folder(folder)
    save_project(project)

    set_state(ProjectState.FOLDER_ADDED, None)
    set_state(
        ProjectState.UPLOAD_SUCCESS_MESSAGE,
        f"Folders **'{folder}'** was deleted successfully",
    )


def submit_delete_file(file: FileRef):
    """Callback function to set state in order to enable a delete on the next run."""
    # display a warning if the user entered an existing name
    project = st.session_state.selected_project
    if project is None:
        set_state(ProjectState.FILE_WARNING_MESSAGE, "No project is selected")
    elif file is None:
        set_state(ProjectState.FILE_WARNING_MESSAGE, "No file is selected")
    elif not has_project_write_access(project):
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            f"You don't have write access to project: {project.name}",
        )
        return
    else:
        set_state(
            ProjectState.FILE_DELETE_CONFIRM,
            f"Are you sure you want to delete file **'{file.name}'**?",
        )
        set_state(ProjectState.FILE_TO_DELETE, file)


def action_delete_file(_file: FileRef):
    project = get_selected_project_or_error()
    project.delete_file(_file)
    save_project(project)
    set_state(ProjectState.FILE_SUCCESS_MESSAGE, f"File {_file.name} was deleted successfully")


def submit_add_project(project: Optional[Project] = None):
    """Callback function during adding a new project."""

    message_verb = "updated"
    container = st.session_state.message_box if "message_box" in st.session_state else st

    name = get_state("create_project_name")
    description = str(get_state("create_project_description"))
    users = get_state("create_project_users")
    is_public = bool(get_state("create_project_public", False))

    if not name:
        container.warning("No project name was provided")
        return

    users_list = seperate_users(users)
    if project is None:
        message_verb = "created"
        project = Project(
            name=name,
            owner=get_user_email(),
            description=description,
            users=users_list,
            public=is_public,
        )
        if project_duplicate_exists(project.name, project.owner, str(project.id)):
            st.session_state.proj_warning_message = f"A Project with the name: **'{name}'** already exists"
            return
    else:
        # Get latest DB copy of the project
        project = get_project(str(project.id), st.session_state.project_cache)
        if project is None:
            st.session_state.proj_warning_message = f"Cannot update project: **'{name}'** not found in database"
            return
        project.__dict__.update(
            {
                "name": name,
                "description": description,
                "users": users_list,
                "public": is_public,
            }
        )

    project = save_project(project)
    set_selected_project(project)

    set_state(
        ProjectState.PROJECT_SUCCESS_MESSAGE,
        f"Project **'{name}'** has been {message_verb}.",
    )
    return


def project_form(project: Optional[Project] = None):
    """A form that allows for creating an updating projects.

    Parameters
    ----------
    project : Optional[Project], optional
        _description_, by default None
    """
    is_proj = project is not None
    name_val = project.name if is_proj else ""
    desc_val = project.description if is_proj else ""
    users_val = project.get_users_string() if is_proj else ""
    public_val = project.public if is_proj else False

    if is_proj:
        st.button(
            f"Delete {name_val}",
            on_click=submit_delete_project,
            args=(project,),
        )

    with st.form("create_project", clear_on_submit=True):
        if project is not None:
            st.subheader(f"Edit {project.name}")
        else:
            st.subheader("Create Project")
        st.text_input("Project Name", key="create_project_name", value=name_val)
        st.text_area("Description", key="create_project_description", value=desc_val)
        st.checkbox("Make Public", key="create_project_public", value=public_val)
        st.text_input("Users (emails , seperated)", key="create_project_users", value=users_val)

        st.form_submit_button(
            label="Submit",
            help="Create/Edit a Project",
            on_click=submit_add_project,
            args=(project,),
        )


def add_folders():
    project = st.session_state.selected_project
    folders_string = st.session_state.add_project_folder_name

    if not folders_string:
        set_state(
            ProjectState.UPLOAD_WARNING_MESSAGE,
            "Cannot add new folders: Folder name was empty",
        )
        return

    if not has_project_write_access(project):
        set_state(
            ProjectState.UPLOAD_WARNING_MESSAGE,
            f"You don't have write access to project: {project.name}",
        )
        return

    count = project.add_folders(folders_string)
    save_project(project)
    set_state(
        ProjectState.UPLOAD_SUCCESS_MESSAGE,
        f"{count} folders were added to **'{project.name}'**",
    )


def move_file(selected_file: FileRef, new_path: str):
    project: Project = st.session_state["selected_project"]

    if not new_path:
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            "Cannot move file. New path was empty",
        )
        return

    if selected_file.path == new_path:
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            "Cannot move file. New path is the same as the existing path",
        )
        return

    if not has_project_write_access(project):
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            f"You don't have write access to project: {project.name}",
        )
        return

    project.move_file_to_path(selected_file, new_path)

    save_project(project)

    set_state(
        ProjectState.FILE_SUCCESS_MESSAGE,
        f"File **'{selected_file.name}'** was succesfully moved to **'{new_path.split('/', 1)[1]}'**",
    )


def move_folder(selected_folder: str, new_folder_name: str):
    project: Project = st.session_state["selected_project"]

    if "/" in selected_folder:
        leaf_folder = selected_folder.split("/")[-1]
        folder_root = selected_folder.split(f"/{leaf_folder}")[0]
        full_new_folder_name = "/".join([folder_root, new_folder_name])
    else:
        leaf_folder = selected_folder
        folder_root = ""
        full_new_folder_name = "/".join([new_folder_name])

    if "/" in new_folder_name:
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            "Cannot rename folder. New name must not contain slash (/) characters",
        )
        return

    if not new_folder_name:
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            "Cannot rename folder. New name was empty",
        )
        return

    if leaf_folder == new_folder_name:
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            "Cannot rename folder. New name is the same as the existing name",
        )
        return

    if not has_project_write_access(project):
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            f"You don't have write access to project: {project.name}",
        )
        return

    project.rename_folder(selected_folder, full_new_folder_name)

    save_project(project)

    set_state(
        ProjectState.FILE_SUCCESS_MESSAGE,
        f"Folder **'{leaf_folder}'** was succesfully renamed to **'{new_folder_name}'**",
    )


def copy_file_to_project(selected_file: FileRef, new_project: Project):
    current_project: Project = st.session_state["selected_project"]

    if not has_project_write_access(new_project):
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            f"You don't have write access to project: {new_project.name}",
        )
        return

    if current_project.name in selected_file.get_prefix():
        new_path = f"{selected_file.get_prefix().replace(current_project.name, new_project.name).replace(str(current_project.id), str(new_project.id))}{selected_file.get_suffix()}"  # noqa: E501
    else:
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            "Cannot copy file. File does not exist in current project",
        )
        return

    if selected_file.path == new_path:
        set_state(
            ProjectState.FILE_WARNING_MESSAGE,
            "Cannot copy file. New path is the same as the current path.",
        )
        return

    new_file_ref = new_project.copy_file_to_path(selected_file, new_path)

    # if there are user folders included with the new path, add them to the project as well
    new_folder_message = ""
    folders_string = new_file_ref.get_user_folders()
    if folders_string != "":
        new_folder_count = new_project.add_folders(folders_string)
        if new_folder_count > 0:
            new_folder_message = f"**{new_folder_count}** folders were added."

    save_project(new_project)

    set_state(
        ProjectState.FILE_SUCCESS_MESSAGE,
        f"File **'{selected_file.name}'** was succesfully copied to **'{new_project.name}'**. " + new_folder_message,
    )


@st.cache_data(ttl=300)
def get_df_preview(path: str, ext: Optional[str], num_rows=25):
    # if filepath.suffix == ".zip":
    #     frame = get_gdf_from_file(filepath)
    #     return frame.iloc[:num_rows, :-1]
    _ext = ext.strip(".").lower() if ext else None
    if _ext == "csv":
        file = storage_client().get_file(path)
        encoding, dialect = get_encoding_and_dialect(file)
        return pd.read_csv(file, nrows=num_rows, sep=dialect.delimiter, encoding=encoding)
    if _ext == "feather":
        file = storage_client().get_file(path)
        return pd.read_feather(file)
    if _ext == "xlsx":
        file = storage_client().get_file(path)
        return pd.read_excel(file, sheet_name=0, nrows=num_rows)

    return None


def get_string_preview(fileref: FileRef):
    file = storage_client().get_file(fileref.path)
    return file.getvalue().decode("utf-8")


def _state_name(project_id: str, folder: str) -> str:
    return f"{project_id}-{folder}_fs"


@st.cache_data(ttl=15)
def get_proj_options(
    include_public: bool = False,
    other_apps: bool = True,
    shared_project: bool = True,
    selected_in_options: bool = True,
    cache_id=None,
):
    selected_project = get_selected_project()
    projects = get_projects(include_public, other_apps, shared_project, get_project_cache())
    sel_idx = 0
    options = {}
    for idx, proj in enumerate(projects):
        if selected_project and proj.id == selected_project.id:
            if selected_in_options:
                sel_idx = idx
            else:
                # when selected_in_options is false, skip the rest of this iteration
                continue

        option_str = f"{proj.name} ({proj.application}){'- 📢Public' if proj.public else ''}"
        if not proj.public and proj.owner.lower() != get_user_email().lower():
            option_str += " - 🤝Shared"
        options[idx] = option_str
    return options, projects, sel_idx


def on_project_select():
    proj_idx = get_state("project_select")
    include_public = bool(get_state("include_public_projects", False))
    include_other_apps = bool(get_state("include_other_apps", False))
    options, projects, _ = get_proj_options(include_public, include_other_apps, cache_id=get_project_cache())

    if proj_idx is not None and proj_idx > -1:
        selected_project = projects[proj_idx] if proj_idx != -1 else None
        set_selected_project(selected_project)
    else:
        set_selected_project(None)


def project_filters():
    with st.expander("Project Filters"):
        st.checkbox("Public projects", value=False, key="include_public_projects")
        st.checkbox("Other Apps", value=True, key="include_other_apps")
        st.checkbox("Shared projects", value=True, key="include_shared_projects")


def project_selector(
    select_box_label="Select Project",
    select_box_help=None,
    null_option="-- Select Project --",
    st_context=st.sidebar,
    on_select_change=None,
    enable_filters=True,
    set_selected=True,
    selected_in_options=True,
    prefix="",
    render_layout: Literal["vertical", "horizontal", "compact"] = "vertical",
) -> Tuple[Union["Project", None], List["Project"]]:
    """UI to select and create projects."""
    selected_project = None

    if render_layout == "horizontal":
        layout_container1, layout_container2 = st_context.columns(2)
        layout_container2.markdown("#")
    else:
        layout_container1 = st_context.container()
        layout_container2 = st_context.container()

    include_public = bool(get_state("include_public_projects", False))
    include_other_apps = bool(get_state("include_other_apps", False))
    include_shared_projects = bool(get_state("include_shared_projects", False))

    if enable_filters:
        with layout_container2:
            project_filters()
    options, projects, sel_idx = get_proj_options(
        include_public,
        include_other_apps,
        include_shared_projects,
        selected_in_options=selected_in_options,
        cache_id=get_project_cache(),
    )
    proj_options = {}

    # accomodate the null option if one is provided
    if null_option is not None:
        proj_options = {-1: null_option}
        sel_idx = sel_idx + 1

    if options is not None:
        proj_options = {**proj_options, **options}

    if len(proj_options) > 0:
        proj_idx = layout_container1.selectbox(
            select_box_label,
            help=select_box_help,
            key=f"{prefix}{PROJECT_SHARED_KEY}",
            index=sel_idx,
            on_change=on_select_change,
            options=proj_options.keys(),
            format_func=lambda x: proj_options[x],
        )

        selected_project = None
        if proj_idx is not None:
            selected_project = projects[proj_idx] if proj_idx != -1 else None
            if set_selected:
                set_selected_project(selected_project)

    else:
        st_context.warning("No projects were found")

    return selected_project, projects


def load_csv(
    data_file,
    st_context=st,
):
    """Takes a csv file and loads it into session_state."""

    try:
        encoding, dialect = get_encoding_and_dialect(data_file)
        raw_df = pd.read_csv(
            data_file,
            header=None,
            skip_blank_lines=True,
            engine="python",
            sep=None,
            encoding=encoding,
        )
    except Exception as err:
        raise ValueError("Could not parse txt/csv file.") from err

    c1, c2 = st.columns([1, 3])
    c1.header("CSV Data Import")
    c2.subheader("Import Preview (15 Rows)")
    if len(raw_df.columns) < 5:
        c2.info(
            "If preview has not loaded rows/columns correctly it may mean the wrong separator has been "
            + "detected. If that is the case than please check your file and remove unnecessary "
            + "header information."
        )
    c2.write(raw_df.head(15))

    with c1.form("config_df"):
        row_options: List[Union[str, int]] = list(range(16))
        row_options_wnone = row_options.copy()
        row_options_wnone.insert(0, "None")
        header_row = st_context.selectbox(label="Column Names Row", options=row_options)
        units_row = st_context.selectbox(label="Units Row", options=row_options_wnone)
        skip_rows = st_context.multiselect(label="Skip Rows", options=list(range(9)))

        if st.form_submit_button("Save Data"):
            return parse_csv_data(raw_df, header_row, units_row, skip_rows)
    return None, None


def parse_csv_data(raw_df: pd.DataFrame, header_row, units_row, skip_rows: Optional[List[int]] = None):
    units = {}
    if skip_rows is None:
        skip_rows = []

    raw_df.columns = raw_df.iloc[header_row]

    if units_row is not None and units_row != "None":
        units = raw_df.iloc[units_row].to_dict()
        if units_row != header_row and units_row not in skip_rows:
            raw_df = raw_df.drop(labels=units_row)

    if header_row not in skip_rows:
        raw_df = raw_df.drop(labels=header_row)

    raw_df = raw_df.drop(labels=skip_rows)
    raw_df = raw_df.reset_index(drop=True)

    return raw_df, units


def _update_key(prefix: str = "", replace: bool = False):
    """Hack to clear file upload after save by updating the key."""
    value = prefix + str(randint(1000, 100000000))
    set_state(f"{prefix}file_manager_key{'_replace' if replace else ''}", value)
    return str(value)


def _get_key(prefix: str = "", replace: bool = False):
    """Hack to clear file upload after save by updating the key."""
    key = get_state(f"{prefix}file_manager_key{'_replace' if replace else ''}", None)
    return _update_key(prefix, replace) if key is None else key


def file_manager(
    project: Project,
    types: List[str],
    st_context=st.sidebar,
    upload_label: str = "Upload file(s) to selected folder",
    help_text: Optional[str] = None,
    allow_upload=True,
    allow_multiple_uploads=False,
    allow_delete=True,
    allow_replace=True,
    allow_file_rename=False,
    allow_file_move=False,
    allow_file_copy_to_project=False,
    allow_folder_add=False,
    allow_folder_rename=False,
    key_prefix: str = "",
    allow_file_select=True,
    expand_file_actions=True,
    expand_folder_actions=True,
    folder_select_text="Select Borehole/Run",
    auto_parse_csv: Optional[bool] = None,
    render_layout: Literal["vertical", "horizontal", "compact"] = "vertical",
):
    file_delete_confirm = get_state(ProjectState.FILE_DELETE_CONFIRM)
    file_to_delete = get_state(ProjectState.FILE_TO_DELETE)
    file_success_message = get_state(ProjectState.FILE_SUCCESS_MESSAGE)
    file_warning_message = get_state(ProjectState.FILE_WARNING_MESSAGE)

    folder_to_delete = get_state(ProjectState.FOLDER_TO_DELETE)
    folder_delete_confirm = get_state(ProjectState.UPLOAD_DELETE_CONFIRM)
    folder_success_message = get_state(ProjectState.UPLOAD_SUCCESS_MESSAGE)
    folder_warning_message = get_state(ProjectState.UPLOAD_WARNING_MESSAGE)

    st_context.subheader(f"Files: {project.name}")
    if file_delete_confirm and file_to_delete:
        st.warning(file_delete_confirm)
        st.button("I'm Sure", on_click=action_delete_file, args=(file_to_delete,))

    if file_success_message:
        st.success(file_success_message)
    if file_warning_message:
        st.warning(file_warning_message)

    if folder_delete_confirm and folder_to_delete:
        st.warning(folder_delete_confirm)
        st.button("I'm Sure", on_click=action_delete_folder, args=(folder_to_delete,))

    if folder_success_message:
        st.success(folder_success_message)
    if folder_warning_message:
        st.warning(folder_warning_message)

    if render_layout == "horizontal":
        layout_container1, layout_container2 = st_context.columns(2)
    else:
        layout_container1 = st_context.container()
        layout_container2 = st_context.container()

    folders_dict = project.get_folders_map()
    folder = layout_container1.selectbox(
        folder_select_text,
        key=FOLDER_SHARED_KEY,
        options=folders_dict.keys(),
        format_func=lambda x: folders_dict[x],
    )
    path = project.get_folder_path(folder) if folder is not None else None
    if path is not None and folder is not None:
        row = layout_container1.expander("Folder Actions", expanded=expand_folder_actions)

        state = _state_name(str(project.id), folder)
        if state not in st.session_state:
            st.session_state[state] = 0

        if allow_upload and has_project_write_access(project):
            if auto_parse_csv is not None:
                try_parse_csv = row.checkbox(
                    "Parse CSV/TXT as Dataset",
                    value=auto_parse_csv,
                    help=(
                        "If a CSV or TXT file is uploaded you will be given options to help "
                        + "calibrate it for use as a dataset."
                    ),
                )
            else:
                try_parse_csv = False
            uploaded_files = row.file_uploader(
                upload_label,
                key=_get_key(key_prefix),
                type=types,
                help=help_text,
                accept_multiple_files=allow_multiple_uploads,
            )

            # handle cases where allow_multiple_uploads is false
            if uploaded_files is None:
                uploaded_files = []
            elif not isinstance(uploaded_files, list):
                uploaded_files = [uploaded_files]

            upload_messages = []
            for uploaded_file in uploaded_files:
                file_ref = None
                file_ref_units = None
                if (
                    uploaded_file
                    and try_parse_csv
                    and (uploaded_file.name.lower().endswith(".csv") or uploaded_file.name.lower().endswith(".txt"))
                ):
                    frame = None
                    try:
                        frame, units = load_csv(uploaded_file, st)
                    except ValueError:
                        st.warning(
                            "Could not parse CSV/TXT as a dataset. "
                            + "This may mean the file requires special parsing (such as a PWAVE file)"
                        )
                        try_parse_csv = not st.button("Upload anyway")
                        units = None

                    if frame is not None:
                        data_name = f"{Path(uploaded_file.name).stem}.feather"
                        with BytesIO() as buffer:
                            frame.to_feather(buffer)
                            buffer.seek(0)
                            file_ref = project.add_replace_file(
                                buffer,
                                folder=folder,
                                filename=data_name,
                            )
                        units_name = ""
                        if units:
                            units_name = f"{Path(uploaded_file.name).stem}_units.json"
                            units_string = json.dumps(units)
                            file_ref_units = project.add_replace_file(
                                units_string,
                                folder=folder,
                                filename=units_name,
                                content_type="application/json",
                            )

                elif uploaded_file:
                    file_ref = project.add_replace_file(
                        uploaded_file.getvalue(),
                        folder=folder,
                        filename=uploaded_file.name,
                    )

                if uploaded_file and file_ref:
                    uploaded_file.close()
                    upload_messages.append(
                        f"File: **'{file_ref.name}'** {' and ' + file_ref_units.name if file_ref_units else ''} "
                        + f" uploaded successfully to folder **'{file_ref.get_folder()}'**",
                    )

            if len(upload_messages) > 0:
                save_project(project)
                _update_key(key_prefix)
                set_state(
                    ProjectState.FILE_SUCCESS_MESSAGE,
                    "".join([f"> 1. {msg} \n" for msg in upload_messages]),
                )
                st.experimental_rerun()

        if render_layout == "compact":
            folder_add_sub_text_container = row.container()
            folder_add_sub_button_container = row.container()
            folder_delete_container = row.container()
            if allow_folder_rename:
                folder_rename_text_container = row.container()
                folder_rename_button_container = row.container()
        else:
            (
                folder_add_sub_text_container,
                folder_add_sub_button_container,
                folder_delete_container,
            ) = row.columns([3, 1, 1])
            folder_add_sub_button_container.markdown("#")
            folder_delete_container.markdown("#")
            if allow_folder_rename:
                (
                    folder_rename_text_container,
                    folder_rename_button_container,
                    _,
                ) = row.columns([3, 1, 1])
                folder_rename_button_container.markdown("#")

        if allow_folder_add:
            folder_add_sub_text_container.text_input(
                "Add sub folders (use ',' to separate multiple folders and '/' to separate levels) ",
                key="add_project_folder_name",
                help="All folders are created relative to the project root. "
                + "Create multiple folders at once by using ',' as a separator, folders can be "
                + "multiple levels deep using '/' e.g. folder1/subfolder1, folder1/subfolder22",
                placeholder="folder1/subfolder1, folder1/subfolder2",
            )
            folder_add_sub_button_container.button(
                label="Add Folders",
                help="Create new folder(s)",
                on_click=add_folders,
            )
        if allow_folder_rename and folder != "":
            folder_rename_string = folder_rename_text_container.text_input(
                "Rename folder as:",
                key="rename_project_folder_name",
                help=(
                    "Selected folder will be renamed to this value when 'Rename Selected' is clicked. "
                    + "New name will be applied to the 'leaf' folder and can not contain slashes"
                ),
                placeholder="New folder name",
            )
            if len(folder_rename_string) > 0:
                folder_rename_button_container.button(
                    label="Rename Selected",
                    help="Rename Folder",
                    on_click=move_folder,
                    args=(
                        folder,
                        folder_rename_string,
                    ),
                )

        if allow_delete and folder != "/":
            folder_delete_container.button(
                "Delete Selected",
                key=f"{key_prefix}folder_delete_btn",
                on_click=submit_delete_folder,
                args=(folder,),
            )
        if allow_file_select:
            files = project.get_files_in_folder(folder, include_subfolders=False)
            if files is not None and len(files) > 0:
                selected_key = layout_container2.selectbox(
                    "Select File",
                    options=files.keys(),
                    key=f"{key_prefix}file_manager_file_select",
                )
                selected_file = files[selected_key] if selected_key in files else None
                if selected_file is not None and selected_key is not None:
                    row = layout_container2.expander("File Actions", expanded=expand_file_actions)
                    if len(selected_key) > 30:
                        row.caption(selected_key)

                    if render_layout == "compact":
                        file_preview_container = row.container()
                        file_prepare_container, file_download_container = row.columns([5, 3])
                        file_download_container = row.container()
                        file_rename_button_container = row.container()
                        file_delete_container = row.container()
                        if allow_file_copy_to_project:
                            file_copy_to_project_select_container = row.container()
                            file_copy_to_project_button_container = row.container()
                        if allow_file_move:
                            file_move_select_container = row.container()
                            file_move_button_container = row.container()

                    else:
                        (
                            file_preview_container,
                            file_prepare_container,
                            file_download_container,
                        ) = row.columns([1, 1, 1])
                        (
                            file_rename_text_container,
                            file_rename_button_container,
                            file_delete_container,
                        ) = row.columns([2, 1, 1])
                        file_rename_button_container.markdown("#")
                        file_delete_container.markdown("#")

                        if allow_file_copy_to_project:
                            (
                                file_copy_to_project_select_container,
                                file_copy_to_project_button_container,
                                _,
                            ) = row.columns([2, 1, 1])
                            file_copy_to_project_button_container.markdown("#")

                        if allow_file_move:
                            (
                                file_move_select_container,
                                file_move_button_container,
                                _,
                            ) = row.columns([2, 1, 1])
                            file_move_button_container.markdown("#")

                    # options = []
                    if allow_delete:
                        file_delete_container.button(
                            "Delete Selected",
                            key=f"{key_prefix}file_delete_btn",
                            on_click=submit_delete_file,
                            args=(selected_file,),
                        )
                    if selected_key.lower().endswith((".zip", ".csv", ".geojson", ".gpkg", ".feather", ".xlsx")):
                        preview_frame = file_preview_container.button(
                            "Preview Frame",
                            key=f"{key_prefix}file_manager_preview_frame",
                        )
                        if preview_frame:
                            with st.expander(f"**Frame Viewer:** {selected_file.name}", expanded=True):
                                st.dataframe(get_df_preview(selected_file.path, selected_file.get_ext()))
                    if selected_key.lower().endswith((".json", ".yml", ".yaml", ".toml", ".md", ".txt")) and (
                        preview_frame := file_preview_container.button(
                            "Preview File",
                            key=f"{key_prefix}file_manager_preview_file",
                        )
                    ):
                        with st.expander(f"**File Viewer:** {selected_file.name}", expanded=True):
                            code_format = CODE_FORMAT_MAPPING.get(selected_key.lower().split(".")[-1])
                            if code_format is None:
                                st.write(get_string_preview(selected_file))
                            else:
                                st.code(
                                    get_string_preview(selected_file),
                                    language=code_format,
                                )
                    if file_prepare_container.checkbox(
                        "Prepare Download",
                        key=f"{key_prefix}file_manager_download_chbx",
                    ):
                        file_data = storage_client().get_file(selected_file.path)

                        file_download_container.download_button(
                            "Download",
                            file_data,
                            selected_file.name,
                            key=f"{key_prefix}file_manager_download_button",
                        )
                    if allow_replace and (
                        uploaded_replace_file := row.file_uploader(
                            "Replace the selected file",
                            key=_get_key(key_prefix, True),
                            type=selected_file.get_ext(),
                            help=REPLACE_FILE_HELP_TXT,
                            accept_multiple_files=False,
                        )
                    ):
                        project.add_replace_file_by_path(uploaded_replace_file, selected_file.path)
                        save_project(project)
                        uploaded_replace_file.close()
                        _update_key(key_prefix, True)
                        set_state(
                            ProjectState.FILE_SUCCESS_MESSAGE,
                            f"Contents of file: **'{selected_file.path}'** was succesfully replaced",
                        )
                        st.experimental_rerun()
                    if allow_file_rename:
                        rename_string = file_rename_text_container.text_input(
                            "Rename file as:",
                            key="rename_project_file_name",
                            help="Selected file will be renamed to this value when 'Rename Selected' is clicked",
                            placeholder="New file name",
                        )
                        if len(rename_string) > 0:
                            file_rename_button_container.button(
                                label="Rename Selected",
                                help="Rename File",
                                on_click=move_file,
                                args=(
                                    selected_file,
                                    f"{selected_file.get_prefix()}/{rename_string}",
                                ),
                            )
                    if allow_file_copy_to_project:
                        copy_to_selected_project, projects = project_selector(
                            select_box_label="Copy file to project:",
                            select_box_help="Selected file will be copied to this project "
                            + "when 'Copy to project' button is clicked",
                            st_context=file_copy_to_project_select_container,  # type: ignore
                            null_option=None,
                            enable_filters=False,
                            set_selected=False,
                            selected_in_options=False,
                            prefix="copy_to_project",
                        )

                        file_copy_to_project_button_container.button(
                            label="Copy to project",
                            help="Copy the selected file to the selected project. "
                            + "Folder structure of the selected file will be replicated in the new project",
                            on_click=copy_file_to_project,
                            args=(selected_file, copy_to_selected_project),
                        )

                    if allow_file_move:
                        file_move_to_folder = file_move_select_container.selectbox(
                            "Move to folder:",
                            key="move_folder_select",
                            options=folders_dict.keys(),
                            format_func=lambda x: folders_dict[x],
                        )

                        file_move_button_container.button(
                            label="Move to Folder",
                            help="Move the selected file to the selected project folder",
                            on_click=move_file,
                            args=(
                                selected_file,
                                "/".join([selected_file.get_root(), file_move_to_folder, selected_file.name,]).replace(
                                    "//", "/"
                                ),  # replace double slashes that occur when file_move_to_folder is project-root
                            ),
                        )

            else:
                layout_container2.markdown("##")
                layout_container2.info("No files in selected folder")

        state_reset()
    return path, folder


@st.cache_data(ttl=300)
def get_file_cached(file_path: str):
    return storage_client().get_file(file_path)


def file_selector(
    project: Project,
    folder: Optional[str] = "",
    select_folder_label: str = "Select Folder",
    select_file_label: str = "Select File",
    extensions: Optional[List[str]] = None,
    state_key: Optional[str] = None,
    prefix: str = "",
    no_file_warning: str = "No files were found with the correct extension.",
    null_option: Optional[str] = None,
):
    """
    Widget to Select and load a file from a selected project.

    Parameters
    ----------
    project : Project
        _description_
    folder : Optional[str], optional
        _description_, by default "/"
    select_folder_label : str, optional
        _description_, by default "Select Folder"
    select_file_label : str, optional
        _description_, by default "Select File"
    extensions : Optional[List[str]], optional
        _description_, by default None
    state_key : Optional[str], optional
        _description_, by default None
    no_file_warning : str, optional
        _description_, by default "No files were found with the correct extension."

    Returns
    -------
    _type_
        _description_
    """
    if folder is None:
        folders_dict = project.get_folders_map()
        folder = st.selectbox(
            select_folder_label,
            key=FOLDER_SHARED_KEY,
            options=folders_dict.keys(),
            format_func=lambda x: folders_dict[x],
        )

    files = project.get_files_in_folder(folder, extensions=extensions, include_subfolders=True, null_option=null_option)
    if files is not None and len(files) > 0:
        selected_key = st.selectbox(
            select_file_label,
            options=files.keys(),
        )
        if selected_key:
            file_ref = files.get(selected_key, None)

            if file_ref is not None and st.button(
                "Load Selected File", key=f"{state_key}_btn" if state_key else f"{prefix}load_btn_{file_ref.name}"
            ):
                file = get_file_cached(file_ref.path)
                if state_key:
                    set_state(state_key, file)
                    set_state(f"{state_key}_ref", file_ref)
                st.success(f"File {file_ref.name} loaded successfully.")
                return file, file_ref
            return None, file_ref
    else:
        st.warning(no_file_warning)
    return None, None


def get_projects_data(projects):
    selected_project = get_selected_project()
    proj_data = []
    for proj in projects:
        proj_dict = proj.dict(exclude={"files", "folders"})
        # proj_dict = proj.dict(exclude={"files", "folders", "id"})

        proj_dict["folders"] = f"{len(proj.folders) if proj.folders else 0} Folders"
        proj_dict["files"] = f"{len(proj.files) if proj.files else 0} Files"
        proj_dict["users"] = ", ".join(proj.users)
        proj_dict["select"] = proj.name == (selected_project.name if selected_project is not None else None)

        proj_data.append(proj_dict)
    return proj_data


def add_new_project(number=1, name_value: Optional[str] = None):
    user_email = get_user_email()
    if name_value is None:
        name_value = f"{user_email.split('@')[0]}_#{number}"
    project = Project(name=name_value, owner=get_user_email())

    project = save_project(project)
    set_selected_project(project)

    set_state(
        ProjectState.PROJECT_SUCCESS_MESSAGE,
        f"Project **'{name_value}'** has been initialised.",
    )

    st.experimental_rerun()


def get_next_project_number(projects: list[Project]):
    highest_number = len(projects) + 1
    for proj in projects:
        try:
            proj_number = proj.name.split("#")[1]
            proj_number = int(proj_number)
            if proj_number >= highest_number:
                highest_number = proj_number + 1
        except (ValueError, IndexError):
            pass
    return highest_number


def project_manager(
    st_context=st.sidebar,
    null_option=None,
    render_layout: Literal["vertical", "horizontal", "compact"] = "vertical",
    on_project_select_change=None,
):
    delete_confirm = get_state(ProjectState.PROJECT_DELETE_CONFIRM)
    project_to_delete = get_state(ProjectState.PROJECT_TO_DELETE, None)
    success_message = get_state(ProjectState.PROJECT_SUCCESS_MESSAGE)
    warning_message = get_state(ProjectState.PROJECT_WARNING_MESSAGE)
    get_state(ProjectState.UPLOAD_DELETE_CONFIRM)
    get_state(ProjectState.FOLDER_TO_DELETE)
    get_state(ProjectState.UPLOAD_SUCCESS_MESSAGE)
    get_state(ProjectState.UPLOAD_WARNING_MESSAGE)

    st_context.subheader("Manage Projects")

    if success_message:
        st.success(success_message)
    if warning_message:
        st.warning(warning_message)
    if delete_confirm and project_to_delete:
        st.warning(delete_confirm)
        st.button("I'm Sure", on_click=action_delete, args=(project_to_delete,))

    if render_layout == "horizontal":
        add_container, save_container, filter_container = st_context.columns([3, 1, 4])
        grid_container = st_context.container()
        select_container, delete_container, _ = st_context.columns([3, 1, 2])

        # # do some spacing that is particular to this layout
        delete_container.markdown("#")
    else:
        filter_container = st_context.container()
        grid_container = st_context.container()
        select_container = st_context.container()

        add_container = st_context.container()
        save_container, delete_container = st_context.columns([1, 1])

    with filter_container:
        project_filters()

    with select_container:
        project, projects = project_selector(
            null_option=null_option,
            select_box_label="Select Project",
            st_context=select_container,  # type: ignore
            on_select_change=on_project_select_change,
            enable_filters=False,
        )

        if len(projects) < 1:
            add_new_project()

    with grid_container:
        if render_layout == "compact":
            column_order = [
                "name",
                "description",
                "public",
                "owner",
                "users",
            ]

            set_col_width = "small"
        else:
            column_order = [
                # "select",
                # "id",
                "select",
                "name",
                "description",
                "application",
                "public",
                "owner",
                "users",
                "folders",
                "files",
            ]
            set_col_width = None  # columns will be sized to fit thier contents

        edited_project_data = st.data_editor(
            pd.DataFrame(get_projects_data(projects)),
            key="project_editor_key",
            use_container_width=True,
            hide_index=True,
            # num_rows="dynamic",
            column_order=column_order,
            column_config={
                "select": st.column_config.CheckboxColumn(
                    label="Selected",
                    help="Currently selected project",
                    width=None,
                    disabled=True,
                ),
                "name": st.column_config.TextColumn(label="Project Name", help="The name of the project", width=None),
                "description": st.column_config.Column(
                    label="Description",
                    help="General project description",
                    width=set_col_width,
                ),
                "application": st.column_config.Column(
                    label="Application",
                    help="The application that utilises this project",
                    disabled=True,
                    width=None,
                ),
                "owner": st.column_config.Column(
                    label="Owner",
                    help="The owner of the project",
                    disabled=True,
                    width=set_col_width,
                ),
                "public": st.column_config.CheckboxColumn(
                    label="Public",
                    help="Whether the project is available to all users",
                    width=None,
                ),
                "files": st.column_config.Column(
                    help="The list of files contained with the project",
                    disabled=True,
                    width=None,
                ),
                "folders": st.column_config.Column(
                    help="The list of folders contained with the project",
                    disabled=True,
                ),
                "users": st.column_config.Column(
                    label="Allowed Users (emails , separated)",
                    help="The list of users with access to the project",
                    disabled=False,
                    width=set_col_width,
                ),
            },
        )

        with add_container:
            name_col, btn_col = st.columns([3, 1])
            name_value = name_col.text_input(
                "Project Name",
                placeholder="Project_Name",
                help="Name to use for a new project",
                label_visibility="collapsed",
            )
            if btn_col.button("Add New"):
                if not name_value:
                    set_state(
                        ProjectState.PROJECT_WARNING_MESSAGE,
                        "**ADD PROJECT ERROR**: No project name value was entered for the new project.",
                    )
                    st.experimental_rerun()
                for proj in projects:
                    if proj.name.lower() == name_value.lower() and proj.owner.lower() == get_user_email().lower():
                        set_state(
                            ProjectState.PROJECT_WARNING_MESSAGE,
                            f"**ADD PROJECT ERROR**: Project with the name **{name_value}** already exists.",
                        )
                        st.experimental_rerun()

                new_proj_number = get_next_project_number(projects)
                add_new_project(new_proj_number, name_value)

        with delete_container:
            if st.button("Delete Selected"):
                submit_delete_project(project)
                st.experimental_rerun()

        with save_container:
            if st.button("Save Changes") and st.session_state.get("project_editor_key").get("edited_rows") is not None:
                update_messages = []
                project_table_data = st.session_state.get("project_editor_key")
                for changed_id in project_table_data["edited_rows"]:
                    # Get latest DB copy of the project
                    db_project = get_project(
                        str(edited_project_data["id"][changed_id]),
                        st.session_state.project_cache,
                    )
                    if db_project is None:
                        set_state(
                            ProjectState.PROJECT_WARNING_MESSAGE,
                            f"Cannot update project: **'{edited_project_data['name'][changed_id]}'** "
                            + " not found in database",
                        )
                    elif db_project.owner.lower() != get_user_email().lower():
                        set_state(
                            ProjectState.PROJECT_WARNING_MESSAGE,
                            f"Save changes on project **{db_project.name}** failed: You are not the owner.",
                        )
                    else:
                        original_name = db_project.name
                        db_project.__dict__.update(
                            {
                                "name": edited_project_data["name"][changed_id],
                                "description": edited_project_data["description"][changed_id],
                                "users": seperate_users(edited_project_data["users"][changed_id]),
                                "public": bool(edited_project_data["public"][changed_id]),
                            }
                        )
                        if project_duplicate_exists(db_project.name, db_project.owner, str(db_project.id)):
                            set_state(
                                ProjectState.PROJECT_WARNING_MESSAGE,
                                f"Cannot update project: A Project with the name: **'{db_project.name}'** "
                                + "already exists",
                            )
                        else:
                            if original_name != edited_project_data["name"][changed_id]:
                                db_project.rename_project(original_name, edited_project_data["name"][changed_id])
                            db_project = save_project(db_project)
                            update_messages.append(f"Project **'{db_project.name}'** updated successfully")

                if len(update_messages) > 1:
                    set_state(
                        ProjectState.PROJECT_SUCCESS_MESSAGE,
                        "".join([f"> 1. {msg} \n" for msg in update_messages]),
                    )
                else:
                    set_state(
                        ProjectState.PROJECT_SUCCESS_MESSAGE,
                        "".join([f"{msg}" for msg in update_messages]),
                    )
                st.experimental_rerun()

    return project, projects
