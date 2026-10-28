# Scan-level model of the safety PLC's isolation-group reset logic, parsed from KPP_COS_V20T.L5K:
#   GroupResetONS = falling edge of any reset button (ONS on XIO, storage bits as in the PLC - shared bits included)
#                   AND NOT FaultResetPulse
#   fault reset   = any reset held -> TON tFaultResetTON (3000) -> ONS -> TOF tFaultResetPulse (PRE from the tags)
#   GroupEn       = ((GroupResetONS AND AllFeedbacksOk) OR GroupEn) AND AllInputsOk AND channels OK AND NOT fault
#   GroupFault    = OTU on FaultResetPulse, then OTL while a channel or device fault is there (device faults latch
#                   like a DCS until the fault reset pulse with the cause gone)
# Safety task 50 ms (standard -> safety map copied at its start); standard routine _099: an HMI reset held 5 s is cleared.
import re
import harness as H

L5K = '/home/claude/src/plc/KPP_COS_V20T.L5K'
_txt = None

def _l5k():
    global _txt
    if _txt is None:
        _txt = open(L5K, encoding='utf-8-sig').read()
    return _txt

_PARSED = {}

def parse_ig(ig):
    if ig in _PARSED:
        return _PARSED[ig]
    _PARSED[ig] = _parse_ig(ig)
    return _PARSED[ig]

def _parse_ig(ig):
    t = _l5k()
    m = re.search(r'N: \[([^\n]*?)\]XIO\(%s\.FaultResetPulse\)OTE\(%s\.GroupResetONS\);' % (ig, ig), t)
    branches = re.findall(r'XIO\((\w+)_SafetyMap\.(\w+)\) ONS\(([^)]+)\)', m.group(1))
    reset = [(b[1], b[2]) for b in branches]
    m2 = re.search(r'N: \[\[([^\n]*?)\] \[TON\(%s\.tFaultResetTON' % ig, t)
    fault = [b[1] for b in re.findall(r'XIC\((\w+)_SafetyMap\.(\w+)\)', m2.group(1))]
    m3 = re.search(r'\b%s : udt_Safety_IsolationGroup \((?:Description := "[^"]*",\s*)?Usage := Public\) := \[0,\[\d+,(\d+),\d+\],'
                   r'\[\d+,(\d+),\d+\],0,\[\d+,(\d+),\d+\],\[\d+,(\d+),\d+\]' % ig, t)
    ton, pulse = int(m3.group(3)), int(m3.group(4))
    return reset, fault, ton, pulse


class IG(object):
    def __init__(self, ig):
        self.name = ig
        self.reset, self.faultrbs, self.ton_pre, self.pulse_pre = parse_ig(ig)
        self.stor = {}                       # ONS storage by operand (a shared operand is one bit)
        for rb, key in self.reset:
            self.stor[key] = True            # reset buttons idle: XIO true, storage set
        self.ton_acc, self.ton_dn, self.ons2 = 0, False, False
        self.tof_dn, self.tof_acc = False, 0
        self.frp = False
        self.reset_ons = False
        self.resets = 0                      # scans with GroupResetONS true
        # plant conditions
        self.estops = True
        self.gates = True
        self.isolator = False
        self.feedbacks = True
        self.in_ok = True
        self.out_ok = True
        self.dev_cause = False
        self.dev_latched = False
        # state
        self.en = False
        self.fault = False
        self.off_acc = 500
        self.iso = False

    def setup(self, en=False, fault=False, cause=False, isolator=False, gates=True):
        self.en, self.fault, self.dev_cause, self.isolator, self.gates = en, fault, cause, isolator, gates
        self.dev_latched = fault or cause
        self.off_acc = 0 if en else 500

    def scan(self, safe):
        outs = []
        for rb, key in self.reset:
            in_ = not safe.get(rb, False)
            outs.append(in_ and not self.stor[key])
            self.stor[key] = in_
        self.reset_ons = any(outs) and not self.frp
        if self.reset_ons:
            self.resets += 1
        anyrb = any(safe.get(rb, False) for rb in self.faultrbs)
        if anyrb:
            self.ton_acc = min(self.ton_acc + 50, self.ton_pre)
            self.ton_dn = self.ton_acc >= self.ton_pre
            ons_in = self.ton_dn
        else:
            self.ton_acc, self.ton_dn, ons_in = 0, False, False
        tof_in = ons_in and not self.ons2
        self.ons2 = ons_in
        if tof_in:
            self.tof_dn, self.tof_acc = True, 0
        elif self.tof_dn:
            self.tof_acc += 50
            if self.tof_acc >= self.pulse_pre:
                self.tof_dn = False
        self.frp = self.tof_dn
        # device faults (DCS-style): reset by the group fault reset pulse once the cause is gone
        if self.frp and not self.dev_cause:
            self.dev_latched = False
        if self.dev_cause:
            self.dev_latched = True
        all_inputs = self.estops and self.gates and not self.isolator
        self.en = ((self.reset_ons and self.feedbacks) or self.en) and all_inputs and self.out_ok and self.in_ok and not self.fault
        if self.frp:
            self.fault = False
        if not (self.in_ok and self.out_ok and not self.dev_latched):
            self.fault = True
        self.off_acc = 0 if self.en else min(self.off_acc + 50, 500)
        self.iso = self.isolator and self.off_acc >= 500 and not self.fault and self.in_ok and self.out_ok and self.feedbacks


class PLC(object):
    def __init__(self, igs, rb_tags, phase=None):
        import random
        self.igs = dict((ig, IG(ig)) for ig in igs)
        self.rb_tags = rb_tags                 # area -> Ignition tag path of <X>_HMI_RB
        self.safe = {}
        self.timeout_acc = dict((a, 0) for a in rb_tags)
        self.timeouts = 0
        self.next_safety = H.CLOCK.now() + (phase if phase is not None else random.randint(0, 49))
        self.trace = []
        for a, p in rb_tags.items():
            H.TAGS[p] = [False, H.CLOCK.now()]
        self.publish()
        H.CLOCK.listeners.append(self.tick)

    def stop(self):
        if self.tick in H.CLOCK.listeners:
            H.CLOCK.listeners.remove(self.tick)

    def tick(self, t):
        # standard task: _099_HMI_RB_Timeout (5 s)
        for a, p in self.rb_tags.items():
            if H.TAGS[p][0]:
                self.timeout_acc[a] += 10
                if self.timeout_acc[a] >= 5000:
                    H.TAGS[p] = [False, t]
                    self.timeouts += 1
            else:
                self.timeout_acc[a] = 0
        if t >= self.next_safety:
            self.next_safety += 50
            for a, p in self.rb_tags.items():
                self.safe[a + '_HMI_RB'] = bool(H.TAGS[p][0])
            for g in self.igs.values():
                g.scan(self.safe)
            self.publish()

    def publish(self):
        bs = H.booth.safety
        t = H.CLOCK.now()
        for name, g in self.igs.items():
            if name not in bs.GROUPS or not bs.GROUPS[name]['tags']:
                continue
            flags = {'GroupEn': g.en, 'GroupIsolated': g.iso, 'GroupFaultActive': g.fault,
                     'AllInputsOk': g.estops and g.gates and not g.isolator, 'AllIsolatorsOk': not g.isolator,
                     'AllInputStatusOk': g.in_ok, 'AllOutputStatusOk': g.out_ok, 'AllDevicesOk': not g.dev_latched,
                     'AllEstopsOk': g.estops, 'AllGatesOk': g.gates, 'AllStandstillsOk': True,
                     'AllSafetyRelaysOk': True, 'AllFeedbacksOk': g.feedbacks}
            for f, v in flags.items():
                p = bs.groupPath(name, 'GroupTags/' + f)
                old = H.TAGS.get(p)
                if old is None or old[0] != v:
                    H.TAGS[p] = [v, t]
