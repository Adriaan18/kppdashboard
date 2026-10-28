# gen_safetydiag_map_v1_0_1.py - Adriaan - SafetyDiag popup 1.3.1: the picked group stands out on the map - bright fill, a
# 4 px line and a glow in its state colour, drawn on top, its 'IG n' larger; the others grey (1.3.0 picked = the plain
# state colours, too faint on the grey map - Adriaan 20:22).
# 1.3.0: the area map in the popup (28 Oct 2026, crews missed
# the safety map after the Diag cards stopped opening the old Safety pages). Built from SafetyDiag 1.2.1 (installed) and the
# map part of Application/Safety/Zone (the attached Safety export): per area its map view with the safety layer only
# (Application/<area folder>/<AREA> Map, the Zone's own params) and the Zone's isolation-group outlines - redrawn in the
# popup's colours, live from the popup's own model, tap to pick the group.
import json, os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gson import dumps

BASE = '/home/claude/out/BoothSafetyDiag_view_v1_2_1.json'
ZONE = ('/tmp/claude-0/-home-claude/093166e4-91e7-5882-8ec5-a1a53ea7875b/scratchpad/safetyzip/x/'
        'com.inductiveautomation.perspective/views/Application/Safety/Zone/view.json')
OUT = '/home/claude/out/BoothSafetyDiag_view_v1_3_1.json'
AREAS = ['SDB', 'GRA', 'COS', 'TNB', 'CHP', 'HOG']
# the Zone's map box at its default size (1920 x 1014): 1420 wide (the 500 px status column off), 45 % of the height
# tall; Chippers' map is the tall one - its outlines are drawn for 1.65:1
ASPECT = {'SDB': '1420:456', 'GRA': '1420:456', 'COS': '1420:456', 'TNB': '1420:456', 'HOG': '1420:456', 'CHP': '1420:861'}
# the map box's own size in the 1002 x 446-482 px device panel, at the Zone's ratio and like the Zone's map box with no
# aspect ratio of its own, so the map and the outlines sit as they did there: wide maps 100 % x 322 px, Chippers 693 x 420
BOX_H = "if({view.custom.area} = 'CHP', '420px', '322px')"
BOX_W = "if({view.custom.area} = 'CHP', '693px', '100%')"
SHOWN = "coalesce({view.custom.showMap}, false) && {view.custom.area} != 'DDB'"


def find(node, name):
    if node.get('meta', {}).get('name') == name:
        return node
    for c in node.get('children', []):
        r = find(c, name)
        if r:
            return r
    return None


def expr(e):
    return {'binding': {'config': {'expression': e}, 'type': 'expr'}}


def click(script):
    return {'dom': {'onClick': {'config': {'script': script}, 'scope': 'G', 'type': 'script'}}}


v = json.load(open(BASE, encoding='utf-8'))
z = json.load(open(ZONE, encoding='utf-8'))
assert v['custom']['version'] == '1.2.1'
zmap = find(z['root'], 'Map')

# ---------------------------------------------------------------- view custom props
v['custom']['version'] = '1.3.1'
v['custom']['showMap'] = False
v['custom']['mapStyle'] = {}
v['propConfig']['custom.showMap'] = {'persistent': True}
v['propConfig']['custom.mapStyle'] = {'binding': {'config': {'path': 'view.custom.model.groups'}, 'transforms': [{'code': (
    "\t# 1.3.1: the map outlines' look per isolation group - from the popup's own model (its state and whether it is\n"
    "\t# picked), no tag reads of its own. Picked: a bright fill, a 4 px line and a glow in its state colour, drawn on top,\n"
    "\t# its 'IG n' larger; the other groups grey while one is picked; none picked: every group in its state colour\n"
    "\tFILL = {'on': '#36664A1F', 'act': '#F2C2004D', 'rst': '#1838D62E', 'stp': '#DC73233D', 'flt': '#C020264D'}\n"
    "\tLINE = {'on': '#36664A', 'act': '#B08D00', 'rst': '#1838D6', 'stp': '#DC7323', 'flt': '#C02026'}\n"
    "\tPICK = {'on': ('#22C55E4D', '#16A34A', '#0B6B32', '34,197,94'), 'act': ('#FACC1566', '#D9A400', '#7A5A00', '250,204,21'),\n"
    "\t\t'rst': ('#3B82F64D', '#2563EB', '#1838D6', '59,130,246'), 'stp': ('#F973164D', '#EA6A0C', '#A84500', '249,115,22'),\n"
    "\t\t'flt': ('#EF444452', '#DC2626', '#A3121A', '239,68,68')}\n"
    "\tout = {}\n"
    "\ttry:\n"
    "\t\tgs = list(value or [])\n"
    "\t\tpicked = len([g for g in gs if g['sel']]) > 0\n"
    "\t\tfor g in gs:\n"
    "\t\t\tt = str(g['tone'])\n"
    "\t\t\ttip = '%s %s - %s - tap to %s' % (g['no'], g['name'], g['word'], 'show every group' if g['sel'] else 'pick it')\n"
    "\t\t\tif g['sel']:\n"
    "\t\t\t\tf, l, x, rgb = PICK.get(t, ('#80878A40', '#4A5558', '#242E30', '74,85,88'))\n"
    "\t\t\t\tst = {'fill': f, 'line': l, 'text': x, 'width': '4px', 'glow': '0 0 18px 6px rgba(%s,0.55)' % rgb, 'z': 5,\n"
    "\t\t\t\t\t'fs': '13px'}\n"
    "\t\t\telif picked:\n"
    "\t\t\t\tst = {'fill': '#00000005', 'line': '#D5DADA', 'text': '#B9C0C1', 'width': '2px', 'glow': 'none', 'z': 1,\n"
    "\t\t\t\t\t'fs': '11px'}\n"
    "\t\t\telse:\n"
    "\t\t\t\tst = {'fill': FILL.get(t, '#0000000F'), 'line': LINE.get(t, '#80878A'), 'text': LINE.get(t, '#80878A'),\n"
    "\t\t\t\t\t'width': '2px', 'glow': 'none', 'z': 1, 'fs': '11px'}\n"
    "\t\t\tst['tip'] = tip\n"
    "\t\t\tout[str(g['id'])] = st\n"
    "\texcept:\n"
    "\t\tpass\n"
    "\treturn out"), 'type': 'script'}], 'type': 'property'}, 'persistent': True}
# the map stays on for the session once chosen
v['root'].setdefault('events', {})['system'] = {'onStartup': {'config': {'script': (
    "\t# 1.3.0: the map on or off as last chosen in this session\n"
    "\ttry:\n"
    "\t\tself.view.custom.showMap = bool(self.session.custom.safetyDiagMap)\n"
    "\texcept:\n"
    "\t\tpass")}, 'scope': 'G', 'type': 'script'}}

# ---------------------------------------------------------------- the Map chip in the devices head
dc = find(v['root'], 'DevicesCard')
head = find(dc, 'Head')
only = find(head, 'OnlyBad')
chip = copy.deepcopy(only)
chip['meta']['name'] = 'MapBtn'
chip['meta']['tooltip'] = {'enabled': True, 'text': 'The area map: live safety devices and the isolation groups - tap a group to pick it'}
chip['children'][0]['props']['text'] = 'Map'
for k in ('props.style.color',):
    chip['children'][0]['propConfig'][k] = expr("if(coalesce({view.custom.showMap}, false), '#FFFFFF', '#242E30')")
chip['propConfig'] = {
    'position.display': expr("{view.custom.area} != 'DDB'"),
    'props.style.backgroundColor': expr("if(coalesce({view.custom.showMap}, false), '#242E30', '#FFFFFF')"),
    'props.style.borderColor': expr("if(coalesce({view.custom.showMap}, false), '#242E30', '#D5DADA')")}
chip['events'] = click(
    "\t# 1.3.0: the area map in place of the device list; kept for the session\n"
    "\ton = not bool(self.view.custom.showMap)\n"
    "\tself.view.custom.showMap = on\n"
    "\ttry:\n"
    "\t\tself.session.custom.safetyDiagMap = on\n"
    "\texcept:\n"
    "\t\tpass")
head['children'].append(chip)

# ---------------------------------------------------------------- the device list gives way to the map
sections = find(dc, 'Sections')
sections.setdefault('propConfig', {})['position.display'] = expr('!(' + SHOWN + ')')

# ---------------------------------------------------------------- the map panel
mapbox = {'children': [], 'meta': {'name': 'MapBox'}, 'position': {'basis': '322px', 'grow': 0, 'shrink': 0},
          'propConfig': {'position.basis': expr(BOX_H), 'props.style.width': expr(BOX_W)},
          'props': {'mode': 'percent',
                    'style': {'backgroundColor': '#FAFAFA', 'border': '1px solid #DDE1E1', 'borderRadius': '6px',
                              'boxSizing': 'border-box', 'overflow': 'hidden'}},
          'type': 'ia.container.coord'}
n_outline = 0
for zc in zmap['children']:
    name = zc['meta']['name']
    area = name[:3]
    assert area in AREAS, name
    c = copy.deepcopy(zc)
    shown = "{view.custom.area} = '%s' && coalesce({view.custom.showMap}, false)" % area
    c['propConfig'] = {'meta.visible': expr(shown)}
    if name.endswith('Components'):
        # the map itself: safety layer only (the Zone's params), loaded only while shown, nothing on it taps through
        c['props'].setdefault('style', {})['pointerEvents'] = 'none'
        ev = c['children'][0]
        assert ev['type'] == 'ia.display.view' and len(c['children']) == 1
        path = ev['props']['path']
        ev['propConfig'] = {'props.path': expr("if(%s, '%s', '')" % (shown, path.replace("'", "\\'")))}
        ev['props']['path'] = ''
    else:
        groups_seen = set()
        for lab in c['children']:
            lab.pop('custom', None)
            lab.pop('propConfig', None)
            nm = lab['meta']['name']
            st = lab.setdefault('props', {}).setdefault('style', {})
            for k in list(st.keys()):
                if k == 'backgroundColor' or k.endswith('Color'):
                    del st[k]
                elif k.endswith('Width'):
                    del st[k]            # one bound borderWidth (sides with no border style stay open)
            if nm == 'Unselect Group Box':
                lab['events'] = click("\t# 1.3.0: a tap on the map outside the groups shows every device again\n"
                                      "\tself.view.custom.ig = ''")
                lab['props'].pop('text', None)
                continue
            ig = '_'.join(nm.split('_')[:2])
            no = ig.split('_IG')[1]
            ms = '{view.custom.mapStyle.%s' % ig
            lab['propConfig'] = {
                'props.style.backgroundColor': expr("try(%s.fill}, '#0000000F')" % ms),
                'props.style.borderColor': expr("try(%s.line}, '#80878A')" % ms),
                'props.style.borderWidth': expr("try(%s.width}, '2px')" % ms),
                'props.style.boxShadow': expr("try(%s.glow}, 'none')" % ms),
                'props.style.zIndex': expr("try(%s.z}, 1)" % ms)}
            st['cursor'] = 'pointer'
            lab['events'] = click("\t# 1.3.0: tap a group's outline to pick it (again to show every device)\n"
                                  "\tself.view.custom.ig = '' if self.view.custom.ig == '%s' else '%s'" % (ig, ig))
            lab['meta']['tooltip'] = {'enabled': True}
            lab['propConfig']['meta.tooltip.text'] = expr("try(%s.tip}, '%s IG%s')" % (ms, area, no))
            if ig not in groups_seen:
                groups_seen.add(ig)
                lab['props']['text'] = 'IG' + no
                lab['props']['alignVertical'] = 'top'
                lab['props']['textStyle'] = {'fontSize': '11px', 'fontWeight': 800, 'letterSpacing': '0.04em',
                                             'paddingLeft': '5px', 'paddingTop': '2px', 'textAlign': 'left',
                                             'whiteSpace': 'nowrap'}
                lab['propConfig']['props.textStyle.color'] = expr("try(%s.text}, '#80878A')" % ms)
                lab['propConfig']['props.textStyle.fontSize'] = expr("try(%s.fs}, '11px')" % ms)
            else:
                lab['props'].pop('text', None)
                lab['props'].pop('textStyle', None)
            n_outline += 1
    mapbox['children'].append(c)

hint = {'meta': {'name': 'MapHint'}, 'position': {'basis': '16px', 'shrink': 0},
        'propConfig': {'props.text': expr(
            "if(len(coalesce({view.custom.ig}, '')) > 0, 'Map - ' + {view.custom.area} + ' ' + "
            "replace({view.custom.ig}, {view.custom.area} + '_', '') + ' picked - tap it again or outside the outlines for "
            "every group; Map off for its device list', 'Map - live safety devices (gates GS, E-stops ES, pull cords PR, "
            "isolators IS, standstill SS) and the isolation groups - tap a group to pick it')")},
        'props': {'style': {'color': '#5F696B', 'fontSize': '11.5px', 'fontWeight': 600, 'lineHeight': '16px',
                            'overflow': 'hidden', 'textOverflow': 'ellipsis', 'whiteSpace': 'nowrap'}, 'text': ''},
        'type': 'ia.display.label'}
panel = {'children': [hint, mapbox], 'meta': {'name': 'MapPanel'}, 'position': {'basis': '0px', 'grow': 1, 'shrink': 1},
         'propConfig': {'position.display': expr(SHOWN)},
         'props': {'alignItems': 'center', 'direction': 'column', 'style': {'gap': '6px', 'minHeight': '0px', 'overflow': 'hidden'}},
         'type': 'ia.container.flex'}
hint['props']['style']['width'] = '100%'
names = [c['meta']['name'] for c in dc['children']]
dc['children'].insert(names.index('Sections') + 1, panel)

s = dumps(v)
assert '\u2013' not in s and '\u2014' not in s
if os.path.exists(OUT) and open(OUT, encoding='utf-8').read() != s:
    os.remove(OUT)
open(OUT, 'w', encoding='utf-8').write(s)
print('written', OUT, len(s), 'outlines', n_outline, 'map containers', len(mapbox['children']))
