from enum import Enum
import json
import re
import os
import glob
import dataclasses
import time
from prettytable import PrettyTable
from .OTBRMgr import OTBRMgr
from ..extlib.CMDAccess.CMDAccess import CMDAccess
from ..extlib.MgmtExt.log import get_logger
from ..extlib.MgmtExt.time import stop_timmer
from ..module.data.MatterDM import MatterDM
from ..module.data.Database import DatabaseHandler
from .struct import OTBRData as OTBRhelpper
from .struct import ChipToolData as ChipToolhelpper
from dataclasses import dataclass


class ChipToolMgr:
    def __init__(self) -> None:
        self._OTBRMgr = OTBRMgr()
        self._MatterDM = MatterDM()
        self._logger = get_logger("APP")

    def get_thread_network(self) -> None:
        return self._OTBRMgr.handle_command(OTBRhelpper.QueryCMDMapper.HEX)

    def list_node_profile(self):
        self._logger.info("=== [Matter Profile] Node ===")
        self.clear_failed_data()
        node_list = self._MatterDM.get_node_list()
        nodeid = []
        name = []
        devicetype = []
        status = []
        fabric = []
        for node in node_list["matter"]["node"]:
            nodeid.append(node["nodeid"])
            name.append(node["name"])
            devicetype.append(node["devicetype"])
            status.append(node["status"])
            fabric.append(node["fabric"])
        tab = PrettyTable()
        tab.add_column('nodeid', nodeid, align='r', valign='t')
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('devicetype', devicetype, align='r', valign='t')
        tab.add_column('status', status, align='r', valign='t')
        tab.add_column('fabric', fabric, align='r', valign='t')
        self._logger.info("\n"+str(tab))

    def list_binding_profile(self):
        self._logger.info("=== [Matter Profile] Binding List ===")
        self.clear_failed_data()
        binding_list = self._MatterDM.get_fully_binding_list()
        name = []
        fabric = []
        nodeid = []
        target_name = []
        target_id = []
        endpoint = []
        for binding in binding_list["matter"]["binding"]:
            name.append(binding["name"])
            fabric.append(binding["fabric"])
            nodeid.append(binding["nodeid"])
            target_name.append(binding["target_name"])
            target_id.append(binding["target_id"])
            endpoint.append(binding["endpoint"])
        tab = PrettyTable()
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('fabric', fabric, align='r', valign='t')
        tab.add_column('nodeid', nodeid, align='r', valign='t')
        tab.add_column('target_name', target_name, align='r', valign='t')
        tab.add_column('target_id', target_id, align='r', valign='t')
        tab.add_column('endpoint', endpoint, align='r', valign='t')
        self._logger.info("\n"+str(tab))

    def list_group_mapper_profile(self):
        self._logger.info("=== [Matter Profile] Group Mapper List ===")
        self.clear_failed_data()
        group_mapper_list = self._MatterDM.get_fully_group_mapper_list()
        name = []
        group_id = []
        target_id = []
        target_name = []
        target_type = []
        target_endpoint = []
        status = []
        for group_mapper in group_mapper_list["matter"]["group_mapper"]:
            name.append(group_mapper["name"])
            group_id.append(group_mapper["group_id"])
            target_id.append(group_mapper["target_id"])
            target_name.append(group_mapper["target_name"])
            target_type.append(group_mapper["target_type"])
            target_endpoint.append(group_mapper["target_endpoint"])
            status.append(group_mapper["status"])
        tab = PrettyTable()
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('group_id', group_id, align='r', valign='t')
        tab.add_column('target_id', target_id, align='r', valign='t')
        tab.add_column('target_name', target_name, align='r', valign='t')
        tab.add_column('target_type', target_type, align='r', valign='t')
        tab.add_column('target_endpoint', target_endpoint,
                       align='r', valign='t')
        tab.add_column('status', status, align='r', valign='t')
        self._logger.info("\n"+str(tab))

    def list_acl_profile(self):
        self._logger.info("=== [Matter Stack] Access Control List ===")
        self.clear_failed_data()
        acl_list = self._MatterDM.get_fully_acl_list()
        name = []
        fabric = []
        nodeid = []
        target_name = []

        target_id = []
        privilege = []
        auto_mode = []
        for acl in acl_list["matter"]["acl"]:
            name.append(acl["name"])
            fabric.append(acl["fabric"])
            nodeid.append(acl["nodeid"])
            target_name.append(acl["target_name"])
            target_id.append(acl["target_id"])
            privilege.append(acl["privilege"])
            auto_mode.append(acl["auto_mode"])
        tab = PrettyTable()
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('fabric', fabric, align='r', valign='t')
        tab.add_column('nodeid', nodeid, align='r', valign='t')
        tab.add_column('target_name', target_name, align='r', valign='t')
        tab.add_column('target_id', target_id, align='r', valign='t')
        tab.add_column('privilege', privilege, align='r', valign='t')
        tab.add_column('auto_mode', auto_mode, align='r', valign='t')
        self._logger.info("\n"+str(tab))

    def list_group_profile(self):
        self._logger.info("=== [Matter Stack] Group Setting List ===")
        self.clear_failed_data()
        group_list = self._MatterDM.get_fully_group_list()
        name = []
        group_id = []
        group_keyset_id = []
        epochkey0 = []
        epochkey1 = []
        epochkey2 = []
        for group in group_list["matter"]["group"]:
            name.append(group["name"])
            group_id.append(group["group_id"])
            group_keyset_id.append(group["group_keyset_id"])
            epochkey0.append(group["epochkey0"])
            epochkey1.append(group["epochkey1"])
            epochkey2.append(group["epochkey2"])
        tab = PrettyTable()
        tab.add_column('name', name, align='r', valign='t')
        tab.add_column('group_id', group_id, align='r', valign='t')
        tab.add_column('group_keyset_id', group_keyset_id,
                       align='r', valign='t')
        tab.add_column('epochkey0', epochkey0, align='r', valign='t')
        tab.add_column('epochkey1', epochkey1, align='r', valign='t')
        tab.add_column('epochkey2', epochkey2, align='r', valign='t')
        self._logger.info("\n"+str(tab))

    def get_profile(self, name):
        return self._MatterDM.get_node("name", name)

    def get_acl(self, name):
        return self._MatterDM.get_acl_list("name", name)

    def get_binding(self, name):
        return self._MatterDM.get_binding_list("name", name)

    def get_group(self, key, data):
        return self._MatterDM.get_group(key, data)

    def get_match_group(self, key, data):
        return self._MatterDM.get_match_group_list(key, data)

    def get_group_mapper(self, key, data):
        return self._MatterDM.get_group_mapper_list(key, data)

    def new_node_profile(self, *args, **kwargs):
        node = self._MatterDM.create_node(
            name=kwargs['name'], devicetype=kwargs['devicetype'], status="Pending")
        status = self._MatterDM.add_node(node)
        return node

    def new_acl_profile(self, *args, **kwargs):
        acl = self._MatterDM.create_acl(
            name=kwargs['name'], nodeid=kwargs['nodeid'], fabric=kwargs['fabric'],
            target_name=kwargs['target_name'], target_id=kwargs['target_id'],
            privilege=kwargs['privilege'], auto_mode=kwargs['auto_mode']
        )
        return acl

    def new_binding_profile(self, *args, **kwargs):
        binding = self._MatterDM.create_binding(
            name=kwargs['name'], fabric=kwargs['fabric'],
            nodeid=kwargs['nodeid'], target_name=kwargs['target_name'],
            target_id=kwargs['target_id'], endpoint=kwargs['endpoint']
        )
        return binding

    def new_group_profile(self, *args, **kwargs):
        group = self._MatterDM.create_group(name=kwargs['name'])
        status = self._MatterDM.add_group(group)
        return group

    def new_group_mapper_profile(self, *args, **kwargs):
        group_mapper = self._MatterDM.create_group_mapper(
            name=kwargs['name'], group_id=kwargs['group_id'],
            target_id=kwargs['target_id'], target_name=kwargs['target_name'],
            target_type=kwargs['target_type'], target_endpoint=kwargs['target_endpoint'],
            status=kwargs['status']
        )
        self._MatterDM.add_group_mapper(group_mapper)
        return group_mapper

    def apply_acl_profile(self, acl):
        self._MatterDM.add_acl(acl)

    def apply_binding_profile(self, binding):
        self._MatterDM.add_binding(binding)

    def update_profile(self, node):
        self._MatterDM.update_node(node)

    def update_group_profile(self, group):
        self._MatterDM.update_group_mapper(group)

    def delete_group(self, name):
        self._MatterDM.delete_match("group", "name", name)
        self._MatterDM.delete_match("group_mapper", "name", name)

    def delete_group_mapper(self, name, nodeid, endpoint):
        delete_count = self._MatterDM.delete_multi_match("group_mapper", {
            "name": name,
            "target_id": str(nodeid),
            "target_endpoint": str(endpoint),
        })
        self._logger.info(str(delete_count))

    def delete_group_acl(self, name, fabric, nodeid, target_name, auto_mode):
        self._MatterDM.delete_multi_match("acl", {
            "name": name, "fabric": fabric, "nodeid": nodeid,
            "auto_mode": auto_mode, "target_name": target_name
        })

    def clear_profile(self, node):
        self._MatterDM.delete_match("node", "name", node["name"])
        self._MatterDM.delete_match("acl", "name", node["name"])
        self._MatterDM.delete_match("acl", "target_name", node["name"])
        self._MatterDM.delete_match("binding", "name", node["name"])
        self._MatterDM.delete_match("binding", "target_name", node["name"])
        self._MatterDM.delete_match(
            "group_mapper", "target_name", node["name"])

    def clear_failed_data(self):
        self._MatterDM.delete_mismatch("node", "status", "Connected")
        self._MatterDM.delete_mismatch("group_mapper", "status", "Success")

    def unique_profile(self, target, key):
        return list(set(item[key] for item in target))


class ChipToolLightMgr:
    class OnoffAction(Enum):
        ON = 'on'
        OFF = 'off'
        TOGGLE = 'toggle'

    def __init__(self) -> None:
        self._CMDAccess = CMDAccess()
        self._ChipToolMgr = ChipToolMgr()
        self._logger = get_logger("APP")

    def onoff_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(ChipToolhelpper.CMDList.LIGHT_ONOFF.value + [
            str(kwargs["contain"]["action"]),
            str(kwargs["contain"]["nodeid"]),
            str(kwargs["contain"]["endpoint"])
        ]))
        return ChipToolhelpper.CMDList.LIGHT_ONOFF.value + [
            str(kwargs["contain"]["action"]),
            str(kwargs["contain"]["nodeid"]),
            str(kwargs["contain"]["endpoint"])
        ]

    def group_onoff_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(ChipToolhelpper.CMDList.LIGHT_GROUP_ONOFF.value[0:2] + [
            str(kwargs["contain"]["action"]),
            "0xffffffffffff" +
            str(hex(kwargs["contain"]["group_id"])[2:].zfill(4)),
            str(kwargs["contain"]["endpoint"])
        ]))
        return ChipToolhelpper.CMDList.LIGHT_GROUP_ONOFF.value[0:2] + [
            str(kwargs["contain"]["action"]),
            "0xffffffffffff" +
            str(hex(kwargs["contain"]["group_id"])[2:].zfill(4)),
            str(kwargs["contain"]["endpoint"])
        ]

    def level_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(ChipToolhelpper.CMDList.LEVEL_CTL.value + [
            str(kwargs["contain"]["level"]),
            str(kwargs["contain"]["transition"]),
            "0", "0",
            str(kwargs["contain"]["nodeid"]),
            str(kwargs["contain"]["endpoint"])
        ]))
        return ChipToolhelpper.CMDList.LEVEL_CTL.value + [
            str(kwargs["contain"]["level"]),
            str(kwargs["contain"]["transition"]),
            "0", "0",
            str(kwargs["contain"]["nodeid"]),
            str(kwargs["contain"]["endpoint"])
        ]

    def acl_passer(self, *args, **kwargs) -> None:
        self._logger.debug(json.dumps(
            ChipToolhelpper.CMDList.SET_ACL.value + [
                kwargs["contain"]["acl"],
                str(kwargs["contain"]["light_id"]),
                str(kwargs["contain"]["endpoint"])
            ]))
        return ChipToolhelpper.CMDList.SET_ACL.value + [
            kwargs["contain"]["acl"],
            str(kwargs["contain"]["light_id"]),
            str(kwargs["contain"]["endpoint"])
        ]

    def acl_json_passer(self, acl_list) -> None:
        rsp = [{
            "fabricIndex": acl_list[0]['fabric'],
            "privilege": 3, "authMode": 2,
            "subjects": [], "targets": None}, {
            "fabricIndex": acl_list[0]['fabric'],
            "privilege": 3, "authMode": 3,
            "subjects": [], "targets": None
        }]
        for acl in acl_list:
            if acl['target_id'] == 112233:
                rsp.append({
                    "fabricIndex": acl_list[0]['fabric'],
                    "privilege": 5, "authMode": 2,
                    "subjects": [acl['target_id']], "targets": None
                })
            elif (acl["privilege"] == 3 and acl["auto_mode"] == 2):
                rsp[0]["subjects"].append(acl['target_id'])
            elif (acl["privilege"] == 3 and acl["auto_mode"] == 3):
                rsp[1]["subjects"].append(acl['target_id'])
        self._logger.debug("="*50)
        self._logger.debug(json.dumps(rsp))
        return json.dumps(rsp)

    def command_passer(self, context_type, *args, **kwargs) -> None:
        cancat_dict = {
            ChipToolhelpper.QueryCMDMapper.LIGHT_ONOFF: self.onoff_passer,
            ChipToolhelpper.QueryCMDMapper.LIGHT_GROUP_ONOFF: self.group_onoff_passer,
            ChipToolhelpper.QueryCMDMapper.LEVEL_CONTROL: self.level_passer,
            ChipToolhelpper.QueryCMDMapper.ACCESS_CONTROL: self.acl_passer,
        }
        return cancat_dict[context_type](contain=kwargs["contain"])

    def handle_command(self, context_type: ChipToolhelpper.QueryCMDMapper, *args, **kwargs) -> None:
        command = self.command_passer(context_type, contain=kwargs)
        status, result = self._CMDAccess.send_command(command)
        return status, result

    def onoff(self, action, light_name, endpoint) -> None:
        self._ChipToolMgr.clear_failed_data()
        if not (any(x for x in self.OnoffAction if x.value == action)):
            self._logger.error("Invailed action type")

        self._logger.info("Stage: Send onoff")
        light_node = self._ChipToolMgr.get_profile(light_name)
        status, result = self.handle_command(ChipToolhelpper.QueryCMDMapper.LIGHT_ONOFF,
                                             action=action, nodeid=light_node['nodeid'],
                                             endpoint=endpoint)
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Connect failed")
        self._logger.info("The node: " + light_name +
                          ", action: " + str(action))

    def group_onoff(self, action, group_name, endpoint) -> None:
        self._ChipToolMgr.clear_failed_data()
        if not (any(x for x in self.OnoffAction if x.value == action)):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Invailed action type")

        self._logger.info("Stage: Send Group onoff")
        group = self._ChipToolMgr.get_group("name", group_name)
        status, result = self.handle_command(ChipToolhelpper.QueryCMDMapper.LIGHT_GROUP_ONOFF,
                                             action=action, group_id=group['group_id'],
                                             endpoint=endpoint)
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Connect failed")
        self._logger.info("The node: " + group_name +
                          ", action: " + str(action))

    def level(self, level, light_name, endpoint, transition) -> None:
        self._ChipToolMgr.clear_failed_data()
        light_node = self._ChipToolMgr.get_profile(light_name)

        self._logger.info("Stage: Send Level Control")
        status, result = self.handle_command(ChipToolhelpper.QueryCMDMapper.LEVEL_CONTROL,
                                             level=level, nodeid=light_node['nodeid'],
                                             transition=transition, endpoint=endpoint)
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Connect failed")
        self._logger.info("The node: " + light_name +
                          ", set level: " + str(level))

    def set_acl(self, light_node, switch_node) -> None:
        acl = self._ChipToolMgr.get_acl(light_node["name"])

        target_acl = {
            "name": light_node["name"], "fabric": light_node["fabric"],
            "nodeid": light_node["nodeid"], "target_name": switch_node["name"],
            "target_id": switch_node["nodeid"], "privilege": 3, "auto_mode": 2,
        }
        if (target_acl not in acl):
            acl.append(target_acl)
        else:
            self._logger.warning("ACL already existed")

        self._logger.debug(json.dumps(acl))
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.ACCESS_CONTROL,
            acl=self.acl_json_passer(acl),
            light_id=light_node["nodeid"],
            endpoint=0
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("set light ACL failed")

        acl = self._ChipToolMgr.new_acl_profile(
            name=light_node["name"], fabric=light_node["fabric"],
            nodeid=light_node["nodeid"], target_name=switch_node["name"],
            target_id=switch_node["nodeid"], privilege=3, auto_mode=2
        )
        self._ChipToolMgr.apply_acl_profile(acl)

    def bind_group_acl(self, node, group) -> None:
        acl = self._ChipToolMgr.get_acl(node["name"])
        target_acl = {
            "name": node["name"], "fabric": node["fabric"],
            "nodeid": node["nodeid"], "target_name": group["name"],
            "target_id": group["nodeid"], "privilege": 3, "auto_mode": 3,
        }
        if (target_acl not in acl):
            acl.append(target_acl)
        else:
            self._logger.warning("ACL already existed")

        self._logger.debug(json.dumps(acl))
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.ACCESS_CONTROL,
            acl=self.acl_json_passer(acl),
            light_id=node["nodeid"],
            endpoint=0
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("set light ACL failed")

        acl = self._ChipToolMgr.new_acl_profile(
            name=node["name"], nodeid=node["nodeid"], fabric=node["fabric"],
            target_name=group["name"], target_id=group["nodeid"],
            privilege=3, auto_mode=3
        )
        self._ChipToolMgr.apply_acl_profile(acl)

    def unbind_group_acl(self, node, group) -> None:
        self._ChipToolMgr.delete_group_acl(
            name=node["name"], fabric=node["fabric"],
            nodeid=node["nodeid"], auto_mode=3, target_name=group["name"],
        )
        acl = self._ChipToolMgr.get_acl(node["name"])

        self._logger.debug(json.dumps(acl))
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.ACCESS_CONTROL,
            acl=self.acl_json_passer(acl),
            light_id=node["nodeid"],
            endpoint=0
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("set light ACL failed")


class ChipToolSwitchMgr:
    @dataclass
    class GroupKeySet():
        groupKeySetID: int
        groupKeySecurityPolicy: int
        epochKey0: str
        epochStartTime0: int
        epochKey1: str
        epochStartTime1: int
        epochKey2: str
        epochStartTime2: int

    def __init__(self) -> None:
        self._CMDAccess = CMDAccess()
        self._ChipToolMgr = ChipToolMgr()
        self._ChipToolLightMgr = ChipToolLightMgr()
        self._logger = get_logger("APP")

    def binding_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.WRITE_BINDING.value + [
                kwargs["contain"]["binding_list"],
                str(kwargs["contain"]["nodeid"]),
                str(kwargs["contain"]["endpoint"])
            ]))
        return ChipToolhelpper.CMDList.WRITE_BINDING.value + [
            kwargs["contain"]["binding_list"],
            str(kwargs["contain"]["nodeid"]),
            str(kwargs["contain"]["endpoint"])
        ]

    def group_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.CREATE_GROUP.value + [
                str(kwargs["contain"]["name"]),
                str(kwargs["contain"]["group_id"])
            ]))
        return ChipToolhelpper.CMDList.CREATE_GROUP.value + [
            str(kwargs["contain"]["name"]),
            str(kwargs["contain"]["group_id"])
        ]

    def remove_group_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.REMOVE_GROUP.value + [
                str(kwargs["contain"]["group_id"])
            ]))
        return ChipToolhelpper.CMDList.REMOVE_GROUP.value + [
            str(kwargs["contain"]["group_id"])
        ]

    def keyset_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.CREATE_KEYSET.value + [
                str(kwargs["contain"]["group_keyset_id"]),
                str(kwargs["contain"]["groupKeySecurityPolicy"]),
                str(kwargs["contain"]["epochStartTime0"]),
                'hex:'+str(kwargs["contain"]["epochKey0"])
            ]))
        return ChipToolhelpper.CMDList.CREATE_KEYSET.value + [
            str(kwargs["contain"]["group_keyset_id"]),
            str(kwargs["contain"]["groupKeySecurityPolicy"]),
            str(kwargs["contain"]["epochStartTime0"]),
            'hex:'+str(kwargs["contain"]["epochKey0"])
        ]

    def remove_keyset_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.REMOVE_KEYSET.value + [
                str(kwargs["contain"]["group_keyset_id"]),
            ]))
        return ChipToolhelpper.CMDList.REMOVE_KEYSET.value + [
            str(kwargs["contain"]["group_keyset_id"]),
        ]

    def bind_group_keyset_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.BIND_GROUP_KEYSET.value + [
                str(kwargs["contain"]["group_id"]),
                str(kwargs["contain"]["group_keyset_id"])
            ]))
        return ChipToolhelpper.CMDList.BIND_GROUP_KEYSET.value + [
            str(kwargs["contain"]["group_id"]),
            str(kwargs["contain"]["group_keyset_id"])
        ]

    def unbind_group_keyset_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.UNBIND_GROUP_KEYSET.value + [
                str(kwargs["contain"]["group_id"]),
                str(kwargs["contain"]["group_keyset_id"]),
            ]))
        return ChipToolhelpper.CMDList.UNBIND_GROUP_KEYSET.value + [
            str(kwargs["contain"]["group_id"]),
            str(kwargs["contain"]["group_keyset_id"]),
        ]

    def apply_keyset_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.APPLY_KEYSET.value + [
                kwargs["contain"]["group_key_set"],
                str(kwargs["contain"]["target_nodeid"]),
                str(kwargs["contain"]["target_endpoint"])
            ]))
        return ChipToolhelpper.CMDList.APPLY_KEYSET.value + [
            kwargs["contain"]["group_key_set"],
            str(kwargs["contain"]["target_nodeid"]),
            str(kwargs["contain"]["target_endpoint"])
        ]

    def denied_keyset_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.DENIED_KEYSET.value + [
                str(kwargs["contain"]["group_keyset_id"]),
                str(kwargs["contain"]["target_nodeid"]),
                "0",
            ]))
        return ChipToolhelpper.CMDList.DENIED_KEYSET.value + [
            str(kwargs["contain"]["group_keyset_id"]),
            str(kwargs["contain"]["target_nodeid"]),
            "0",
        ]

    def apply_keyset_map_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.APPLY_KEYSET_MAP.value + [
                kwargs["contain"]["group_key_map_list"],
                str(kwargs["contain"]["target_nodeid"]),
                str(kwargs["contain"]["target_endpoint"])
            ]))
        return ChipToolhelpper.CMDList.APPLY_KEYSET_MAP.value + [
            kwargs["contain"]["group_key_map_list"],
            str(kwargs["contain"]["target_nodeid"]),
            str(kwargs["contain"]["target_endpoint"])
        ]

    def apply_group_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.APPLY_GROUP.value + [
                str(kwargs["contain"]["groupId"]),
                str(kwargs["contain"]["group_name"]),
                str(kwargs["contain"]["target_nodeid"]),
                str(kwargs["contain"]["target_endpoint"])
            ]))
        return ChipToolhelpper.CMDList.APPLY_GROUP.value + [
            str(kwargs["contain"]["groupId"]),
            str(kwargs["contain"]["group_name"]),
            str(kwargs["contain"]["target_nodeid"]),
            str(kwargs["contain"]["target_endpoint"])
        ]

    def denied_group_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.DENIED_GROUP.value + [
                str(kwargs["contain"]["groupId"]),
                str(kwargs["contain"]["target_nodeid"]),
                str(kwargs["contain"]["target_endpoint"])
            ]))
        return ChipToolhelpper.CMDList.DENIED_GROUP.value + [
            str(kwargs["contain"]["groupId"]),
            str(kwargs["contain"]["target_nodeid"]),
            str(kwargs["contain"]["target_endpoint"])
        ]

    def binding_json_passer(self, binding_list) -> None:
        rsp = []
        for binding in binding_list:
            rsp.append({
                "fabricIndex": binding['fabric'], "node": binding["target_id"],
                "endpoint": binding["endpoint"], "cluster": 6
            })
        self._logger.debug("="*50)
        self._logger.debug(json.dumps(rsp))
        return json.dumps(rsp)

    def keyset_map_json_passer(self, nodeid, fabric) -> None:
        group_mapper_list = self._ChipToolMgr.get_group_mapper(
            "target_id", nodeid)
        group_list = self._ChipToolMgr.unique_profile(
            group_mapper_list, "name")
        rows = []
        for group_item in group_list:
            rows += self._ChipToolMgr.get_match_group(
                "name", group_item)
        rsp = []
        for item in rows:
            self._logger.debug(json.dumps(item))
            rsp.append({
                "fabricIndex": fabric, "groupId": item["group_id"],
                "groupKeySetID": item["group_keyset_id"]
            })
        self._logger.debug("="*50)
        self._logger.debug(json.dumps(rsp))
        return json.dumps(rsp)

    def group_binding_json_passer(self, nodeid, group_id) -> None:
        group_mapper_list = self._ChipToolMgr.get_group_mapper(
            "target_id", nodeid)
        group_list = self._ChipToolMgr.unique_profile(
            group_mapper_list, "group_id")
        rsp = []
        for group in group_list:
            rsp.append({"group": group})
        rsp.append({"group": group_id})
        self._logger.debug("="*50)
        self._logger.debug(json.dumps(rsp))
        return json.dumps(rsp)

    def command_passer(self, context_type, *args, **kwargs) -> None:
        cancat_dict = {
            ChipToolhelpper.QueryCMDMapper.SET_BINDING: self.binding_passer,
            ChipToolhelpper.QueryCMDMapper.CREATE_GROUP: self.group_passer,
            ChipToolhelpper.QueryCMDMapper.REMOVE_GROUP: self.remove_group_passer,
            ChipToolhelpper.QueryCMDMapper.CREATE_KEYSET: self.keyset_passer,
            ChipToolhelpper.QueryCMDMapper.REMOVE_KEYSET: self.remove_keyset_passer,
            ChipToolhelpper.QueryCMDMapper.BIND_GROUP_KEYSET: self.bind_group_keyset_passer,
            ChipToolhelpper.QueryCMDMapper.UNBIND_GROUP_KEYSET: self.unbind_group_keyset_passer,
            ChipToolhelpper.QueryCMDMapper.APPLY_KEYSET: self.apply_keyset_passer,
            ChipToolhelpper.QueryCMDMapper.DENIED_KEYSET: self.denied_keyset_passer,
            ChipToolhelpper.QueryCMDMapper.APPLY_KEYSET_MAP: self.apply_keyset_map_passer,
            ChipToolhelpper.QueryCMDMapper.APPLY_GROUP: self.apply_group_passer,
            ChipToolhelpper.QueryCMDMapper.DENIED_GROUP: self.denied_group_passer,
        }
        return cancat_dict[context_type](contain=kwargs["contain"])

    def handle_command(self, context_type: ChipToolhelpper.QueryCMDMapper, *args, **kwargs) -> None:
        command = self.command_passer(context_type, contain=kwargs)
        status, result = self._CMDAccess.send_command(command)
        return status, result

    def set_binding(self, light_name, light_endpoint, switch_name, switch_endpoint):
        self._ChipToolMgr.clear_failed_data()
        light_node = self._ChipToolMgr.get_profile(light_name)
        switch_node = self._ChipToolMgr.get_profile(switch_name)
        self._ChipToolLightMgr.set_acl(
            light_node=light_node, switch_node=switch_node)

        binding_list = self._ChipToolMgr.get_binding(switch_node["name"])
        target_bind = {
            "name": switch_node["name"], "fabric": light_node['fabric'],
            "nodeid": switch_node["nodeid"], "endpoint": switch_endpoint,
            "target_name": light_node["name"], "target_id": light_node["nodeid"],
            "endpoint": light_endpoint,
        }
        if (target_bind not in binding_list):
            binding_list.append(target_bind)
        else:
            self._logger.warning("binding already in binding list")

        self._logger.info("Stage: Set Binding")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.SET_BINDING,
            binding_list=self.binding_json_passer(binding_list),
            nodeid=switch_node["nodeid"], endpoint=switch_endpoint
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("set switch binding failed")

        binding = self._ChipToolMgr.new_binding_profile(
            name=switch_node['name'], fabric=switch_node['fabric'],
            nodeid=switch_node['nodeid'], endpoint=switch_endpoint,
            target_name=light_node['name'], target_id=light_node['nodeid'],
            target_endpoint=light_endpoint
        )
        self._ChipToolMgr.apply_binding_profile(binding)
        self._logger.info("Success: Execute command")

    def gen_group(self, group_name):
        self._ChipToolMgr.clear_failed_data()
        group = self._ChipToolMgr.new_group_profile(name=group_name)

        self._logger.info("Stage: Create Group")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.CREATE_GROUP,
            name=group.name, group_id=group.group_id)
        if not (status == 0):
            for row in result:
                match = re.search(
                    r'CHIP Error 0x0000001F: invalid list length', row)
                if match:
                    self._logger.warning(
                        "chip-tool groups' count has reached the limit")
            self._ChipToolMgr.delete_group(group_name)
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Create Group failed")

        self._logger.info("Stage: Create Keyset")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.CREATE_KEYSET,
            group_keyset_id=group.group_keyset_id, groupKeySecurityPolicy=0,
            epochStartTime0=2220000, epochKey0=group.epochkey0
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Create GroupKeySet failed")

        self._logger.info("Stage: Bind Keyset")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.BIND_GROUP_KEYSET,
            group_id=group.group_id, group_keyset_id=group.group_keyset_id
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Bind Group-Keyset failed")
        self._logger.info("The group " + str(group_name) + " success created")
        self._logger.info("Success: Execute command")

    def del_group(self, group_name):
        self._ChipToolMgr.clear_failed_data()
        group = self._ChipToolMgr.get_group('name', group_name)
        self._ChipToolMgr.delete_group(group_name)
        self._logger.info(json.dumps(group))
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.UNBIND_GROUP_KEYSET,
            group_id=group['group_id'], group_keyset_id=group['group_keyset_id'])
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Unbind Group failed")

        # status, result = self.handle_command(
        #     ChipToolhelpper.QueryCMDMapper.REMOVE_KEYSET,
        #     group_keyset_id=group['group_keyset_id'])
        # if not (status == 0):
        #     self._logger.error("Remove Keyset failed")

        self._logger.info("Stage: Remove Group")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.REMOVE_GROUP,
            group_id=group['group_id'])
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Remove Group failed")
        self._logger.info("The group " + str(group_name) + " success remove")
        self._logger.info("Success: Execute command")

    def join_group(self, group_name, target_name, target_endpoint):
        self._ChipToolMgr.clear_failed_data()
        target_node = self._ChipToolMgr.get_profile(target_name)
        target_type = target_node['devicetype'].upper()
        group = self._ChipToolMgr.get_group("name", group_name)

        group_mapper = self._ChipToolMgr.new_group_mapper_profile(
            name=group['name'], group_id=group['group_id'],
            target_id=target_node['nodeid'], target_name=target_name,
            target_type=target_type, target_endpoint=target_endpoint,
            status="Init"
        )
        group_mapper.status = "Panding"
        self._ChipToolMgr.update_group_profile(group_mapper)

        GKS = self.GroupKeySet(
            groupKeySetID=group['group_id'], groupKeySecurityPolicy=0,
            epochKey0=group['epochkey0'], epochStartTime0=2220000,
            epochKey1=group['epochkey1'], epochStartTime1=2220001,
            epochKey2=group['epochkey2'], epochStartTime2=2220002,
        )

        self._logger.info("Stage: Apply Keyset")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.APPLY_KEYSET,
            group_key_set=json.dumps(dataclasses.asdict(GKS)),
            target_nodeid=target_node['nodeid'], target_endpoint="0"
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("APPLY_KEYSET failed")

        self._logger.info("Stage: Apply Keyset Map")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.APPLY_KEYSET_MAP,
            group_key_map_list=self.keyset_map_json_passer(
                target_node["nodeid"], target_node["fabric"]),
            target_nodeid=target_node["nodeid"], target_endpoint="0"
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("APPLY_KEYSET_MAP failed")

        self._logger.info("Stage: Apply Group")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.APPLY_GROUP,
            groupId=group['group_id'], group_name=group['name'],
            target_nodeid=target_node['nodeid'], target_endpoint=target_endpoint
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("APPLY_GROUP failed")

        self._logger.info("Stage: Setup Device Setting")
        self._logger.info(target_type.upper())
        if target_type == "LIGHT":
            group["nodeid"] = group['group_id']
            self._ChipToolLightMgr.bind_group_acl(target_node, group)
        elif target_type == "SWITCH":
            group_binding_list = self.group_binding_json_passer(
                target_node["nodeid"], group['group_id'])
            status, result = self.handle_command(
                ChipToolhelpper.QueryCMDMapper.SET_BINDING,
                binding_list=group_binding_list,
                nodeid=target_node["nodeid"], endpoint=target_endpoint
            )
            if not (status == 0):
                self._logger.info("Execute time: " + str(stop_timmer("CMD")))
                self._logger.error("SWITCH srt binding failed")

        group_mapper.status = "Success"
        self._ChipToolMgr.update_group_profile(group_mapper)
        self._logger.info("The group " + str(group_name) + " uccess join")
        self._logger.info("Success: Execute command")

    def leave_group(self, group_name, target_name, target_endpoint):
        self._ChipToolMgr.clear_failed_data()
        target_node = self._ChipToolMgr.get_profile(target_name)
        target_type = target_node['devicetype'].upper()
        group_list = self._ChipToolMgr.get_group_mapper("name", group_name)
        group = {}
        for item in group_list:
            if (item["target_name"] == target_name):
                group = item
                break
        if not group:
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Device name not found in group")
        self._ChipToolMgr.delete_group_mapper(
            name=group['name'], nodeid=target_node['nodeid'], endpoint=target_endpoint)

        self._logger.info("Stage: Clear Device Binding")
        self._logger.info(target_type)
        if target_type == "LIGHT":
            group["nodeid"] = group['group_id']
            self._ChipToolLightMgr.unbind_group_acl(target_node, group)
        elif target_type == "SWITCH":
            group_binding_list = self.group_binding_json_passer(
                target_node["nodeid"], group['group_id'])
            status, result = self.handle_command(
                ChipToolhelpper.QueryCMDMapper.SET_BINDING,
                binding_list=group_binding_list,
                nodeid=target_node["nodeid"], endpoint=target_endpoint
            )
            if not (status == 0):
                self._logger.info("Execute time: " + str(stop_timmer("CMD")))
                self._logger.error("SWITCH binding failed")

        self._logger.info("Stage: Clear KEYSET Binding")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.DENIED_KEYSET,
            group_keyset_id=group['group_id'],
            target_nodeid=target_node['nodeid'], target_endpoint="0"
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("DENIED_KEYSET failed")

        self._logger.info("Stage: Clear KEYSET MAP")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.DENIED_KEYSET_MAP,
            group_key_map_list=self.keyset_map_json_passer(
                target_node["nodeid"], target_node["fabric"]),
            target_nodeid=target_node["nodeid"], target_endpoint="0"
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("DENIED_KEYSET_MAP failed")

        self._logger.info("Stage: Clear Group")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.DENIED_GROUP,
            groupId=group['group_id'], target_nodeid=target_node['nodeid'],
            target_endpoint=target_endpoint
        )
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("DENIED_GROUP failed")

        self._logger.info("The group " + str(group_name) + " success leave")
        self._logger.info("Success: Execute command")


class ChipToolConnectMgr:
    def __init__(self) -> None:
        self._CMDAccess = CMDAccess()
        self._ChipToolMgr = ChipToolMgr()
        self._DBHandler = DatabaseHandler()
        self._OTBRMgr = OTBRMgr()
        self._logger = get_logger("CMD")

    def connect_passer(self, *args, **kwargs) -> None:
        return ChipToolhelpper.CMDList.CONNECT_THEAD.value + [
            str(kwargs["contain"]["nodeid"]),
            "hex:"+kwargs["contain"]["otbr_hex"],
            str(kwargs["contain"]["pincode"]),
            str(kwargs["contain"]["discriminator"]),
            "--ble-adapter",
            str(kwargs["contain"]["ble_adapter"])
        ]

    def disconnect_passer(self, *args, **kwargs) -> None:
        return ChipToolhelpper.CMDList.DISCONNECT_THEAD.value + [
            str(kwargs["contain"]["nodeid"])
        ]

    def reset_matter_passer(self, *args, **kwargs) -> None:
        self._logger.info(json.dumps(
            ChipToolhelpper.CMDList.RESET_MATTER.value))
        return ChipToolhelpper.CMDList.RESET_MATTER.value

    def disable_srp_passer(self, *args, **kwargs) -> None:
        return OTBRhelpper.CMDList.DISABLE_SRP.value

    def enable_srp_passer(self, *args, **kwargs) -> None:
        return OTBRhelpper.CMDList.ENABLE_SRP.value

    def command_passer(self, context_type, *args, **kwargs) -> None:
        cancat_dict = {
            ChipToolhelpper.QueryCMDMapper.CONN_THREAD: self.connect_passer,
            ChipToolhelpper.QueryCMDMapper.DISCONN_THREAD: self.disconnect_passer,
            ChipToolhelpper.QueryCMDMapper.RESET_MATTER: self.reset_matter_passer,
            OTBRhelpper.QueryCMDMapper.DISABLE_SRP: self.disable_srp_passer,
            OTBRhelpper.QueryCMDMapper.ENABLE_SRP: self.enable_srp_passer,
        }
        return cancat_dict[context_type](contain=kwargs["contain"])

    def handle_command(self, context_type, *args, **kwargs) -> None:
        command = self.command_passer(context_type, contain=kwargs)
        status, result = self._CMDAccess.send_command(command)
        return status, result

    def connect(self, name, devicetype, pincode, discriminator, ble_adapter):
        self._ChipToolMgr.clear_failed_data()
        self._logger.info("Stage: Get Thread Network")
        otbr_hex = self._ChipToolMgr.get_thread_network()

        self._logger.info("Stage: Start Connection")
        node = self._ChipToolMgr.new_node_profile(
            name=name, devicetype=devicetype)
        node.status = "Panding"
        self._ChipToolMgr.update_profile(node)
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.CONN_THREAD,
            nodeid=node.nodeid, pincode=pincode,
            discriminator=discriminator, otbr_hex=otbr_hex,
            ble_adapter=ble_adapter)
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Connect failed")

        fabric_index = -1
        for row in result:
            match = re.search(r'FabricIndex (\d+)', row)
            if match:
                fabric_index = match.group(1)
                if (fabric_index):
                    break
        if (fabric_index == -1):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error("Connected Fabric not found")

        node.status = "Connected"
        node.fabric = fabric_index
        self._ChipToolMgr.update_profile(node)

        self._logger.info("Stage: Setup ACL")
        acl = self._ChipToolMgr.new_acl_profile(name=node.name, fabric=fabric_index,
                                                nodeid=node.nodeid, target_name="Admin",
                                                target_id=112233, privilege=5,
                                                auto_mode=2)
        self._ChipToolMgr.apply_acl_profile(acl=acl)
        self._logger.info("The node name: " + node.name +
                          " already connnected")
        self._logger.info("Success: Execute command")

    def disconnect(self, name):
        self._ChipToolMgr.clear_failed_data()
        node = self._ChipToolMgr.get_profile(name)

        self._logger.info("Stage: Clear Profile")
        self._ChipToolMgr.clear_profile(node)

        self._logger.info("Stage: Start Disconnect")
        status, result = self.handle_command(
            ChipToolhelpper.QueryCMDMapper.DISCONN_THREAD,
            nodeid=node['nodeid'])
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error('Disconnect failed')

    def reset(self):
        self._DBHandler.init_database()
        self._logger.info("Stage: Clear Profile")
        for filePath in glob.glob('/tmp/chip_*'):
            try:
                os.remove(filePath)
            except:
                self._logger.error("Error while deleting file")

        self._logger.info("Stage: Restart SRP")
        status, result = self.handle_command(
            OTBRhelpper.QueryCMDMapper.DISABLE_SRP)
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error('DISABLE_SRP')

        time.sleep(3)
        status, result = self.handle_command(
            OTBRhelpper.QueryCMDMapper.ENABLE_SRP)
        if not (status == 0):
            self._logger.info("Execute time: " + str(stop_timmer("CMD")))
            self._logger.error('ENABLE_SRP')
