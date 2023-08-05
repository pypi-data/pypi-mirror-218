from enum import Enum


class CMDList(Enum):
    CONNECT_THEAD = ['chip-tool', 'pairing', 'ble-thread']
    DISCONNECT_THEAD = ['chip-tool', 'pairing', 'unpair']
    RESET_MATTER = ['sudo', 'rm', '/tmp/chip_*']
    SET_ACL = ['chip-tool', 'accesscontrol', 'write', 'acl']
    WRITE_BINDING = ['chip-tool', 'binding', 'write', 'binding']
    CREATE_GROUP = ['chip-tool', 'groupsettings', 'add-group']
    REMOVE_GROUP = ['chip-tool', 'groupsettings', 'remove-group']
    CREATE_KEYSET = ['chip-tool', 'groupsettings', 'add-keysets']
    REMOVE_KEYSET = ['chip-tool', 'groupsettings', 'remove-keyset']
    BIND_GROUP_KEYSET = ['chip-tool', 'groupsettings', 'bind-keyset']
    UNBIND_GROUP_KEYSET = ['chip-tool', 'groupsettings', 'unbind-keyset']
    APPLY_KEYSET = ['chip-tool', 'groupkeymanagement', 'key-set-write']
    DENIED_KEYSET = ['chip-tool', 'groupkeymanagement', 'key-set-remove']
    APPLY_KEYSET_MAP = ['chip-tool',
                        'groupkeymanagement', 'write', 'group-key-map']
    DENIED_KEYSET_MAP = ['chip-tool',
                         'groupkeymanagement', 'write', 'group-key-map']
    APPLY_GROUP = ['chip-tool', 'groups', 'add-group']
    DENIED_GROUP = ['chip-tool', 'groups', 'remove-group']
    LIGHT_ONOFF = ['chip-tool', 'onoff']
    LIGHT_GROUP_ONOFF = ['chip-tool', 'onoff', '0xffffffffffff']
    LEVEL_CTL = ['chip-tool', 'levelcontrol', 'move-to-level-with-on-off']
    CHECK_COMMAND_SUCCESS = 'echo $?'


class QueryCMDMapper(Enum):
    CONN_THREAD = CMDList.CONNECT_THEAD.name
    DISCONN_THREAD = CMDList.DISCONNECT_THEAD.name
    RESET_MATTER = CMDList.RESET_MATTER.name
    ACCESS_CONTROL = CMDList.SET_ACL.name
    SET_BINDING = CMDList.WRITE_BINDING.name
    CREATE_GROUP = CMDList.CREATE_GROUP.name
    REMOVE_GROUP = CMDList.REMOVE_GROUP.name
    CREATE_KEYSET = CMDList.CREATE_KEYSET.name
    REMOVE_KEYSET = CMDList.REMOVE_KEYSET.name
    BIND_GROUP_KEYSET = CMDList.BIND_GROUP_KEYSET.name
    UNBIND_GROUP_KEYSET = CMDList.UNBIND_GROUP_KEYSET.name
    APPLY_KEYSET = CMDList.APPLY_KEYSET.name
    DENIED_KEYSET = CMDList.DENIED_KEYSET.name
    APPLY_KEYSET_MAP = CMDList.APPLY_KEYSET_MAP.name
    DENIED_KEYSET_MAP = CMDList.DENIED_KEYSET_MAP.name
    LIGHT_ONOFF = CMDList.LIGHT_ONOFF.name
    LIGHT_GROUP_ONOFF = CMDList.LIGHT_GROUP_ONOFF.name
    LEVEL_CONTROL = CMDList.LEVEL_CTL.name
    APPLY_GROUP = CMDList.APPLY_GROUP.name
    DENIED_GROUP = CMDList.DENIED_GROUP.name
    CHECK_STATE = CMDList.CHECK_COMMAND_SUCCESS.name


def check_query_exists(query: str):
    return True if any(x for x in QueryCMDMapper if x.name == query) else False


def check_command_exists(query: str):
    return True if any(x for x in CMDList if x.name == query) else False


def get_query_prefix(query: str):
    return CMDList[QueryCMDMapper[query].value].value
