import sys, json
sys.path.insert(0, '.')
import harness as H, plcsim
H.load_all()
sr, bs, ah = H.booth.safetyreset, H.booth.safety, H.forensics.alarmHistory
OUT = '/home/claude/out/'
fails = 0
def expect(c, m):
    global fails
    if not c:
        fails += 1; print('  FAIL:', m)

class Obj(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)

def find(n, name):
    if n.get('meta', {}).get('name') == name:
        return n
    for c in n.get('children', []):
        r = find(c, name)
        if r:
            return r

def fn(code, sig):
    src = 'def _f(%s):\n%s\n' % (sig, code)
    ns = {'system': H.SYSTEM, 'booth': H.booth, 'forensics': H.forensics}
    exec(compile(H.to_py3(src), '<view>', 'exec'), ns)
    return ns['_f']

def event(view, comp, kind='dom', name='onClick'):
    v = json.load(open(OUT + view, encoding='utf-8'))
    n = find(v['root'], comp) if comp != 'root' else v['root']
    return fn(n['events'][kind][name]['config']['script'], 'self, event')

def mkself(custom=None, params=None, user='shane', path='/COS/Overview'):
    view = Obj(custom=Obj(**(custom or {})), params=Obj(**(params or {})))
    return Obj(view=view, session=Obj(props=Obj(auth=Obj(user=Obj(userName=user)))), page=Obj(props=Obj(path=path)),
               props=Obj(style=Obj()))

# PLC model: every IG with tags, all energized except a fault on SDB_IG2 and GRA isolated
igs = sorted([ig for ig in bs.GROUPS if bs.GROUPS[ig]['tags']])
H.CLOCK.listeners[:] = []
plc = plcsim.PLC(igs, dict(sr.RB_TAG), 0)
for ig in igs:
    plc.igs[ig].setup(en=True)
plc.igs['SDB_IG2'].setup(fault=True)
plc.igs['GRA_IG3'].setup(isolator=True)
plc.publish()
H.CLOCK.advance(1000)

print('== Alarms popup: chips and the history transform')
s = mkself(custom={'tab': 'active', 'hours': 24, 'mode': 'all', 'search': ''})
event('BoothAlarmsPopup_view_v1_1_0.json', 'TabHistory')(s, None); expect(s.view.custom.tab == 'history', 'tab')
event('BoothAlarmsPopup_view_v1_1_0.json', 'R168')(s, None); expect(s.view.custom.hours == 168, 'hours')
event('BoothAlarmsPopup_view_v1_1_0.json', 'MSafety')(s, None); expect(s.view.custom.mode == 'safety', 'mode')
event('BoothAlarmsPopup_view_v1_1_0.json', 'TabActive')(s, None); expect(s.view.custom.tab == 'active', 'tab back')
v = json.load(open(OUT + 'BoothAlarmsPopup_view_v1_1_0.json', encoding='utf-8'))
tr = fn(v['propConfig']['custom.hist']['binding']['transforms'][0]['code'], 'self, value, quality, timestamp')
r = tr(None, Obj(tab='active', f='SDB,HOG', h=24, m='all', s=''), None, None)
expect(r['rows'] == [] and r['info'] == '', 'no query on the ACTIVE tab')
ah.logAction('reset', 'SDB', 'RESET ALL IGs - Stem Debarker (HMI)', value='DONE', who='t', station='s', detail='x')
r = tr(None, Obj(tab='history', f='SDB,HOG', h=24, m='all', s=''), None, None)
print('  history:', r['info'], len(r['rows']))
expect(len(r['rows']) >= 1 and set(r['rows'][0].keys()) == set(['when', 'type', 'what', 'detail', 'state', 'lasted', 'by']),
       'rows with the table fields')
cols = [c['field'] for c in find(v['root'], 'Table')['props']['columns']]
expect(set(cols) == set(r['rows'][0].keys()), 'table columns = row fields')

print('== MessageAckButton 1.1.0')
mp = '[TL-KPPWS01-01]KPP/StemDB/Data/ScreenData/MessageAck'
H.TAGS[mp] = [False, H.CLOCK.now()]
s = mkself(custom={'path': mp, 'sentAt': 0, 'areaText': 'Debarker', 'button': '(I:70/17) Message Acknowledge'},
           params={'Area': 'SDB'}, user='kenny', path='/Debarker/Overview')
n0 = len(H.SQL_LOG)
event('BoothMessageAckButton_view_v1_1_0.json', 'root')(s, None)
expect(H.TAGS[mp][0] is False, 'released')
expect(any("'msgack'" in q for q in H.SQL_LOG[n0:]), 'msgack row written')
r = ah.rows('SDB,HOG', 24, 'safety', 'kenny')
print('  ', r['info'], [c['value'] for c in r['rows'][0].values()] if r['rows'] else None)

print('== SafetyDiag ResetBtn')
s = mkself(custom={'area': 'SDB'}, user='shane', path='/Debarker/Overview')
event('BoothSafetyDiag_view_v1_2_0.json', 'ResetBtn')(s, None)
st = sr.state('SDB')
print('  ', st['text'], '|', st['note'])
expect(plc.igs['SDB_IG2'].en and not plc.igs['SDB_IG2'].fault, 'SDB_IG2 fault reset and energized from the popup')

print('== AreaSafetyCard ResetButton + OpenButton')
s = mkself(params={'Area': 'GRA'}, user='mike', path='/Safety/SafetyPlantOverview')
event('AreaSafetyCard_view_v1_5_0.json', 'ResetButton')(s, None)
st = sr.state('GRA')
print('  ', st['text'], '|', st['note'])
expect('isolated' in st['note'] and plc.igs['GRA_IG3'].iso, 'GRA IG3 stays isolated, says so')
H._Perspective.POPUPS[:] = []
event('AreaSafetyCard_view_v1_5_0.json', 'OpenButton')(s, None)
print('  ', H._Perspective.POPUPS[-1])
expect(H._Perspective.POPUPS[-1][0][1] == 'Application/Booth/Popups/SafetyDiag' and H._Perspective.POPUPS[-1][1]['params'] == {'area': 'GRA'}, 'opens the popup on GRA')
s = mkself(params={'Area': 'DDB'})
event('AreaSafetyCard_view_v1_5_0.json', 'ResetButton')(s, None)
expect(sr.state('DDB')['text'] == 'MONITORING ONLY', 'DDB monitoring only')

v = json.load(open(OUT + 'AreaSafetyCard_view_v1_5_0.json', encoding='utf-8'))
rb = find(v['root'], 'ResetButton')
expect(rb['type'] == 'ia.container.flex' and 'component' not in rb.get('events', {}), 'card reset is a tap target (no keyboard action)')
expect('reset.cls' in rb['propConfig']['props.style.classes']['binding']['config']['expression'], 'class bound to the state')
expect(find(rb, 'Text')['propConfig']['props.style.color']['binding']['config']['expression'].count('reset.cardFg') == 1, 'label colour bound')
expect('reset' in v['custom'] and v['custom']['reset']['cls'] == 'gbtn gbtn-gold', 'custom.reset default has the glass class')

print('== SafetyPlantOverview tile')
plc.igs['COS_IG1'].setup(fault=True); plc.publish(); H.CLOCK.advance(200)
H._Perspective.POPUPS[:] = []
event('SafetyPlantOverview_view_v1_25_0.json', 'SafetyDiagButton')(mkself(), None)
print('  ', H._Perspective.POPUPS[-1][1]['params'])
expect(H._Perspective.POPUPS[-1][1]['params'] == {'area': 'COS'}, 'opens on the faulted area (COS)')
plc.igs['COS_IG1'].setup(en=True); plc.publish(); H.CLOCK.advance(200)
H._Perspective.POPUPS[:] = []
event('SafetyPlantOverview_view_v1_25_0.json', 'SafetyDiagButton')(mkself(), None)
print('  no fault ->', H._Perspective.POPUPS[-1][1]['params'])

print('== engine tick over the whole run (rows of every kind)')
H.GLOBALS.pop(ah._KEY, None)
ah.tick()
print('  ', [(r[0], r[1]) for r in [[x['type']['value'], x['state']['value']] for x in ah.rows('', 24, 'all', '')['rows'][:8]]])
plc.stop()
warns = [l for l in H.Logger.LINES if l[0] == 'WARN']
print('WARN lines:', len(warns)); [print('   ', w) for w in warns[:8]]
print('FAILS: %d' % fails)
