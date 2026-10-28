import sys, json, re, glob
sys.path.insert(0, '.')
from py2check import check_source, py3_only
OUT = '/home/claude/out/'
SRC = '/home/claude/src/proj/com.inductiveautomation.perspective/views/'
VIEWS = {'BoothAlarmsPopup_view_v1_1_0.json': 'Application/Booth/Popups/Alarms',
         'BoothAlarmPanel_view_v1_3_0.json': 'Application/Booth/Components/AlarmPanel',
         'BoothMessageAckButton_view_v1_1_0.json': 'Application/Booth/Components/MessageAckButton',
         'BoothSafetyDiag_view_v1_2_0.json': 'Application/Booth/Popups/SafetyDiag',
         'AreaSafetyCard_view_v1_5_0.json': 'Application/Safety/Components/AreaSafetyCard',
         'SafetyPlantOverview_view_v1_25_0.json': 'Application/Safety/SafetyPlantOverview'}
fails = 0
def bad(m):
    global fails
    fails += 1
    print('  FAIL', m)

def walk(n, path, out):
    nm = n.get('meta', {}).get('name', '?')
    p = path + '/' + nm
    for kind, evs in (n.get('events') or {}).items():
        for en, ev in evs.items():
            evl = ev if isinstance(ev, list) else [ev]
            for e in evl:
                if e.get('type') == 'script':
                    out.append(('event', p + ':' + en, e['config']['script'], e.get('scope')))
    for k, pc in (n.get('propConfig') or {}).items():
        b = pc.get('binding') or {}
        for t in b.get('transforms', []) or []:
            if t.get('type') == 'script':
                out.append(('transform', p + ':' + k, t['code'], None))
        if b.get('type') == 'expr':
            out.append(('expr', p + ':' + k, b['config']['expression'], None))
        if b.get('type') == 'expr-struct':
            for sk, sv in b['config']['struct'].items():
                out.append(('expr', p + ':' + k + '.' + sk, sv, None))
        if pc.get('onChange'):
            out.append(('onchange', p + ':' + k, pc['onChange']['script'], None))
    for h in (n.get('scripts') or {}).get('messageHandlers', []) or []:
        out.append(('handler', p + ':' + h['messageType'], h['script'], None))
    for c in n.get('children', []):
        walk(c, p, out)

SIG = {'event': 'def runAction(self, event):\n', 'transform': 'def transform(self, value, quality, timestamp):\n',
       'handler': 'def onMessageReceived(self, payload):\n',
       'onchange': 'def valueChanged(self, previousValue, currentValue, origin, missedEvents):\n'}

def expr_ok(e):
    depth, q = 0, None
    for ch in e:
        if q:
            if ch == q:
                q = None
            continue
        if ch in ('"', "'"):
            q = ch
        elif ch in '({':
            depth += 1
        elif ch in ')}':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and q is None

for f, src in VIEWS.items():
    v = json.load(open(OUT + f, encoding='utf-8'))
    old = json.load(open(SRC + src + '/view.json', encoding='utf-8'))
    items = []
    # view-level propConfig (custom.*) - walk a fake node
    walk({'meta': {'name': 'VIEW'}, 'propConfig': v.get('propConfig', {})}, '', items)
    walk(v['root'], '', items)
    old_items = []
    walk({'meta': {'name': 'VIEW'}, 'propConfig': old.get('propConfig', {})}, '', old_items)
    walk(old['root'], '', old_items)
    oldset = set((k, c) for k, _, c, _ in old_items)
    new = [i for i in items if (i[0], i[2]) not in oldset]
    customs = set(v.get('custom', {}).keys())
    params = set(v.get('params', {}).keys())
    nexpr = nscript = 0
    for kind, where, code, scope in new:
        if kind == 'expr':
            nexpr += 1
            if not expr_ok(code):
                bad('%s %s unbalanced: %s' % (f, where, code))
            for m in re.findall(r'\{view\.custom\.(\w+)', code):
                if m not in customs:
                    bad('%s %s: view.custom.%s not declared' % (f, where, m))
            for m in re.findall(r'\{view\.params\.(\w+)', code):
                if m not in params:
                    bad('%s %s: view.params.%s not declared' % (f, where, m))
            if re.search('[\u2013\u2014]', code) or '\\u' in code:
                bad('%s %s: dash or \\u escape in an expression' % (f, where))
        else:
            nscript += 1
            body = SIG[kind] + code
            err = check_source(body, where)
            if err:
                bad('%s %s: %s' % (f, where, err))
            p3 = py3_only(code)
            if p3:
                bad('%s %s: py3 only %s' % (f, where, p3))
            if kind == 'event' and scope != 'G':
                bad('%s %s: scope %s' % (f, where, scope))
    s = open(OUT + f, encoding='utf-8').read()
    dash_new = len(re.findall('[\u2013\u2014]', s)) - len(re.findall('[\u2013\u2014]', open(SRC + src + '/view.json', encoding='utf-8').read()))
    if dash_new > 0:
        bad('%s: %d new em/en dashes' % (f, dash_new))
    if '/root/' in s:
        bad('%s: /root/ path' % f)
    print('%-42s new expressions %2d, new scripts %2d checked' % (f, nexpr, nscript))
print('FAILS: %d' % fails)
