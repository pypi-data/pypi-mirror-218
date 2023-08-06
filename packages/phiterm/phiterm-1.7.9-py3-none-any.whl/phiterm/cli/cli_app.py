"""The Phi Cli

This is the entrypoint for the `phi` cli application.
"""
from typing import Optional

import typer

from phiterm.cli.ws.ws_app import ws_app
from phiterm.cli.k8s.k8s_app import k8s_app
from phiterm.cli.wf.wf_app import wf_app
from phiterm.utils.log import set_log_level_to_debug

cli_app = typer.Typer(
    help="""\b
Phidata is a toolkit for building applications using open source tools.
\b
Get started:
1. Run `phi ws create` to create a new workspace
2. Run `phi ws up` to start the workspace
3. Run `phi ws down` to stop the workspace
""",
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=True,
    options_metavar="\b",
    subcommand_metavar="[command]",
    pretty_exceptions_show_locals=False,
)


@cli_app.command(short_help="Initialize phidata, use -r to reset")
def init(
    reset: bool = typer.Option(
        False, "--reset", "-r", help="Reset phidata", show_default=True
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    login: bool = typer.Option(
        False, "--login", "-l", help="Login using phidata.com", show_default=True
    ),
):
    """
    \b
    Initialize phidata, use -r to reset

    \b
    Examples:
    * `phi init`    -> Initializing phidata
    * `phi init -r` -> Reset and initializing phidata
    """
    from phiterm.cli.cli_operator import initialize_phidata

    if print_debug_log:
        set_log_level_to_debug()

    init_success: bool = initialize_phidata(reset=reset, login=login)


@cli_app.command(short_help="Authenticate with phidata.com")
def auth(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Authenticate your account with phidata.
    """
    from phiterm.cli.cli_operator import authenticate_user

    if print_debug_log:
        set_log_level_to_debug()

    auth_success: bool = authenticate_user()


@cli_app.command(short_help="Set current directory as active workspace")
def set(
    ws_name: str = typer.Option(None, "-ws", help="Active workspace name"),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Setup the current directory as the active workspace.
    This command can be run from within the workspace directory
        OR with a -ws flag to set another workspace as primary.

    Set a workspace as active

    \b
    Examples:
    $ `phi ws set`           -> Set the current directory as the active phidata workspace
    $ `phi ws set -ws idata` -> Set the workspace named idata as the active phidata workspace
    """
    from phiterm.workspace.ws_operator import set_workspace_as_active

    if print_debug_log:
        set_log_level_to_debug()

    operation_success: bool = set_workspace_as_active(ws_name)


@cli_app.command(short_help="Log in from the cli")
def login(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Log in from the cli

    \b
    Examples:
    * `phi login`
    """
    from phiterm.cli.cli_operator import sign_in_using_cli

    if print_debug_log:
        set_log_level_to_debug()

    auth_success: bool = sign_in_using_cli()


@cli_app.command(short_help="Reset phidata installation")
def reset(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Reset the existing phidata installation
    After resetting please run `phi init` to initialize again.
    """
    from phiterm.cli.cli_operator import initialize_phidata

    if print_debug_log:
        set_log_level_to_debug()

    init_success: bool = initialize_phidata(reset=True)


@cli_app.command(short_help="Ping phidata servers", hidden=True)
def ping(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """Ping the phidata servers and check if you are authenticated"""
    from phiterm.api.user import user_ping, is_user_authenticated
    from phiterm.utils.cli_console import print_info

    if print_debug_log:
        set_log_level_to_debug()

    ping_success = user_ping()
    if ping_success:
        print_info("Ping successful")
    else:
        print_info("Could not reach phidata servers")

    if is_user_authenticated():
        print_info("User is authenticated")
    else:
        print_info("User is not authenticated, run `phi auth` to log in")


@cli_app.command(short_help="Print phidata config", hidden=True)
def config(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    show_all: bool = typer.Option(
        False,
        "-a",
        "--all",
        help="Show all workspaces",
    ),
):
    """Print your current phidata config"""
    from phiterm.conf.phi_conf import PhiConf
    from phiterm.utils.cli_console import print_info

    if print_debug_log:
        set_log_level_to_debug()

    conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if conf is not None:
        conf.print_to_cli(show_all=show_all)
    else:
        print_info("Phidata has not been setup, run `phi init` to get started")


@cli_app.command(short_help="Start resources defined in a resources.py file")
def start(
    resources_file: str = typer.Argument(
        "resources.py",
        help="Path to workspace file.",
        show_default=False,
    ),
    env_filter: Optional[str] = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment to deploy"
    ),
    config_filter: Optional[str] = typer.Option(
        None, "-c", "--config", metavar="", help="Filter the config to deploy"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be deployed and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before deploying resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Start resources defined in a resources.py file
    \b
    Examples:
    > `phi ws start`                -> Start resources defined in a resources.py file
    > `phi ws start workspace.py`   -> Start resources defined in a workspace.py file
    """
    from pathlib import Path
    from phiterm.conf.phi_conf import PhiConf
    from phiterm.cli.cli_operator import start_resources
    from phiterm.utils.load_env import load_env
    from phiterm.utils.cli_console import print_error, print_conf_not_available_msg
    from phiterm.workspace.ws_enums import WorkspaceConfigType

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    # Load environment from .env
    load_env(
        env={
            "PHI_WS_FORCE": str(force),
        },
        dotenv_dir=Path(".").resolve(),
    )

    target_env: Optional[str] = None
    target_config_str: Optional[str] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None
    target_group: Optional[str] = None

    if env_filter is not None and isinstance(env_filter, str):
        target_env = env_filter
    if config_filter is not None and isinstance(config_filter, str):
        target_config_str = config_filter
    if name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if group_filter is not None and isinstance(group_filter, str):
        target_group = group_filter

    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = WorkspaceConfigType.from_str(target_config_str)

    resources_file_path: Path = Path(".").resolve().joinpath(resources_file)
    start_resources(
        resources_file_path=resources_file_path,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_group=target_group,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
    )


@cli_app.command(short_help="Stop resources defined in a resources.py file")
def stop(
    resources_file: str = typer.Argument(
        "resources.py",
        help="Path to workspace file.",
        show_default=False,
    ),
    env_filter: Optional[str] = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment to deploy"
    ),
    config_filter: Optional[str] = typer.Option(
        None, "-c", "--config", metavar="", help="Filter the config to deploy"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be deployed and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before deploying resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Start resources defined in a resources.py file
    \b
    Examples:
    > `phi ws start`                -> Start resources defined in a resources.py file
    > `phi ws start workspace.py`   -> Start resources defined in a workspace.py file
    """
    from pathlib import Path
    from phiterm.conf.phi_conf import PhiConf

    from phiterm.cli.cli_operator import stop_resources
    from phiterm.utils.load_env import load_env
    from phiterm.utils.cli_console import print_error, print_conf_not_available_msg
    from phiterm.workspace.ws_enums import WorkspaceConfigType

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    # Load environment from .env
    load_env(
        env={
            "PHI_WS_FORCE": str(force),
        },
        dotenv_dir=Path(".").resolve(),
    )

    target_env: Optional[str] = None
    target_config_str: Optional[str] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None
    target_group: Optional[str] = None

    if env_filter is not None and isinstance(env_filter, str):
        target_env = env_filter
    if config_filter is not None and isinstance(config_filter, str):
        target_config_str = config_filter
    if name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if group_filter is not None and isinstance(group_filter, str):
        target_group = group_filter

    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = WorkspaceConfigType.from_str(target_config_str)

    resources_file_path: Path = Path(".").resolve().joinpath(resources_file)
    stop_resources(
        resources_file_path=resources_file_path,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_group=target_group,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
    )


@cli_app.command(short_help="Update resources defined in a resources.py file")
def patch(
    resources_file: str = typer.Argument(
        "resources.py",
        help="Path to workspace file.",
        show_default=False,
    ),
    env_filter: Optional[str] = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment to deploy"
    ),
    config_filter: Optional[str] = typer.Option(
        None, "-c", "--config", metavar="", help="Filter the config to deploy"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be deployed and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before deploying resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Start resources defined in a resources.py file
    \b
    Examples:
    > `phi ws start`                -> Start resources defined in a resources.py file
    > `phi ws start workspace.py`   -> Start resources defined in a workspace.py file
    """
    from pathlib import Path
    from phiterm.conf.phi_conf import PhiConf

    from phiterm.cli.cli_operator import patch_resources
    from phiterm.utils.load_env import load_env
    from phiterm.utils.cli_console import print_error, print_conf_not_available_msg
    from phiterm.workspace.ws_enums import WorkspaceConfigType

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    # Load environment from .env
    load_env(
        env={
            "PHI_WS_FORCE": str(force),
        },
        dotenv_dir=Path(".").resolve(),
    )

    target_env: Optional[str] = None
    target_config_str: Optional[str] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None
    target_group: Optional[str] = None

    if env_filter is not None and isinstance(env_filter, str):
        target_env = env_filter
    if config_filter is not None and isinstance(config_filter, str):
        target_config_str = config_filter
    if name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if group_filter is not None and isinstance(group_filter, str):
        target_group = group_filter

    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = WorkspaceConfigType.from_str(target_config_str)

    resources_file_path: Path = Path(".").resolve().joinpath(resources_file)
    patch_resources(
        resources_file_path=resources_file_path,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_group=target_group,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
    )


@cli_app.command(short_help="Restart resources defined in a resources.py file")
def restart(
    resources_file: str = typer.Argument(
        "resources.py",
        help="Path to workspace file.",
        show_default=False,
    ),
    env_filter: Optional[str] = typer.Option(
        None, "-e", "--env", metavar="", help="Filter the environment to deploy"
    ),
    config_filter: Optional[str] = typer.Option(
        None, "-c", "--config", metavar="", help="Filter the config to deploy"
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    group_filter: Optional[str] = typer.Option(
        None, "-g", "--group", metavar="", help="Filter using group name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be deployed and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the confirmation before deploying resources.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
    force: bool = typer.Option(
        False,
        "-f",
        "--force",
        help="Force",
    ),
):
    """\b
    Restart resources defined in a resources.py file
    \b
    Examples:
    > `phi ws restart`                -> Start resources defined in a resources.py file
    > `phi ws restart workspace.py`   -> Start resources defined in a workspace.py file
    """
    from time import sleep
    from phiterm.utils.cli_console import print_info

    stop(
        resources_file=resources_file,
        env_filter=env_filter,
        config_filter=config_filter,
        name_filter=name_filter,
        type_filter=type_filter,
        group_filter=group_filter,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
        print_debug_log=print_debug_log,
        force=force,
    )
    print_info("Sleeping for 2 seconds..")
    sleep(2)
    start(
        resources_file=resources_file,
        env_filter=env_filter,
        config_filter=config_filter,
        name_filter=name_filter,
        type_filter=type_filter,
        group_filter=group_filter,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
        print_debug_log=print_debug_log,
        force=force,
    )


cli_app.add_typer(ws_app)
cli_app.add_typer(k8s_app)
cli_app.add_typer(wf_app)
