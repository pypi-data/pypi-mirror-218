import typer
from typing import Optional
from .api.ChipToolMgr import ChipToolMgr
from .api.ChipToolMgr import ChipToolLightMgr
from .api.ChipToolMgr import ChipToolSwitchMgr
from .api.ChipToolMgr import ChipToolConnectMgr
from .api.OTBRMgr import OTBRMgr
from .api.struct import OTBRData as CMDhelpper
from .extlib.MgmtExt.log import set_log_level, get_logger
from .extlib.MgmtExt.time import start_timmer, stop_timmer
from . import __app_name__, __version__

app = typer.Typer()


def check_log_level(flag):
    if flag == True:
        set_log_level("DEBUG")
    else:
        set_log_level("INFO")

### Thread Command ###


@app.command(name="state")
def get_state(
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Thread] Get Thread Network state."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    OTBRMgr().handle_command(CMDhelpper.QueryCMDMapper.STATE)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="dataset")
def get_dataset(
        hex: Optional[int] = typer.Option(
            0, "--hex", "-x",
            help="BLE adapter with HCI device [int]",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Thread] Get Thread active dataset."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    if (hex == 0):
        OTBRMgr().handle_command(CMDhelpper.QueryCMDMapper.DATA)
    else:
        OTBRMgr().handle_command(CMDhelpper.QueryCMDMapper.HEX)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


### Matter Command ###

@app.command(name="connect")
def connect(
        name: Optional[str] = typer.Argument(
            None, help="device alias",
        ),
        devicetype: Optional[str] = typer.Argument(
            None, help="device type",
        ),
        pincode: Optional[str] = typer.Argument(
            None, help="device pincode",
        ),
        discriminator: Optional[int] = typer.Argument(
            None, help="device long discriminator",
        ),
        ble_adapter: Optional[int] = typer.Option(
            0, "--ble-adapter", "-b",
            help="BLE adapter with HCI device [int]",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] Pair device with Thread."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolConnectMgr().connect(name, devicetype, pincode, discriminator, ble_adapter)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="disconnect")
def disconnect(
        name: Optional[str] = typer.Argument(
            None, help="device alias",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] Unpair device with Thread."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolConnectMgr().disconnect(name)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="reset")
def reset(
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] Reset matter-tool (Factory reset devices first)"""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolConnectMgr().reset()
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="group_gen")
def group_gen(
        group_name: Optional[str] = typer.Argument(
            None, help="Group name",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] Generate group."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolSwitchMgr().gen_group(group_name)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="group_del")
def group_del(
        group_name: Optional[str] = typer.Argument(
            None, help="Group name",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] Delete group."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolSwitchMgr().del_group(group_name)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="group_join")
def group_join(
        group_name: Optional[str] = typer.Argument(
            None, help="Group name",
        ),
        target_name: Optional[str] = typer.Argument(
            None, help="Connected target name",
        ),
        target_endpoint: Optional[int] = typer.Option(
            1, "--target-endpoint", "-l",
            help="target endpoint",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] join device to group."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolSwitchMgr().join_group(group_name, target_name, target_endpoint)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="group_leave")
def group_leave(
        group_name: Optional[str] = typer.Argument(
            None, help="Group name",
        ),
        target_name: Optional[str] = typer.Argument(
            None, help="Connected target name",
        ),
        target_endpoint: Optional[int] = typer.Option(
            1, "--target-endpoint", "-l",
            help="target endpoint",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] leave device to group."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolSwitchMgr().leave_group(
        group_name, target_name, target_endpoint)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="onoff")
def onoff(
        action: Optional[str] = typer.Argument(
            'on', help="control light: [on/off/toggle]",
        ),
        light_name: Optional[str] = typer.Argument(
            None, help="target light name",
        ),
        endpoint: Optional[int] = typer.Argument(
            1, help="target endpoint",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] Onoff control Matter Light."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolLightMgr().onoff(action, light_name, endpoint)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="group_onoff")
def group_onoff(
        action: Optional[str] = typer.Argument(
            'on', help="control light: [on/off/toggle]",
        ),
        group_name: Optional[str] = typer.Argument(
            None, help="target group name",
        ),
        endpoint: Optional[int] = typer.Argument(
            1, help="target endpoint",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] Group onoff control Matter Light."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolLightMgr().group_onoff(action, group_name, endpoint)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="level")
def level(
        level: Optional[int] = typer.Argument(
            0, help="target level",
        ),
        transition: Optional[int] = typer.Option(
            0, "--transition", "-t",
            help="transitiontime",
        ),
        light_name: Optional[str] = typer.Argument(
            None, help="target light name",
        ),
        endpoint: Optional[int] = typer.Argument(
            1, help="target endpoint",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] level control Matter Light."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolLightMgr().level(level, light_name, endpoint, transition)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="show")
def show(
        display: Optional[int] = typer.Option(
            0, "--level", "-l",
            help="""
            Matter Profile Level:\n
            level 0 (default): display node profile\n
            level 1: display Matter profile and Matter stack information\n
            """,
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] show matter profile"""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    if (display == 0):
        ChipToolMgr().list_node_profile()
        ChipToolMgr().list_binding_profile()
        ChipToolMgr().list_group_mapper_profile()
    elif (display == 1):
        ChipToolMgr().list_node_profile()
        ChipToolMgr().list_binding_profile()
        ChipToolMgr().list_group_mapper_profile()
        ChipToolMgr().list_acl_profile()
        ChipToolMgr().list_group_profile()
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


@app.command(name="bind")
def bind(
        light_name: Optional[str] = typer.Argument(
            None, help="Connected light name",
        ),
        light_endpoint: Optional[int] = typer.Option(
            1, "--light-endpoint", "-l",
            help="target light endpoint",
        ),
        switch_name: Optional[str] = typer.Argument(
            None, help="Connected switch name",
        ),
        switch_endpoint: Optional[int] = typer.Option(
            1, "--switch-endpoint", "-s",
            help="target switch endpoint",
        ),
        is_debug: bool = typer.Option(False, "--debug", "-d"),) -> None:
    """[Matter] Set binding between light and switch."""
    check_log_level(is_debug)
    _logger = get_logger("APP")
    start_timmer("CMD")
    ChipToolSwitchMgr().set_binding(
        light_name, light_endpoint, switch_name, switch_endpoint)
    _logger.info("Execute time: " + str(stop_timmer("CMD")))


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
