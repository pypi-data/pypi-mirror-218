"""iscsi.py: Module with methods for iSCSI initiator."""

#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import re
from pathlib import Path
from typing import ClassVar, Dict, List, Literal, Optional, Union, TypedDict

from sts import linux, mp, net, scsi
from sts.utils.cmdline import StsCompletedProcess, run, run_ret_out

PACKAGE_NAME = "iscsi-initiator-utils"
CLI_NAME = "iscsiadm"
ISCSID_SERVICE_NAME = "iscsid"
ISCSIUIO_SERVICE_NAME = "iscsiuio"


class IscsiAdm:
    """Class for `iscsiadm` cli tool (iscsi-initiator-utils)."""

    def __init__(
        self,
        debug_level: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8] = 0,
        disable_check: bool = False,
        verbose: bool = True,
    ) -> None:
        """Args:
        debug_level: print iscsiadm debug info (0-8)
        disable_check: disable argument validation.
        """
        self.disable_check = disable_check
        self.debug_level = debug_level
        self.verbose = verbose

        if not linux.install_package(PACKAGE_NAME, check=True, verbose=self.verbose):
            print(f"FATAL: Could not install {PACKAGE_NAME}")

    # available modes and respective short options available as per iscsiadm.c
    MODES: ClassVar[Dict[str, str]] = {
        "discovery": "DSIPdntplov",
        "discoverydb": "DSIPdntplov",
        "node": "RsPIdlSonvupTULW",
        "session": "PiRdrusonuSv",
        "host": "CHdPotnvxA",
        "iface": "HIdnvPoCabci",
        "fw": "dlWnv",
    }

    OPTIONS: ClassVar[Dict[str, str]] = {
        "p": "portal",
        "T": "targetname",
        "I": "interface",
        "o": "op",
        "t": "type",
        "n": "name",
        "v": "value",
        "H": "host",
        "r": "sid",
        "R": "rescan",
        "P": "print",
        "D": "discover",
        "l": "login",
        "L": "loginall",
        "u": "logout",
        "U": "logoutall",
        "s": "stats",
        "k": "killiscsid",
        "d": "debug",
        "S": "show",
        "V": "version",
        "h": "help",
        "C": "submode",
        "a": "ip",
        "b": "packetsize",
        "c": "count",
        "i": "interval",
        "x": "index",
        "A": "portal_type",
        "W": "no_wait",
    }

    def validate_mode(self, mode: str) -> None:
        """Checks if mode is valid iscsiadm mode.

        Args:
          mode: Example: "discovery"
        """
        if mode not in self.MODES:
            err_msg = f"Invalid {CLI_NAME} mode: {mode}"
            raise ValueError(err_msg)

    def validate_arguments(self, mode: str, arguments: Union[Dict[str, str], Dict[str, Optional[str]]]) -> None:
        available_options: List[str] = self.get_short_options_list(mode) + self.get_long_options_list(mode)
        for key, _value in arguments.items():
            key_to_check = key.strip("-")
            if key_to_check not in available_options:
                err_msg = f"Invalid {CLI_NAME} argument: {key}"
                raise ValueError(err_msg)

    def get_short_options_list(self, mode: str) -> List[str]:
        if mode not in self.MODES.keys():
            raise ValueError
        return [*self.MODES[mode]]

    def get_long_options_list(self, mode: str) -> List[str]:
        if mode not in self.MODES.keys():
            raise ValueError
        return [self.OPTIONS[short_option] for short_option in [*self.MODES[mode]]]

    def available_options(self, mode: str) -> List[str]:
        return self.get_short_options_list(mode) + self.get_long_options_list(mode)

    def _run(
        self,
        mode: str = "",
        arguments: Optional[Union[Dict[str, str], Dict[str, Optional[str]]]] = None,
        timeout: Union[int, None] = None,
    ) -> StsCompletedProcess:
        if mode is not None:
            self.validate_mode(mode)
        if arguments is not None and self.disable_check is not True:
            self.validate_arguments(mode, arguments)

        command_list: List[str] = [CLI_NAME, "--mode", mode]
        if arguments is not None:
            command_list = command_list + [f"{k}" if v is None else f"{k} {v}" for k, v in arguments.items()]
        if self.debug_level:
            command_list = [*command_list, "--debug", str(self.debug_level)]
        command: str = " ".join(command_list)
        return run(command, capture_output=True, timeout=timeout, verbose=self.verbose)

    def iface(
        self,
        op: str,
        iface: str,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ) -> StsCompletedProcess:
        return self._run(
            mode="iface",
            arguments={"-o": op, "-n": name, "-v": value, "-I": iface},
        )

    def iface_update(self, iface: str, name: str, value: str) -> StsCompletedProcess:
        return self.iface(op="update", iface=iface, name=f"iface.{name}", value=value)

    def iface_update_iqn(self, iface: str, iqn: str) -> StsCompletedProcess:
        return self.iface_update(iface=iface, name="initiatorname", value=iqn)

    def iface_update_ip(self, iface: str, ip: str) -> StsCompletedProcess:
        return self.iface_update(iface=iface, name="iface.ipaddress", value=ip)

    def iface_exists(self, iface: str) -> bool:
        return self.iface(op="show", iface=iface).returncode == 0

    def discovery(
        self,
        portal: str,
        type: str = "st",  # noqa: A002
        interface: Optional[str] = None,
        **kwargs: str,
    ) -> StsCompletedProcess:
        arguments = {"-t": type, "-p": portal, **kwargs}
        if interface:
            arguments.update({"-I": interface})
        return self._run(mode="discovery", arguments=arguments)

    def node(self, **kwargs: Union[str, Optional[str]]) -> StsCompletedProcess:
        return self._run(mode="node", arguments={**kwargs})

    def node_login(self, **kwargs: str) -> StsCompletedProcess:
        arguments = {"--login": None, **kwargs}
        return self.node(**arguments)

    def node_logout(self, **kwargs: str) -> StsCompletedProcess:
        arguments = {"--logout": None, **kwargs}
        return self.node(**arguments)


class IfaceVars(TypedDict):
    hwaddress: str
    iscsi_ifacename: str
    net_ifacename: str
    transport_name: str
    initiatorname: str
    isid: str
    bootproto: str
    ipaddress: str
    prefix_len: str
    subnet_mask: str
    gateway: str
    primary_dns: str
    secondary_dns: str
    vlan_id: str
    vlan_priority: str
    vlan_state: str
    ipv6_linklocal: str
    ipv6_router: str
    ipv6_autocfg: str
    linklocal_autocfg: str
    router_autocfg: str
    state: str
    iface_num: str
    mtu: str
    port: str
    delayed_ack: str
    tcp_nagle: str
    tcp_wsf_state: str
    tcp_wsf: str
    tcp_timer_scale: str
    tcp_timestamp: str
    dhcp_dns: str
    dhcp_slp_da: str
    tos_state: str
    tos: str
    gratuitous_arp: str
    dhcp_alt_client_id_state: str
    dhcp_alt_client_id: str
    dhcp_req_vendor_id_state: str
    dhcp_vendor_id_state: str
    dhcp_vendor_id: str
    dhcp_learn_iqn: str
    fragmentation: str
    incoming_forwarding: str
    ttl: str
    gratuitous_neighbor_adv: str
    redirect: str
    ignore_icmp_echo_request: str
    mld: str
    flow_label: str
    traffic_class: str
    hop_limit: str
    nd_reachable_tmo: str
    nd_rexmit_time: str
    nd_stale_tmo: str
    dup_addr_detect_cnt: str
    router_adv_link_mtu: str
    def_task_mgmt_timeout: str
    header_digest: str
    data_digest: str
    immediate_data: str
    initial_r2t: str
    data_seq_inorder: str
    data_pdu_inorder: str
    erl: str
    max_receive_data_len: str
    first_burst_len: str
    max_outstanding_r2t: str
    max_burst_len: str
    chap_auth: str
    bidi_chap: str
    strict_login_compliance: str
    discovery_auth: str
    discovery_logout: str

class TargetVars(TypedDict):
    name: str  # iqn
    interface: str
    portal: str  # ip or hostname
    type: str  # discovery type

class ConfVars(TypedDict):
    initiatorname: str  # iqn.1994-05.redhat:example
    targets: List[TargetVars]
    ifaces: List[IfaceVars]

class AuthFields(TypedDict):
    tbl_idx: str
    authmethod: str
    username: str
    password: str
    password_length: str
    username_in: str
    password_in: str


def setup(variables: ConfVars) -> bool:
    """Configure iSCSI initiator based on env variables."""
    iscsiadm = IscsiAdm(verbose=True)

    if "initiatorname" in variables:
        if not set_initiatorname(variables["initiatorname"]):
            return False
        linux.service_restart(ISCSID_SERVICE_NAME, verbose=False)

    if "ifaces" in variables:
        for iface in variables["ifaces"]:
            ifacename = iface["iscsi_ifacename"]
            if ("qedi" in ifacename or "bnx2i" in ifacename) and not linux.is_service_running(ISCSIUIO_SERVICE_NAME):
                linux.service_enable(ISCSIUIO_SERVICE_NAME, now=True)
            if not iscsiadm.iface_exists(iface = ifacename):
                create_iscsi_iface(iface_name=ifacename)
            for n, v in iface.items():
                if n == "iscsi_ifacename":
                    continue
                completed_process = iscsiadm.iface_update(iface=ifacename, name=n, value=v)
                ret = completed_process.returncode
                out = completed_process.output
                if ret != 0:
                    print(f"FAIL: iscsi update command returned {ret}. Output: {out}")
                    return False

    if "targets" in variables:
        for target in variables["targets"]:
            if iscsiadm.discovery(**target) != 0:
                return False

    if not linux.is_service_enabled(ISCSID_SERVICE_NAME):
        linux.service_enable(ISCSID_SERVICE_NAME)
    return True


def discovery_login(iface_name, portal, iqn, iface_ip=None, subnet_mask=None, gateway=None) -> bool:  # noqa: ANN001
    if not iface_name or not portal or not iqn:
        print("FAIL: auto_conf() - Missing iface_name, portal or iqn")
        return False

    if iface_ip and not iface_set_ip(iface_name, iface_ip, subnet_mask, gateway):
        print(f"FAIL: auto_conf() - Could not set IP for {iface_name}")
        return False

    print("INFO: IQN will be set to " + iqn)

    if not iface_set_iqn(iqn, iface_name):
        print(f"FAIL: auto_conf() - Could not set {iqn} to iface {iface_name}")
        return False

    if not discovery_st(portal, ifaces=iface_name, disc_db=True):
        print(f"FAIL: auto_conf() - Could not discover any target on {portal} using iface {iface_name}")
        return False

    if not node_login():
        print("FAIL: auto_conf() - Could not login to new discovered portal")
        return False
    print(f"INFO: Iface {iface_name} logged in successfully to {portal}")

    return True


# used to match regex for each session information that we support
supported_discovery_info = {
    "address": r".*DiscoveryAddress: (\S+)",
    "target": r".*Target: (\S+)",
    "portal": r".*Portal: (\S+):(\S+),(\S+)",
    "iface": r".*Iface Name: (\S+)",
}

# used to match regex for each session information that we support
supported_session_info = {
    "t_iqn": r".*Target: (\S+)",
    "h_iqn": r".*Iface Initiatorname: (\S+)",
    "iface": r".*Iface Name: (\S+)",
    "transport": r".*Iface Transport: (\S+)",
    "iface_ip": r".*Iface IPaddress: (\S+)",
    "mac": r".*Iface HWaddress: (\S+)",
    "sid": r".*SID: (\S+)",
    "host": r".*Host Number: (\S+).*State: (\S+)",  # e.g. Host Number: 6	State: running
    "disks": r".*Attached scsi disk (\S+).*State: (\S+)",
    # eg. Attached scsi disk sdb		State: running
    "target_ip": r".*Current Portal: (\S+):[0-9]+,",
    "persist_ip": r".*Persistent Portal: (\S+):[0-9]+,",
    # negotiated parameters
    "header_digest": r".*HeaderDigest: (\S+)",
    "data_digest": r".*DataDigest: (\S+)",
    "max_recv": r".*MaxRecvDataSegmentLength: (\S+)",
    "max_xmit": r".*MaxXmitDataSegmentLength: (\S+)",
    "first_burst": r".*FirstBurstLength: (\S+)",
    "max_burst": r".*MaxBurstLength: (\S+)",
    "immediate_data": r".*ImmediateData: (\S+)",
    "initial_r2t": r".*InitialR2T: (\S+)",
    "max_outst_r2t": r".*MaxOutstandingR2T: (\S+)",
}

host_path = "/sys/class/iscsi_host/"


def is_iqn(iqn):  # noqa: ANN001, ANN201
    if re.match(r"^iqn\.", iqn):
        return True
    return False


def install():  # noqa: ANN201
    """Install iscsiadm tool
    The arguments are:
    None
    Returns:
    True: If iscsiadm is installed correctly
    False: If some problem happened.
    """
    if not linux.install_package(PACKAGE_NAME):
        print(f"FAIL: Could not install {PACKAGE_NAME}")
        return False

    return True


# Return an array with all iscsi_hosts numbers
def get_iscsi_hosts():  # noqa: ANN201
    cmd = "ls " + host_path
    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
    if retcode != 0:
        return None
    # remove 'host' prefix
    output = re.sub("host", "", output)
    return output.split()


# iSCSI discovery ###
def query_discovery():  # noqa: ANN201
    """Query all iSCSI targets
    The arguments are:
    None
    Returns:
    Dict:    Dict with all discovered targets
    None:    If some problem happened.
    """
    cmd = "iscsiadm -m discovery -P1"
    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
    if retcode != 0:
        # If no target is found iscsiadm returns error code
        return None
    lines = output.split("\n")

    supported_discovery_modes = ["SENDTARGETS", "iSNS", "STATIC", "FIRMWARE"]
    supported_mode_type = {"SENDTARGETS": "sendtargets", "iSNS": "isns"}

    discovery_info_dict = {}
    discovery_address = None
    disc_mode = None
    target_name = None

    for line in lines:
        # print "(%s)" % line
        # Check if it is discovery mode information
        m = re.match("(^.*):", line)
        if m and m.group(1) in supported_discovery_modes:
            disc_mode = m.group(1)
            # We will use DiscoveryAddress as key
            discovery_info_dict[disc_mode] = {}
            discovery_address = None
            continue

        # We will use TargetAddress as key for the target dictionary
        m = re.match(supported_discovery_info["address"], line)
        if m:
            discovery_address = m.group(1)
            if discovery_address not in list(discovery_info_dict[disc_mode].keys()):
                discovery_info_dict[disc_mode][discovery_address] = {}
            disc_addr_regex = re.compile(r"(\S+),(\S+)")
            d = disc_addr_regex.match(discovery_address)
            if d:
                discovery_info_dict[disc_mode][discovery_address]["disc_addr"] = d.group(1)
                discovery_info_dict[disc_mode][discovery_address]["disc_port"] = d.group(2)

            if disc_mode in list(supported_mode_type.keys()):
                discovery_info_dict[disc_mode][discovery_address]["mode"] = supported_mode_type[disc_mode]
            continue

        m = re.match(supported_discovery_info["target"], line)
        if m:
            # FIRMWARE discovery might not use discovery address
            if not discovery_address:
                discovery_address = "NotSet"
                discovery_info_dict[disc_mode][discovery_address] = {}

            target_name = m.group(1)
            if "targets" not in list(discovery_info_dict[disc_mode][discovery_address].keys()):
                discovery_info_dict[disc_mode][discovery_address]["targets"] = {}
            discovery_info_dict[disc_mode][discovery_address]["targets"][target_name] = {}
            continue

        m = re.match(supported_discovery_info["portal"], line)
        if m:
            discovery_info_dict[disc_mode][discovery_address]["targets"][target_name]["portal"] = {}
            discovery_info_dict[disc_mode][discovery_address]["targets"][target_name]["portal"]["address"] = m.group(1)
            discovery_info_dict[disc_mode][discovery_address]["targets"][target_name]["portal"]["port"] = m.group(2)
            continue

        m = re.match(supported_discovery_info["iface"], line)
        if m:
            iface = m.group(1)
            if "iface" not in list(discovery_info_dict[disc_mode][discovery_address]["targets"][target_name].keys()):
                discovery_info_dict[disc_mode][discovery_address]["targets"][target_name]["iface"] = []
            discovery_info_dict[disc_mode][discovery_address]["targets"][target_name]["iface"].append(iface)
            continue
            # print "Found %s: %s" % (key, m.group(1))

    return discovery_info_dict


def discovery_st(target, ifaces=None, disc_db=False):  # noqa: ANN001, ANN201
    """Discover iSCSI target
    The arguments are:
    target:   Address of target to be discovered
    ifaces:   iSCSI interfaces to be used, separated by space (optional)
    disc_db:  To use discoverydb instead of discovery (optional).

    Returns:
    True:     If it discovered an iSCSI target
    False:    If some problem happened.
    """
    max_retries = 5
    print("INFO: Executing Discovery_ST() with these arges:")
    print(f"\tTarget: {target}")
    if ifaces:
        print(f"\tIfaces: {ifaces}")

    disc_opt = "discovery"
    operation = None

    if disc_db:
        disc_opt = "discoverydb -D"
        operation = "new"

    cmd = f"iscsiadm -m {disc_opt} -p {target}"
    if operation:
        cmd += f" -o {operation}"

    if ifaces:
        if ("bnx2i" in ifaces or "qedi" in ifaces) and linux.is_service_running(ISCSIUIO_SERVICE_NAME) != 0:
            linux.service_enable(ISCSIUIO_SERVICE_NAME, now=True)
        interfaces = ifaces.split(" ")
        for interface in interfaces:
            cmd += f" -I {interface}"
    cmd += " -t st"
    retries = 0
    retcode, data = run_ret_out(cmd, return_output=True, verbose=True)
    while retcode == 0 and "(err 29)" in data and retries < max_retries:
        retcode, data = run_ret_out(cmd, return_output=True, verbose=True)
        retries += 1
    if retcode != 0 or retries == max_retries:
        print(f"FAIL: Could not discover iSCSI target. Return code: {retcode}")
        return False
    return True


def is_target_discovered(t_iqn):  # noqa: ANN001, ANN201
    """Check if an iSCSI target is already discovered
    The arguments are:
    iSCSI Target:   iQN of iSCSI target
    Returns:
    True:     If target is discovered
    False:    If was not found.
    """
    if not t_iqn:
        print("FAIL: is_target_discovered() - requires target iqn as parameter")

    disc_dict = query_discovery()
    if not disc_dict:
        return False

    for disc_type in list(disc_dict.keys()):
        for disc_addr in list(disc_dict[disc_type].keys()):
            if "targets" not in list(disc_dict[disc_type][disc_addr].keys()):
                continue
            if t_iqn in list(disc_dict[disc_type][disc_addr]["targets"].keys()):
                # Target is already discovered we do not need to do anything
                return True
    return False


def get_disc_ifaces_of_t_iqn(t_iqn):  # noqa: ANN001, ANN201
    """From given target IQN, return the interfaces that discovered it
    The arguments are:
    iSCSI Target:   iQN of iSCSI target
    Returns:
    List ifaces:     Discovered interfaces
    None:             If iface was not found.
    """
    if not t_iqn:
        print("FAIL: get_t_iqn_disc_ifaces() - requires target iqn")
        return None

    if not is_target_discovered(t_iqn):
        print(f"FAIL: get_t_iqn_disc_ifaces() - target iqn: {t_iqn} is not discovered")
        return None

    disc_dict = query_discovery()
    for disc_type in list(disc_dict.keys()):
        for disc_addr in list(disc_dict[disc_type].keys()):
            if "targets" not in list(disc_dict[disc_type][disc_addr].keys()):
                continue
            if t_iqn in list(disc_dict[disc_type][disc_addr]["targets"].keys()) and "iface" in list(
                disc_dict[disc_type][disc_addr]["targets"][t_iqn].keys(),
            ):
                return disc_dict[disc_type][disc_addr]["targets"][t_iqn]["iface"]
    return None


def delete_discovery_target_portal(portal, port="3260", tp="st"):  # noqa: ANN001, ANN201
    """Delete discovered iSCSI target
    The arguments are:
    portal:   Address of target to be discovered
    port:     Port of iSCSI target to be deleted
    tp:       Discovery type, sendtargets, isns...

    Returns:
    True:     If deleted discovered iSCSI target
    False:    If some problem happened.
    """
    print(f"INFO: Deleting target portal: {portal}")
    if net.get_ip_version(portal) == 6:
        # IF IPv6 we need to append squared brackets to the address
        portal = "[" + portal + "]"

    cmd = f'iscsiadm -m discoverydb --type {tp} --portal "{portal}:{port}" -o delete'
    if run(cmd).returncode != 0:
        print("FAIL: Could not delete discover iSCSI target")
        return False
    return True


def clean_up(portal="all"):  # noqa: ANN001, ANN201
    """Remove iSCSI session and discover information for specific target
    The arguments are:
    target:   Address of target to be removed
    Returns:
    True:     If iSCSI target is removed
    False:    If some problem happened.
    """
    error = 0
    # TODO: iSCSI boot clean up
    if is_iscsi_boot():
        boot_dev = linux.get_boot_device()
        if not boot_dev:
            print("FAIL: clean_up() - Could not determine boot device")
            return False

        boot_wwid = linux.get_device_wwid(boot_dev)
        if not boot_wwid:
            print(f"FAIL: clean_up() - Could not determine boot WWID for {boot_dev}")
            return False

        ses_ids = get_all_session_ids()
        if not ses_ids:
            print("FAIL: is_iscsi_boot() - It is iSCSI boot, but did not find any session id")
            return False

        if portal == "all":
            # Logout from all iSCSI session, that do not have boot device
            for ses_id in ses_ids:
                iscsi_wwids = scsi_wwid_of_iscsi_session(sid=ses_id)
                if boot_wwid in iscsi_wwids:
                    print(f"INFO: Can't log out of session {ses_id}, because it is used for iSCSI boot")
                else:
                    print(f"INFO: Logging out of session {ses_id}")
                    session_logout(ses_id)
                    # TODO Clean up discovery info
        else:
            # TODO Logout single portal from iSCSI boot
            print(f"FAIL: clean_up() - Does not know how to clean up portal {portal} for iSCSI boot")
            return False

        return True

    # Not iSCSI boot
    if portal == "all":
        # log out of all iSCSI sessions
        if get_all_session_ids():  # noqa: SIM102
            # There is at least one session
            if not node_logout():
                print(f"FAIL: Could not logout from {portal} iSCSI target")
                error += 1
    elif not node_logout(portal=portal):
        print(f"FAIL: Could not logout from {portal} iSCSI target")
        error += 1

    disc_dict = query_discovery()
    # If there is discovery information
    if disc_dict:
        # We will search for this portal on sendtargets and iSNS
        for mode in list(disc_dict.keys()):
            if mode != "SENDTARGETS" and mode != "iSNS":
                # We only delete discover info for st and isns
                continue
            m_dict = disc_dict[mode]
            # Search for all discovered address if they match the one given
            for addr in list(m_dict.keys()):
                d_dict = m_dict[addr]

                disc_addr = d_dict["disc_addr"]
                port = d_dict["disc_port"]
                if disc_addr == portal or portal == "all":  # noqa: SIM102
                    if not delete_discovery_target_portal(disc_addr, port=port, tp=d_dict["mode"]):
                        print(f"FAIL: Deleting iSCSI target {d_dict['disc_addr']}")
                        error += 1

    if error:
        return False
    return True


# iSCSI session ###
# def query_sessions():
#    #cmd output: tcp: [21] 127.0.0.1:3260,1 iqn.2009-10.com.redhat:storage-1 (non-flash)
#    cmd = "iscsiadm -m session"
#    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
#    if (retcode != 0):
#        return None
#    lines = output.split("\n")
#    session_regex = re.compile("(\S+):\s[(\d+)]\s(\S+):(\S+),(\d+),(\S+)")
#    sessions_dict = {}
#    for line in lines:
#        m = session_regex.search(line)
#        if m:
#            sid = m.group(2)
#            ses_dict = {}
#            ses_dict["driver"] = m.group(1)
#            ses_dict["portal"] = m.group(3)
#            ses_dict["portal_port"] = m.group(4)
#            ses_dict["target_iqn"] = m.group(6)
#            sessions[sid] = ses_dict
#    return sessions_dict


def get_all_session_ids():  # noqa: ANN201
    cmd = "iscsiadm -m session -P1"
    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
    if retcode != 0:
        # print ("INFO: there is no iSCSI session")
        return None
    lines = output.split("\n")

    session_ids = []

    for line in lines:
        m = re.match(supported_session_info["sid"], line)
        if not m:
            continue
        # print "Found session id: %s" %m.group(1)
        session_ids.append(m.group(1))
    return session_ids


def query_iscsi_session(sid):  # noqa: ANN001, ANN201
    """Query information from a specific iSCSI session
    The arguments are:
    sid:      Session id
    Returns:
    Dict:     A dictionary with session info
    None:     If some problem happened.
    """
    if not sid:
        print("FAIL: query_iscsi_session() - requires sid as argument")
        return None

    regex_session_scsi_id = "^[ \t]+scsi([0-9]+) Channel ([0-9]+) Id ([0-9])+ Lun: ([0-9]+)$"
    cmd = f"iscsiadm -m session -P3 -S -r {sid}"
    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
    if retcode != 0:
        return None
    lines = output.split("\n")

    session_info_dict = {}
    # dict with disk name and its status
    session_disks_dict = {}
    # store host number and status
    session_host_dict = {}
    for line in lines:
        # print "(%s)" % line

        m = re.match(regex_session_scsi_id, line)
        if m:
            host_id = m.group(1)
            target_id_only = m.group(2)
            bus_id_only = m.group(3)
            lun_id = m.group(4)
            target_id_only = re.sub("^0+(?=.)", "", target_id_only)
            scsi_id = f"{host_id}:{target_id_only}:{bus_id_only}:{lun_id}"

            if "scsi_id_info" not in list(session_info_dict.keys()):
                session_info_dict["scsi_id_info"] = {}
            session_info_dict["scsi_id_info"][scsi_id] = {}
            session_info_dict["scsi_id_info"][scsi_id]["scsi_id"] = scsi_id

        # Could be more than one scsi disk, will add as dict
        m = re.match(supported_session_info["disks"], line)
        if m:
            disk_dict = {"status": m.group(2), "wwid": scsi.wwid_of_disk(m.group(1))}
            # disk_dict["scsi_name"] = m.group(1)
            session_disks_dict[m.group(1)] = disk_dict
            continue

        # Could be more than one scsi disk, will add as dict
        m = re.match(supported_session_info["host"], line)
        if m:
            session_host_dict[m.group(1)] = m.group(2)
            continue
        # Generic search for keys and values
        for key in list(supported_session_info.keys()):
            m = re.match(supported_session_info[key], line)
            if not m:
                continue
            # print "Found %s: %s" % (key, m.group(1))
            session_info_dict[key] = m.group(1)
            if session_info_dict[key] == "<empty>":
                session_info_dict[key] = None
                if key == "mac":  # noqa: SIM102
                    # Try to get based on iface IP address
                    if "iface_ip" in list(session_info_dict.keys()):
                        nic = net.get_nic_of_ip(session_info_dict["iface_ip"])
                        if nic:
                            session_info_dict[key] = net.get_mac_of_nic(nic)
    # added info for the specific session
    session_info_dict["disks"] = session_disks_dict
    session_info_dict["host"] = session_host_dict
    return session_info_dict


def query_all_iscsi_sessions() -> Union[dict, None]:
    """First we get all iSCSI ids, later on we get the information of each session individually."""
    session_ids = get_all_session_ids()
    if not session_ids:
        return None

    iscsi_sessions = {}
    # Collecting info from each session
    for sid in session_ids:
        session_info_dict = query_iscsi_session(sid)
        iscsi_sessions[sid] = session_info_dict

    # print iscsi_sessions
    return iscsi_sessions


def session_logout(sid=None):  # noqa: ANN001, ANN201
    cmd = "iscsiadm -m session -u"
    if sid:
        cmd += f" -r {sid}"
    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
    if retcode != 0:
        print(output)
        print("FAIL: session_logout() - Could not logout from session")
        return None
    return True


def get_iscsi_session_by_scsi_id(scsi_id):  # noqa: ANN001, ANN201
    """Return the Session Dict that has the scsi_id."""
    sessions = query_all_iscsi_sessions()
    if not sessions:
        return None

    for ses in sessions:
        if "scsi_id_info" not in list(sessions[ses].keys()):
            continue
        if scsi_id in list(sessions[ses]["scsi_id_info"].keys()):
            return sessions[ses]
    return None


def h_iqn_of_sessions():  # noqa: ANN201
    """Usage
        h_iqn_of_sessions()
    Purpose
        Get the Host IQNs of all active iSCSI sessions
    Parameter
        None
    Returns
        List:   h_iqns
            or
        None.
    """
    h_iqns = None
    sessions = query_all_iscsi_sessions()
    if not sessions:
        return None

    for key in list(sessions.keys()):
        info = sessions[key]
        if "h_iqn" in list(info.keys()):
            if not h_iqns:
                h_iqns = []
            if info["h_iqn"] not in h_iqns:
                h_iqns.append(info["h_iqn"])
    return h_iqns


def t_iqn_of_sessions():  # noqa: ANN201
    """Usage
        t_iqn_of_sessions()
    Purpose
        Get the Target IQNs of all active iSCSI sessions
    Parameter
        None
    Returns
        List:   t_iqns
            or
        None.
    """
    t_iqns = None
    sessions = query_all_iscsi_sessions()
    if not sessions:
        return None

    for key in list(sessions.keys()):
        info = sessions[key]
        if "t_iqn" in list(info.keys()):
            if not t_iqns:
                t_iqns = []
            if info["t_iqn"] not in t_iqns:
                t_iqns.append(info["t_iqn"])
    return t_iqns


def mac_of_iscsi_session():  # noqa: ANN201
    """Usage
        mac_of_iscsi_session()
    Purpose
        We only check host IQN in active iSCSI session.
    Parameter
        None
    Returns
        List:   macs
            or
        None.
    """
    macs = None
    sessions = query_all_iscsi_sessions()
    if not sessions:
        return None

    for key in list(sessions.keys()):
        info = sessions[key]
        if "mac" in list(info.keys()):
            if not macs:
                macs = []
            if info["mac"] != "<empty>" and info["mac"] and info["mac"] not in macs:
                macs.append(info["mac"])
    return macs


def scsi_names_of_iscsi_session(h_iqn=None, t_iqn=None, sid=None):  # noqa: ANN001, ANN201
    """Usage
        scsi_names_of_iscsi_session();
        scsi_names_of_iscsi_session(sid=1);
        scsi_names_of_iscsi_session(h_iqn=h_iqn, t_iqn=t_iqn);
    # we should not support this method since the h_iqn for qla4xxx
    #    scsi_names_of_iscsi_session(t_iqn=t_iqn, h_iqn=h_iqn);
        scsi_names_of_iscsi_session(iface=iface,target_ip=target_ip,;
            t_iqn=t_iqn);
        scsi_names_of_iscsi_session(session_id=session_id);
    Purpose
        Query out all SCSI device names for certain iscsi session.
    Parameter
        h_iqn                  # the IQN used by the host
        t_iqn                  # the IQN used by iscsi target
        sid                    # the iSCSI session id
    Returns
        scsi_names
            or
        None.
    """
    sessions = query_all_iscsi_sessions()
    if not sessions:
        return None

    if sid:
        if sid in list(sessions.keys()) and "disks" in list(sessions[sid].keys()):
            return list(sessions[sid]["disks"].keys())
        return None

    scsi_names = None
    if not h_iqn and not t_iqn:
        for sid in list(sessions.keys()):
            if "disks" in list(sessions[sid].keys()):
                if not scsi_names:
                    scsi_names = []
                scsi_names.extend(list(sessions[sid]["disks"].keys()))
        return scsi_names

    if h_iqn and t_iqn:
        for sid in list(sessions.keys()):
            if (sessions[sid]["h_iqn"] == h_iqn and sessions[sid]["t_iqn"] == t_iqn) and "disks" in list(
                sessions[sid].keys(),
            ):
                if not scsi_names:
                    scsi_names = []
                scsi_names.extend(list(sessions[sid]["disks"].keys()))
        return scsi_names

    print("FAIL: scsi_names_of_iscsi_session() - Unsupported parameters given")
    return None


def scsi_wwid_of_iscsi_session(h_iqn=None, t_iqn=None, sid=None):  # noqa: ANN001, ANN201
    """Usage
        scsi_wwid_of_iscsi_session();
        scsi_wwid_of_iscsi_session(sid=1);
        scsi_wwid_of_iscsi_session(h_iqn=h_iqn, t_iqn=t_iqn);
    # we should not support this method since the h_iqn for qla4xxx
    #    scsi_wwid_of_iscsi_session(t_iqn=t_iqn, h_iqn=h_iqn);
        scsi_wwid_of_iscsi_session(iface=iface,target_ip=target_ip,;
            t_iqn=t_iqn);
        scsi_wwid_of_iscsi_session(session_id=session_id);
    Purpose
        Query out all SCSI WWIDs for certain iscsi session.
    Parameter
        h_iqn                  # the IQN used by the host
        t_iqn                  # the IQN used by iscsi target
        sid                    # the iSCSI session id
    Returns
        wwids
            or
        None.
    """
    wwids = None
    if sid:
        sid = str(sid)
        session_info = query_iscsi_session(sid)
        if not session_info:
            return None
        if "disks" in list(session_info.keys()):
            if not wwids:
                wwids = []
            for scsi_name in list(session_info["disks"].keys()):
                wwid = session_info["disks"][scsi_name]["wwid"]
                if wwid and wwid not in wwids:
                    wwids.append(wwid)
            return wwids
        return None

    sessions = query_all_iscsi_sessions()
    if not sessions:
        return None

    if not h_iqn and not t_iqn:
        for sid in list(sessions.keys()):
            if "disks" in list(sessions[sid].keys()):
                if not wwids:
                    wwids = []
                for scsi_name in list(sessions[sid]["disks"].keys()):
                    wwid = scsi.wwid_of_disk(scsi_name)
                    if wwid and wwid not in wwids:
                        wwids.append(wwid)
        return wwids

    if h_iqn and t_iqn:
        for sid in list(sessions.keys()):
            if (sessions[sid]["h_iqn"] == h_iqn and sessions[sid]["t_iqn"] == t_iqn) and "disks" in list(
                sessions[sid].keys(),
            ):
                if not wwids:
                    wwids = []
                for scsi_name in list(sessions[sid]["disks"].keys()):
                    wwid = scsi.wwid_of_disk(scsi_name)
                    if wwid and wwid not in wwids:
                        wwids.append(wwid)
        return wwids

    print("FAIL: scsi_wwid_of_iscsi_session() - Unsupported parameters given")
    return None


def is_iscsi_boot():  # noqa: ANN201
    iscsi_wwids = scsi_wwid_of_iscsi_session()
    if not iscsi_wwids:
        return False
    boot_dev = linux.get_boot_device()
    if not boot_dev:
        print("FAIL: is_iscsi_boot() - Could not determine boot device")
        return False

    boot_wwid = linux.get_device_wwid(boot_dev)
    if not boot_wwid:
        print(f"WARN: is_iscsi_boot() - Could not determine boot WWID for {boot_dev}")
        return False

    if boot_wwid in iscsi_wwids:
        return True

    return False


# iSCSI node ###
def node_login(options=None, target=None, portal=None, udev_wait_time=15):  # noqa: ANN001, ANN201
    """Login to an iSCSI portal, or all discovered portals
    The arguments are:
    arget:    iSCSI targets to be used, separated by space (optional)
    options:   extra parameters. eg: "-T <target> -p <portal>"
    Returns:
    True:     If iSCSI node is logged in
    False:    If some problem happened.
    """
    # Going to delete discovered target information
    print("INFO: Performing iSCSI login")
    cmd = "iscsiadm -m node -l"
    if options:
        cmd += f" {options}"

    if target:
        for target_iqn in target.split():
            cmd += f" -T {target_iqn}"

    if portal:
        cmd += f" -p {portal}"

    retcode, output = run_ret_out(cmd, return_output=True, verbose=True)
    if retcode != 0:
        print("FAIL: Could not login to iSCSI target")
        print(output)
        return False

    linux.wait_udev(udev_wait_time)
    return True


def node_logout(options=None, target=None, portal=None):  # noqa: ANN001, ANN201
    """Logout from an iSCSI node
    The arguments are:
    options:   extra parameters. eg: "-T <target> -p <portal>"
    Returns:
    True:     If iSCSI node is removed
    False:    If some problem happened.
    """
    ses_dict = query_all_iscsi_sessions()
    if not ses_dict:
        # There is no session to logout just skip
        return True
    print("INFO: Performing iSCSI logout")
    cmd = "iscsiadm -m node -u"
    if options:
        cmd += f" {options}"

    if target:
        cmd += f" -T {target}"

    if portal:
        cmd += f" -p {portal}"

    retcode, output = run_ret_out(cmd, return_output=True, verbose=True)
    if retcode != 0:
        print("FAIL: Could not logout from iSCSI target")
        print(output)
        return False
    return True


def node_delete(options=None):  # noqa: ANN001, ANN201
    """Delete node information."""
    if not options:
        print("FAIL: node_delete() - requires portal and/or target parameters")
        return False

    cmd = "iscsiadm -m node -o delete"
    if options:
        cmd += f" {options}"

    if run(cmd).returncode != 0:
        print("FAIL: Could not delete node iSCSI target")
        return False
    return True


# iSCSI iface ###
def iface_query_all_info(iface_name=None):  # noqa: ANN001, ANN201
    """Return a dict with interface names as key with detailed information of
    interface.
    """
    ifaces = [iface_name] if iface_name else get_iscsi_iface_names()

    if not ifaces:
        return None

    all_iface_dict = {}
    iface_info_regex = re.compile(r"iface\.(\S+) = (\S+)")

    for iface in ifaces:
        cmd = f"iscsiadm -m iface -I {iface}"
        retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
        if retcode != 0:
            print("FAIL: Could not delete node iSCSI target")
            continue
        details = output.split("\n")
        for info in details:
            m = iface_info_regex.match(info)
            if not m:
                continue
            if iface not in list(all_iface_dict.keys()):
                all_iface_dict[iface] = {}
            value = m.group(2)
            if value == "<empty>":
                value = None
            all_iface_dict[iface][m.group(1)] = value

    if iface_name:
        if iface_name not in list(all_iface_dict.keys()):
            return None
        return all_iface_dict[iface_name]

    return all_iface_dict


def iface_update(iface, name, value):  # noqa: ANN001, ANN201
    """Updates iSCSI interface parameter
    The arguments are:
    iface # Interface name (-I $)
    name  # Name of parameter (-n iface.$)
    value  # Value to set (-v $).

    Returns:
    True:     If value is set successfully
    False:    If some problem happened.
    """
    if not iface or not name or not value:
        print("FAIL: iface_update() - required parameters: iface, name, value")
        return False

    cmd = f"iscsiadm -m iface -I {iface} -o update -n iface.{name} -v {value}"
    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
    if retcode != 0:
        print(f"FAIL: Could not set {name} to {value} on iface {iface}")
        print(output)
        return False

    return True


def set_initiatorname(iqn: str) -> bool:
    initiatorname_file = "/etc/iscsi/initiatorname.iscsi"
    str_to_write = f"InitiatorName={iqn}"
    try:
        path = Path(initiatorname_file)
        if not path.is_file():
            linux.service_start(ISCSID_SERVICE_NAME)
        existing_name = path.read_text()
        if str_to_write != existing_name:
            with path.open(mode="w") as i:
                print(f"INFO: Writing {iqn} to {initiatorname_file}")
                i.write(str_to_write)
                linux.service_restart(ISCSID_SERVICE_NAME, verbose=True)
    except Exception as e:
        print(f"FAIL: Could not set iqn in {initiatorname_file}. Exception: {e}")
        return False
    return True


def iface_set_iqn(iqn, iface="default"):  # noqa: ANN001, ANN201
    """Set IQN in /etc/iscsi/initiatorname or for specific iface
    Return:
        True
        of
        False.
    """
    if not iqn:
        print("FAIL: iface_set_iqn() - requires iqn to be set")
        return False

    if iface == "default":
        set_initiatorname(iqn=iqn)
        return True

    iscsiadm = IscsiAdm()
    if not iscsiadm.iface_update(iface, name="initiatorname", value=iqn):
        return False

    return True


def iface_set_ip(iface, ip, mask=None, gw=None):  # noqa: ANN001, ANN201
    """Set IP information for specific iface
    Return:
        True
        of
        False.
    """
    if not iface or not ip:
        print("FAIL: iface_set_ip() - requires iface and ip parameters")
        return False

    if not iface_update(iface, "ipaddress", ip):
        return False

    if mask and not iface_update(iface, "subnet_mask", mask):
        return False

    if gw and not iface_update(iface, "gateway", gw):
        return False

    return True


def get_iscsi_iface_names():  # noqa: ANN201
    """Return a list with the name of all iSCSI interfaces on the host."""
    cmd = 'iscsiadm -m iface | cut -d " " -f 1'
    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
    if retcode != 0:
        print("FAIL: Could not read iSCSI interfaces")
        print(output)
        return None
    ifaces = output.split("\n")
    ifaces[:] = (value for value in ifaces if "iSCSI ERROR" not in value)  # bz1997710
    return ifaces


def set_iscsid_parameter(parameters: dict) -> bool:
    """Change parameter in iscsid.conf file and restarts iscsid service
    Use dictionary with parameter:value as argument.
    """
    filename = "/etc/iscsi/iscsid.conf"
    if not linux.edit_config(filename, parameters, list_values=False):
        print(f"FAIL: Unable to set iscsi parameters: {parameters}")
        return False

    if not linux.service_restart(ISCSID_SERVICE_NAME):
        print("FAIL: Unable to restart iscsid service")
        return False

    return True


def set_chap(target_user, target_pass, initiator_user=None, initiator_pass=None):  # noqa: ANN001, ANN201
    """Set CHAP authentication."""
    if not target_user or not target_pass:
        print("FAIL: set_chap() - requires username and password")
        return False

    parameters = {
        "node.session.auth.authmethod": "CHAP",
        "node.session.auth.username": target_user,
        "node.session.auth.password": target_pass,
        "discovery.sendtargets.auth.authmethod": "CHAP",  # NetApp array requires discovery authentication
        "discovery.sendtargets.auth.username": target_user,
        "discovery.sendtargets.auth.password": target_pass,
    }

    if initiator_user and initiator_pass:
        print("INFO: Setting mutual two-way CHAP authentication")
        parameters["node.session.auth.username_in"] = initiator_user
        parameters["node.session.auth.password_in"] = initiator_pass
        parameters["discovery.sendtargets.auth.username_in"] = initiator_user
        parameters["discovery.sendtargets.auth.password_in"] = initiator_pass

    if not set_iscsid_parameter(parameters):
        print("FAIL: Unable to set CHAP authentication")
        return False

    if not linux.service_restart("iscsid"):
        print("FAIL: Unable to restart iscsid service")
        return False

    print("INFO: CHAP authentication enabled")
    return True


def disable_chap():  # noqa: ANN201
    """Disable CHAP authentication in iscsid.conf and restarts the service."""
    # Removing all previously set auth parameters.
    parameters = [
        "node.session.auth.authmethod",
        "node.session.auth.username",
        "node.session.auth.password",
        "discovery.sendtargets.auth.authmethod",
        "discovery.sendtargets.auth.username",
        "discovery.sendtargets.auth.password",
        "node.session.auth.username_in",
        "node.session.auth.password_in",
        "discovery.sendtargets.auth.username_in",
        "discovery.sendtargets.auth.password_in",
    ]

    linux.remove_from_config("/etc/iscsi/iscsid.conf", parameters, warn=False)

    if not linux.service_restart("iscsid"):
        print("FAIL: Unable to restart iscsid service")
        return False

    return True


def multipath_timeo(seconds=None):  # noqa: ANN001, ANN201
    """If multipath is used for iSCSI session, session replacement
    timeout time should be decreased from default 120 seconds
    https://access.redhat.com/solutions/1171203
    multipathd service should be running when calling this
    The arguments are:
    Seconds - default 10 or number of seconds
    Returns:
    True: Successfully modified iscsid config file.
    False: There was some problem.
    """
    param = "node.session.timeo.replacement_timeout"

    if not seconds:
        seconds = 10
    seconds = str(seconds)

    if mp.is_multipathd_running():
        print("INFO: multipathd is running")
    else:
        print("FAIL: multipathd is not running")
        return False

    if not set_iscsid_parameter({param: seconds}):
        return False

    return True


def create_iscsi_iface(iface_name: str, mac: Optional[str] = None) -> bool:
    """Create a new iSCSI interface, assign mac if specified."""
    if not iface_name:
        print("FAIL: create_iscsi_iface() - requires iface name as parameter")
        return False

    if iface_name in get_iscsi_iface_names():
        print(f"INFO: iSCSI interface {iface_name} already exists")
        return True
    iscsiadm = IscsiAdm(verbose=True)
    retcode, output = iscsiadm.iface(op="new", iface=iface_name)
    if retcode != 0:
        print("FAIL: Could not create iSCSI interface")
        print(output)
        return False

    if mac is not None and not iscsiadm.iface_update(iface=iface_name, name="iface.hwaddress", value=mac):
        return False

    return True


def clone_iscsi_iface(new_iface_name, base_iface):  # noqa: ANN001, ANN201
    print(f"Cloning iface: {base_iface} to {new_iface_name}")
    if not create_iscsi_iface(new_iface_name):
        return False

    iface_info = iface_query_all_info(base_iface)
    if iface_info is None:
        print(f"FAIL: Could not query all info about iface: {base_iface}")
        return False

    if iface_info["hwaddress"] is not None and not iface_update(new_iface_name, "hwaddress", iface_info["hwaddress"]):
        return False

    if iface_info["transport_name"] is not None:  # noqa: SIM102
        if not iface_update(new_iface_name, "transport_name", iface_info["transport_name"]):
            return False

    if iface_info["initiatorname"] is not None:  # noqa: SIM102
        if not iface_update(new_iface_name, "initiatorname", iface_info["initiatorname"]):
            return False

    if iface_info["ipaddress"] is not None and not iface_update(new_iface_name, "ipaddress", iface_info["ipaddress"]):
        return False

    print(f"successfully cloned {base_iface}. new iface: {new_iface_name}")
    return True


def remove_iscsi_iface(iface_name):  # noqa: ANN001, ANN201
    if iface_name not in get_iscsi_iface_names():
        print(f"INFO: iSCSI interface '{iface_name}' does not exist")
        return False

    cmd = f"iscsiadm -m iface -o delete -I {iface_name}"
    if run(cmd, verbose=False).returncode != 0:
        print("FAIL: Could not remove iSCSI interface")
        return False

    return True


def node_iface_info(iface_name):  # noqa: ANN001, ANN201
    cmd = f"iscsiadm -m node -I {iface_name}"
    retcode, output = run_ret_out(cmd, return_output=True, verbose=False)
    if retcode != 0:
        print("FAIL: Could not get iface info!")
        print(output)
        return False

    return True


# iSCSI disks ###


def get_all_iscsi_disks():  # noqa: ANN201
    sessions = query_all_iscsi_sessions()
    disks = []
    if not sessions:
        # there is no iSCSI session
        return None

    # search for disks in each session
    for sid in list(sessions.keys()):
        ses = sessions[sid]
        if ses["disks"]:
            # disk names are key values
            disks.extend(list(ses["disks"].keys()))

    return disks


def get_session_id_from_disk(disk_name: str):  # noqa: ANN201
    sids = query_all_iscsi_sessions()
    fail_msg = f"FAIL: Could not find disk '{disk_name}' in iscsi sessions."
    if not sids:
        print(fail_msg)
        return None
    for sid in sids:
        session = query_iscsi_session(sid)
        if not session:
            print(f"FAIL: Could not query iscsi session sid: '{sid}'.")
            continue
        if disk_name in session["disks"]:
            return session["sid"]
    print(fail_msg)
    return None
