from enum import Enum


class CMDList(Enum):
    OT_DATA_HEX = ['sudo', 'ot-ctl', 'dataset', 'active', '-x']
    OT_DATA = ['sudo', 'ot-ctl', 'dataset', 'active']
    OT_STATE = ['sudo', 'ot-ctl', 'state']
    DISABLE_SRP = ['sudo', 'ot-ctl', 'srp', 'server', 'disable']
    ENABLE_SRP = ['sudo', 'ot-ctl', 'srp', 'server', 'enable']


class QueryCMDMapper(Enum):
    HEX = CMDList.OT_DATA_HEX.name
    DATA = CMDList.OT_DATA.name
    STATE = CMDList.OT_STATE.name
    DISABLE_SRP = CMDList.DISABLE_SRP.name
    ENABLE_SRP = CMDList.ENABLE_SRP.name


def check_query_exists(query: str):
    return True if any(x for x in QueryCMDMapper if x.name == query) else False


def check_command_exists(query: str):
    return True if any(x for x in CMDList if x.name == query) else False


def get_query_prefix(query: str):
    return CMDList[QueryCMDMapper[query].value].value
