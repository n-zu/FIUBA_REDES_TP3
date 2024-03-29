from logging import info, warning, error, debug
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

from pox.core import core
from pox.lib.revent import *
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.revent.revent import EventMixin
import json

DEFAULT_RULES = "firewall_rules.json"
rules_json = r'{"rules": []}'
firewall_router_id = None

def _add_tos(block, tos):
    if isinstance(tos, int) and tos in range(0, 64):
        block.nw_tos = tos
    else:
        warning("Invalid TOS value: " + str(tos) + ", ignoring it")


def _add_ip_rule(rule, block, name):
    if isinstance(rule, dict):
        if "src" in rule:
            block.nw_src = str(rule["src"])
        if "dst" in rule:
            block.nw_dst = str(rule["dst"])
        if "tos" in rule:
            _add_tos(block, rule["tos"])

    elif isinstance(rule, list):
        try:
            block.nw_src = str(rule[0])
            block.nw_dst = str(rule[1])
            _add_tos(block, rule[2])
        except IndexError:
            pass  # the list may be shorter than 3 elements
    else:
        warning("Invalid " + name + " rule format, ignoring it")
        return
    debug("Added " + name + " rule: " + str(rule))


def add_ipv4_rule(rule, block):
    block.dl_type = pkt.ethernet.IP_TYPE
    _add_ip_rule(rule, block, "IPv4")


def add_ipv6_rule(rule, block):
    block.dl_type = pkt.ethernet.IPV6_TYPE
    _add_ip_rule(rule, block, "IPv6")


def add_eth_rule(rule, block):
    if isinstance(rule, dict):
        if "src" in rule:
            block.dl_src = EthAddr(rule["src"])
        if "dst" in rule:
            block.dl_dst = EthAddr(rule["dst"])
    elif isinstance(rule, list):
        block.dl_src = EthAddr(rule[0])
        block.dl_dst = EthAddr(rule[1])
    else:
        warning("Invalid eth rule format, ignoring it")
        return
    debug("Added eth rule: " + str(rule))


def _add_tp_rule(rule, block, name):
    if isinstance(rule, dict):
        if "src" in rule:
            block.tp_src = int(rule["src"])
        if "dst" in rule:
            block.tp_dst = int(rule["dst"])
    elif isinstance(rule, list):
        try:
            block.tp_src = int(rule[0])
            block.tp_dst = int(rule[1])
        except IndexError:
            pass  # the list may be shorter than 2 elements
    else:
        warning("Invalid" + name + "rule format, ignoring it")
        return
    debug("Added " + name + " rule: " + str(rule))


def add_tcp_rule(rule, block):
    block.dl_type = pkt.ethernet.IP_TYPE
    block.nw_proto = pkt.ipv4.TCP_PROTOCOL
    _add_tp_rule(rule, block, "TCP")


def add_udp_rule(rule, block):
    block.dl_type = pkt.ethernet.IP_TYPE
    block.nw_proto = pkt.ipv4.UDP_PROTOCOL
    _add_tp_rule(rule, block, "UDP")


def add_type_rule(rule, block):
    types = {
        "ipv4": pkt.ethernet.IP_TYPE,
        "ipv6": pkt.ethernet.IPV6_TYPE,
        "arp": pkt.ethernet.ARP_TYPE,
        "rarp": pkt.ethernet.RARP_TYPE,
        "vlan": pkt.ethernet.VLAN_TYPE,
    }

    rule = str(rule).lower()
    if rule in types:
        block.dl_type = types[rule]
    else:
        warning("Invalid type rule format, ignoring it")
        return
    debug("Added type rule: " + str(rule))


def add_proto_rule(rule, block):
    protos = {
        "tcp": pkt.ipv4.TCP_PROTOCOL,
        "udp": pkt.ipv4.UDP_PROTOCOL,
        "icmp": pkt.ipv4.ICMP_PROTOCOL,
    }
    block.dl_type = pkt.ethernet.IP_TYPE

    rule = str(rule).lower()
    if rule in protos:
        block.nw_proto = protos[rule]
    else:
        warning("Invalid protocol rule format, ignoring it")
        return

    debug("Added proto rule: " + str(rule))


def add_in_port_rule(rule, block):
    block.in_port = int(rule)
    debug("Added in_port rule: " + str(rule))


def warn_inconsistent_rule(rule):
    if "tcp" in rule and "udp" in rule:
        warning("Rule has both TCP and UDP, behavior is undefined")


def add_rule(event, rule):
    block = of.ofp_match()
    warn_inconsistent_rule(rule)

    if "eth" in rule:
        add_eth_rule(rule["eth"], block)
    if "ipv4" in rule:
        add_ipv4_rule(rule["ipv4"], block)
    if "tcp" in rule:
        add_tcp_rule(rule["tcp"], block)
    if "udp" in rule:
        add_udp_rule(rule["udp"], block)
    if "type" in rule:
        add_type_rule(rule["type"], block)
    if "proto" in rule:
        add_proto_rule(rule["proto"], block)
    if "in_port" in rule:
        add_in_port_rule(rule["in_port"], block)

    block_rule = of.ofp_flow_mod()
    block_rule.match = block
    event.connection.send(block_rule)


class SDNFirewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)

    def _handle_ConnectionUp(self, event):
        if event.dpid == firewall_router_id:
            rules = rules_json["rules"]
            for rule in rules:
                add_rule(event, rule)
            info("Firewall set up in switch %s" % firewall_router_id)


def launch(rules=DEFAULT_RULES, router_id=None):
    global rules_json
    global firewall_router_id
    if router_id is None:
        router_id = input("Enter the firewall router ID (1, 2, etc): ")
    firewall_router_id = int(router_id)

    try:
        with open(rules) as f:
            rules_json = json.load(f)
        info("Loaded rules from " + rules)
    except Exception as e:
        error("Could not load rules: " + str(e))

    core.registerNew(SDNFirewall)
