# SafetyDiag 1.3.0 (the area map): every new expression and script checked; the scripts run in the stand-in
import sys, json, re
sys.path.insert(0, '.')
import test_views as TV          # walk, expr_ok, SIG, check_source, py3_only (its own run is for the earlier views)
import harness as H
NEW = '/home/claude/out/BoothSafetyDiag_view_v1_3_0.json'
OLD = '/home/claude/out/BoothSafetyDiag_view_v1_2_1.json'
fails = 0
def expect(c, m):
    global fails
    if not c:
        fails += 1; print('  FAIL:', m)
v, o = json.load(open(NEW)), json.load(open(OLD))
items, old_items = [], []
TV.walk({'meta': {'name': 'VIEW'}, 'propConfig': v.get('propConfig', {})}, '', items); TV.walk(v['root'], '', items)
TV.walk({'meta': {'name': 'VIEW'}, 'propConfig': o.get('propConfig', {})}, '', old_items); TV.walk(o['root'], '', old_items)
oldset = set((k, c) for k, _, c, _ in old_items)
new = [i for i in items if (i[0], i[2]) not in oldset]
customs = set(v['custom'].keys())
ne = ns = 0
for kind, where, code, scope in new:
    if kind == 'expr':
        ne += 1
        expect(TV.expr_ok(code), 'unbalanced %s: %s' % (where, code))
        for m in re.findall(r'\{view\.custom\.(\w+)', code):
            expect(m in customs, '%s: view.custom.%s not declared' % (where, m))
    else:
        ns += 1
        err = TV.check_source(TV.SIG.get(kind, 'def f(self):\n') + code, where)
        expect(err is None, err)
        expect(not TV.py3_only(code), '%s py3 only' % where)
        if kind == 'event':
            expect(scope == 'G', '%s scope %s' % (where, scope))
# system.onStartup is not in TV.walk's event kinds? it is (events.system) - make sure it was found
expect(any('onStartup' in w for k, w, c, s in new), 'onStartup script found')
print('new expressions %d, new scripts %d' % (ne, ns))

def find(n, name):
    if n.get('meta', {}).get('name') == name:
        return n
    for c in n.get('children', []):
        r = find(c, name)
        if r:
            return r

class Obj(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)
def fn(code, sig):
    ns_ = {'system': H.SYSTEM}
    exec(compile(H.to_py3('def _f(%s):\n%s\n' % (sig, code)), '<v>', 'exec'), ns_)
    return ns_['_f']
class Sess(object):
    pass
sess = Obj(custom=Sess())
view = Obj(custom=Obj(showMap=False, ig='', area='COS'))
comp = Obj(view=view, session=sess)
chip = find(v['root'], 'MapBtn')
press = fn(chip['events']['dom']['onClick']['config']['script'], 'self, event')
press(comp, None)
expect(view.custom.showMap is True and sess.custom.safetyDiagMap is True, 'Map on, kept in the session')
start = fn(v['root']['events']['system']['onStartup']['config']['script'], 'self')
view2 = Obj(custom=Obj(showMap=False, ig='', area='COS'))
start(Obj(view=view2, session=sess), )
expect(view2.custom.showMap is True, 'a new popup opens with the map on')
start(Obj(view=view2, session=Obj(custom=Obj())))
expect(view2.custom.showMap is True, 'no session flag: unchanged, no error')
press(comp, None)
expect(view.custom.showMap is False and sess.custom.safetyDiagMap is False, 'Map off again')
lab = find(v['root'], 'COS_IG2_1')
tap = fn(lab['events']['dom']['onClick']['config']['script'], 'self, event')
tap(comp, None); expect(view.custom.ig == 'COS_IG2', 'outline tap picks the group')
tap(comp, None); expect(view.custom.ig == '', 'second tap shows every group')
view.custom.ig = 'COS_IG1'
ub = find(find(v['root'], 'COS Isolation Groups'), 'Unselect Group Box')
fn(ub['events']['dom']['onClick']['config']['script'], 'self, event')(comp, None)
expect(view.custom.ig == '', 'a tap outside the outlines shows every group')
tr = fn(v['propConfig']['custom.mapStyle']['binding']['transforms'][0]['code'], 'self, value, quality, timestamp')
groups = [{'id': 'COS_IG1', 'no': 'IG1', 'name': 'COS Area', 'tone': 'on', 'word': 'ENERGIZED', 'sel': False},
          {'id': 'COS_IG2', 'no': 'IG2', 'name': 'Winch ropes', 'tone': 'stp', 'word': 'STOPPED', 'sel': False}]
r = tr(None, groups, None, None)
print('   styles:', r)
expect(r['COS_IG1']['line'] == '#36664A' and r['COS_IG2']['fill'] == '#DC73233D', 'tones to colours')
groups[1]['sel'] = True
r = tr(None, groups, None, None)
expect(r['COS_IG1']['line'] == '#C5CBCC' and r['COS_IG2']['line'] == '#DC7323' and 'show every group' in r['COS_IG2']['tip'], 'picked: the others grey')
expect(tr(None, None, None, None) == {}, 'no model: no styles')
# structure: every outline names a group the safety library knows; the map paths exist in the export
H.load_all()
known = set(H.booth.safety.GROUPS.keys())
mb = find(v['root'], 'MapBox')
outl = []
for c in mb['children']:
    if c['meta']['name'].endswith('Isolation Groups'):
        for l in c['children']:
            if l['meta']['name'] != 'Unselect Group Box':
                outl.append('_'.join(l['meta']['name'].split('_')[:2]))
    else:
        e = c['children'][0]['propConfig']['props.path']['binding']['config']['expression']
        path = re.findall(r"'(Application/[^']+)'", e)[0]
        import os
        expect(os.path.exists('/home/claude/src/proj/com.inductiveautomation.perspective/views/' + path + '/view.json'), 'map view %s exists' % path)
        expect(c['props']['style'].get('pointerEvents') == 'none', 'map not tappable %s' % c['meta']['name'])
expect(set(outl) <= known, 'outline groups known: %s' % (set(outl) - known))
print('   outline groups:', sorted(set(outl)))
print('FAILS: %d' % fails)
