# Off-gateway stand-in for Ignition 8.3 / Jython 2.7: java.*, system.*, a virtual clock, a PostgreSQL-backed
# system.db (local PG 16 via psql), a fake alarm status list and the project modules loaded from source.
# Run with python3.11 (lib2to3 converts the Jython sources).
import sys, types, re, json, csv, io, subprocess, random, datetime, warnings
from zoneinfo import ZoneInfo
warnings.filterwarnings('ignore')
from lib2to3.refactor import RefactoringTool

NZ = ZoneInfo('Pacific/Auckland')

# ------------------------------------------------------------------ virtual clock
class Clock(object):
    def __init__(self, t=None):
        self.t = int(t if t is not None else datetime.datetime(2026, 10, 28, 15, 0, 0, tzinfo=NZ).timestamp() * 1000)
        self.listeners = []
        self.real = False

    def now(self):
        if self.real:
            import time
            return int(time.time() * 1000)
        return self.t

    def advance(self, ms):
        if self.real:
            import time
            time.sleep(ms / 1000.0)
            return
        end = self.t + int(ms)
        while self.t < end:
            self.t += min(10, end - self.t)
            for f in list(self.listeners):
                f(self.t)

CLOCK = Clock()

# ------------------------------------------------------------------ java stubs
class Throwable(Exception):
    pass

class System(object):
    @staticmethod
    def currentTimeMillis():
        return CLOCK.now()

class Thread(object):
    @staticmethod
    def sleep(ms):
        CLOCK.advance(int(ms))

class Date(object):
    def __init__(self, ms=None):
        self.ms = int(CLOCK.now() if ms is None else ms)
    def getTime(self):
        return self.ms
    def dt(self):
        return datetime.datetime.fromtimestamp(self.ms / 1000.0, NZ)
    def __str__(self):
        return self.dt().strftime('%a %b %d %H:%M:%S NZDT %Y')
    __repr__ = __str__
    def __eq__(self, o):
        return isinstance(o, Date) and o.ms == self.ms
    def __hash__(self):
        return hash(self.ms)

class ConcurrentHashMap(dict):
    def putIfAbsent(self, k, v):
        if k in self:
            return dict.__getitem__(self, k)
        dict.__setitem__(self, k, v)
        return None
    def replace(self, k, old, new):
        if k in self and dict.__getitem__(self, k) == old:
            dict.__setitem__(self, k, new)
            return True
        return False
    def remove(self, k, v=None):
        if k in self and (v is None or dict.__getitem__(self, k) == v):
            dict.__delitem__(self, k)
            return True
        return False
    def put(self, k, v):
        dict.__setitem__(self, k, v)

def _mod(name, **attrs):
    m = types.ModuleType(name)
    m.__dict__.update(attrs)
    sys.modules[name] = m
    return m

java = _mod('java')
java.lang = _mod('java.lang', Throwable=Throwable, System=System, Thread=Thread)
java.util = _mod('java.util', Date=Date)
java.util.concurrent = _mod('java.util.concurrent', ConcurrentHashMap=ConcurrentHashMap)

class _Prop(object):
    def __init__(self, n):
        self.name = n
    def __repr__(self):
        return self.name

class CommonAlarmProperties(object):
    AckUser = _Prop('AckUser')
    EventValue = _Prop('EventValue')
    # AckUserName deliberately missing: the code must fall back to AckUser
for _p in ['com', 'com.inductiveautomation', 'com.inductiveautomation.ignition', 'com.inductiveautomation.ignition.common',
           'com.inductiveautomation.ignition.common.alarming']:
    _mod(_p)
_mod('com.inductiveautomation.ignition.common.alarming.config', CommonAlarmProperties=CommonAlarmProperties)

# ------------------------------------------------------------------ system.*
class Logger(object):
    LINES = []
    def __init__(self, name):
        self.name = name
    def _w(self, lvl, msg):
        Logger.LINES.append((lvl, self.name, u'%s' % (msg,)))
    def info(self, m): self._w('INFO', m)
    def warn(self, m): self._w('WARN', m)
    def debug(self, m): self._w('DEBUG', m)
    def error(self, m): self._w('ERROR', m)
    def infof(self, m, *a): self._w('INFO', m % a)

class Quality(object):
    def __init__(self, good=True, name='Good'):
        self.good = good
        self.name = name if not good else 'Good'
    def isGood(self):
        return self.good
    def __str__(self):
        return self.name

class QV(object):
    def __init__(self, value, good, ts):
        self.value = value
        self.quality = Quality(good, 'Bad_NotFound')
        self.timestamp = Date(ts)

TAGS = {}            # path -> [value, ts_ms]
WRITE_LATENCY = [20, 150]
WRITE_FAIL = set()   # paths whose writes fail
WRITE_LIE = set()    # paths whose writes reach the PLC but come back Bad
WRITES = []          # (t, path, value)

class _Tag(object):
    def readBlocking(self, paths, timeout=None):
        out = []
        for p in paths:
            if p in TAGS:
                v, ts = TAGS[p]
                out.append(QV(v, True, ts))
            else:
                out.append(QV(None, False, CLOCK.now()))
        return out
    def writeBlocking(self, paths, values, timeout=None):
        out = []
        for p, v in zip(paths, values):
            lat = random.randint(*WRITE_LATENCY)
            CLOCK.advance(lat // 2)
            if p in WRITE_FAIL or p not in TAGS:
                out.append(Quality(False, 'Bad_Failure'))
            elif p in WRITE_LIE:
                TAGS[p] = [v, CLOCK.now()]
                WRITES.append((CLOCK.now(), p, v))
                out.append(Quality(False, 'Bad_Timeout'))
            else:
                TAGS[p] = [v, CLOCK.now()]
                WRITES.append((CLOCK.now(), p, v))
                out.append(Quality(True))
            CLOCK.advance(lat - lat // 2)
        return out

# ---- system.db over psql (local PG 16, database kpp)
PSQL = ['psql', '-h', '/tmp', '-p', '55432', '-U', 'postgres', '-d', 'kpp', '-X', '-v', 'ON_ERROR_STOP=1']
SQL_LOG = []

class DBError(Throwable):
    pass

def _lit(v):
    if v is None:
        return 'NULL'
    if isinstance(v, bool):
        return 'TRUE' if v else 'FALSE'
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, Date):
        return "'%s'::timestamptz" % v.dt().isoformat()
    return "'" + (u'%s' % (v,)).replace("'", "''") + "'"

def _bind(sql, args):
    args = list(args or [])
    out, i, q = [], 0, False
    for ch in sql:
        if ch == "'":
            q = not q
        if ch == '?' and not q:
            out.append(_lit(args[i]))
            i += 1
        else:
            out.append(ch)
    if i != len(args):
        raise DBError('bind: %d placeholders, %d args' % (i, len(args)))
    return ''.join(out)

DB_DOWN = [False]

def _run(sql, csvmode=False):
    SQL_LOG.append(sql)
    if DB_DOWN[0]:
        raise DBError('connection refused (test: database down)')
    cmd = PSQL + (['--csv', '-P', 'null=<<NULL>>'] if csvmode else ['-At']) + ['-c', sql]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise DBError(r.stderr.strip()[:500])
    return r.stdout

RX_TS = re.compile(r'^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d(\.\d+)?([+-]\d\d(:\d\d)?)?$')

def _conv(s):
    if s == '<<NULL>>':
        return None
    if s in ('t', 'f'):
        return s == 't'
    if re.match(r'^-?\d+$', s):
        return int(s)
    if re.match(r'^-?\d+\.\d+(e[-+]?\d+)?$', s):
        return float(s)
    if RX_TS.match(s):
        x = s
        if re.search(r'[+-]\d\d$', x):
            x += ':00'
        d = datetime.datetime.fromisoformat(x)
        if d.tzinfo is None:
            d = d.replace(tzinfo=NZ)
        return Date(int(d.timestamp() * 1000))
    return s

class DS(object):
    def __init__(self, cols, rows):
        self.cols, self.rows = cols, rows
    def getRowCount(self):
        return len(self.rows)
    def getColumnCount(self):
        return len(self.cols)
    def getValueAt(self, r, c):
        if not isinstance(c, int):
            c = self.cols.index(c)
        return self.rows[r][c]
    def __len__(self):
        return len(self.rows)

def _query(sql):
    out = _run(sql, True)
    rd = list(csv.reader(io.StringIO(out)))
    if not rd:
        return DS([], [])
    return DS(rd[0], [[_conv(x) for x in row] for row in rd[1:]])

def _update(sql):
    out = _run(sql)
    n = 0
    for line in out.strip().splitlines():
        m = re.match(r'^(INSERT \d+|UPDATE|DELETE) (\d+)$', line.strip())
        if m:
            n += int(m.group(2))
    return n

class _Db(object):
    def runUpdateQuery(self, sql, database=None, tx=None, getKey=False, skipAudit=False):
        return _update(sql)
    def runPrepUpdate(self, sql, args, database=None, tx=None, getKey=False, skipAudit=False):
        return _update(_bind(sql, args))
    def runQuery(self, sql, database=None, tx=None):
        return _query(sql)
    def runPrepQuery(self, sql, args, database=None, tx=None):
        return _query(_bind(sql, args))
    def runScalarQuery(self, sql, database=None, tx=None):
        ds = _query(sql)
        return ds.rows[0][0] if ds.rows else None
    def runNamedQuery(self, *a, **k):
        return 0

# ---- system.alarm
ALARMS = []
class _Alarm(object):
    def queryStatus(self, **kw):
        return list(ALARMS)

class EventData(object):
    def __init__(self, ms, props=None):
        self.ms, self.props = ms, props or {}
    def getTimestamp(self):
        return Date(self.ms)
    def get(self, prop):
        return self.props.get(getattr(prop, 'name', prop))

class FakeEvent(object):
    def __init__(self, eid, source, dp, label, pri='High', act=None, clr=None, ack=None, ackUser=None, value=None):
        self.eid, self.source, self.dp, self.label, self.pri = eid, source, dp, label, pri
        self.act, self.clr, self.ack, self.ackUser, self.value = act, clr, ack, ackUser, value
    def getId(self): return self.eid
    def getSource(self): return self.source
    def getDisplayPath(self): return self.dp
    def getLabel(self): return self.label
    def getName(self): return 'Alarm'
    def getPriority(self): return self.pri
    def isCleared(self): return self.clr is not None
    def isAcked(self): return self.ack is not None
    def getActiveData(self): return EventData(self.act, {'EventValue': self.value})
    def getClearedData(self): return EventData(self.clr) if self.clr is not None else None
    def getAckData(self): return EventData(self.ack, {'AckUser': self.ackUser}) if self.ack is not None else None

# ---- system.util / date
GLOBALS = {}
class _Util(object):
    globals = GLOBALS
    INLINE = True
    def getGlobals(self):
        return GLOBALS
    def getLogger(self, name):
        return Logger(name)
    def invokeAsynchronous(self, fn, *a, **k):
        if _Util.INLINE:
            fn()
        else:
            import threading
            threading.Thread(target=fn).start()
    def getProjectName(self):
        return 'MainSCADA_Timberlands'

_JTOK = re.compile(r"yyyy|yy|MMMM|MMM|MM|M|dd|d|EEEE|EEE|HH|H|mm|ss|a")
_JMAP = {'yyyy': '%Y', 'yy': '%y', 'MMMM': '%B', 'MMM': '%b', 'MM': '%m', 'M': '%-m', 'dd': '%d', 'd': '%-d', 'EEEE': '%A',
         'EEE': '%a', 'HH': '%H', 'H': '%-H', 'mm': '%M', 'ss': '%S', 'a': '%p'}

def _jfmt(fmt):
    return _JTOK.sub(lambda m: _JMAP[m.group(0)], fmt)

class _DateFns(object):
    def now(self):
        return Date()
    def fromMillis(self, ms):
        return Date(ms)
    def format(self, d, fmt):
        return d.dt().strftime(_jfmt(fmt))
    def millisBetween(self, a, b):
        return b.getTime() - a.getTime()
    def parse(self, text, fmt):
        f = _jfmt(fmt).replace('%-d', '%d').replace('%-m', '%m').replace('%-H', '%H')
        d = datetime.datetime.strptime(text, f).replace(tzinfo=NZ)
        return Date(int(d.timestamp() * 1000))
    def midnight(self, d):
        x = d.dt().replace(hour=0, minute=0, second=0, microsecond=0)
        return Date(int(x.timestamp() * 1000))

class _Perspective(object):
    POPUPS = []
    def openPopup(self, *a, **k):
        _Perspective.POPUPS.append((a, k))
    def closePopup(self, *a, **k):
        pass
    def navigate(self, *a, **k):
        _Perspective.POPUPS.append(('navigate', a, k))
    def isAuthorized(self, *a):
        return True
    def sendMessage(self, *a, **k):
        pass

class _System(object):
    tag = _Tag()
    db = _Db()
    alarm = _Alarm()
    util = _Util()
    date = _DateFns()
    perspective = _Perspective()

SYSTEM = _System()
sys.modules['system'] = SYSTEM

# ------------------------------------------------------------------ project modules from source
_RT = RefactoringTool(['lib2to3.fixes.fix_print', 'lib2to3.fixes.fix_long', 'lib2to3.fixes.fix_except',
                       'lib2to3.fixes.fix_has_key', 'lib2to3.fixes.fix_xrange', 'lib2to3.fixes.fix_basestring'])

def to_py3(src, name='<src>'):
    if not src.endswith('\n'):
        src += '\n'
    return str(_RT.refactor_string(src, name))

class NS(object):
    pass

booth = NS()
forensics = NS()
workmate = NS()
shared = NS()
_diag = NS()
_diag.log = lambda *a, **k: None
_diag.error = lambda *a, **k: None
workmate.diag = _diag

def load(path, name):
    src = open(path, encoding='utf-8').read()
    code = to_py3(src, name)
    m = types.ModuleType(name)
    m.__dict__.update(system=SYSTEM, booth=booth, forensics=forensics, workmate=workmate, shared=shared)
    exec(compile(code, path, 'exec'), m.__dict__)
    return m

import os as _os
def load_all(out=_os.environ.get('KPP_OUT', '/home/claude/out'), proj='/home/claude/src/proj/ignition/script-python'):
    booth.safety = load(proj + '/booth/safety/code.py', 'booth.safety')
    booth.safetyreset = load(out + '/booth_safetyreset_v1_0_0.py', 'booth.safetyreset')
    forensics.alarmHistory = load(out + '/forensics_alarmHistory_v1_0_0.py', 'forensics.alarmHistory')
    shared.purge = load(out + '/shared_purge_v1_2_0.py', 'shared.purge')
    return booth, forensics, shared
