# gen_views_v1_0_0.py - Adriaan - builds the six view.json files of the 28 Oct 2026 session from the 28 Oct 14:22 export.
# Refuses to overwrite a different existing output (bump the version instead); prints every changed leaf.
import json, os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gson import dumps

SRC = '/home/claude/src/proj/com.inductiveautomation.perspective/views/'
OUT = '/home/claude/out/'


def load(path):
    return json.load(open(SRC + path + '/view.json', encoding='utf-8'))


def save(obj, name):
    s = dumps(obj)
    p = OUT + name
    if os.path.exists(p) and open(p, encoding='utf-8').read() != s:
        os.remove(p)   # generator-owned output in this session (versions not yet delivered)
    open(p, 'w', encoding='utf-8').write(s)
    return p


def find(node, name):
    if node.get('meta', {}).get('name') == name:
        return node
    for c in node.get('children', []):
        r = find(c, name)
        if r:
            return r
    return None


def parent_of(node, name):
    for c in node.get('children', []):
        if c.get('meta', {}).get('name') == name:
            return node
        r = parent_of(c, name)
        if r:
            return r
    return None


def leaves(o, path=''):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(leaves(v, path + '/' + k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out.update(leaves(v, path + '[%d]' % i))
    else:
        out[path] = o
    return out


def report(name, before, after):
    a, b = leaves(before), leaves(after)
    changed = [k for k in a if k in b and a[k] != b[k]]
    added = [k for k in b if k not in a]
    removed = [k for k in a if k not in b]
    print('%s: %d changed, %d added, %d removed leaves' % (name, len(changed), len(added), len(removed)))
    for k in changed:
        print('   ~ %s: %r -> %r' % (k, str(a[k])[:70], str(b[k])[:70]))
    return changed, added, removed


def expr(e):
    return {'binding': {'config': {'expression': e}, 'type': 'expr'}}


def ev_click(script):
    return {'dom': {'onClick': {'config': {'script': script}, 'scope': 'G', 'type': 'script'}}}


def label(name, text='', style=None, pos=None, pc=None):
    d = {'meta': {'name': name}, 'position': pos or {'shrink': 0}, 'props': {'style': style or {}, 'text': text},
         'type': 'ia.display.label'}
    if pc:
        d['propConfig'] = pc
    return d


# ======================================================================= 1. Booth Alarms popup 1.1.0
def chip(name, text, sel, script):
    """light toggle chip - the SafetyDiag 'Only not OK' style"""
    return {
        'children': [label('Text', text, {'fontSize': '12px', 'fontWeight': 700, 'lineHeight': '26px', 'whiteSpace': 'nowrap'},
                           pc={'props.style.color': expr("if(%s, '#FFFFFF', '#242E30')" % sel)})],
        'events': ev_click(script),
        'meta': {'name': name},
        'position': {'shrink': 0},
        'propConfig': {'props.style.backgroundColor': expr("if(%s, '#242E30', '#FFFFFF')" % sel),
                       'props.style.borderColor': expr("if(%s, '#242E30', '#D5DADA')" % sel)},
        'props': {'alignItems': 'center', 'direction': 'row', 'justify': 'center',
                  'style': {'borderRadius': '6px', 'borderStyle': 'solid', 'borderWidth': '1px', 'boxSizing': 'border-box',
                            'cursor': 'pointer', 'height': '28px', 'overflow': 'hidden', 'padding': '0px 12px'}},
        'type': 'ia.container.flex'}


HIST_TRANSFORM = (
    "\t# HISTORY tab (1.1.0): forensics.alarmHistory.rows(filter, hours, mode, search) - read only while the tab is open,\n"
    "\t# then every 15 s and on every chip or search change. 30 days kept (shared.purge).\n"
    "\tif str(value.tab or '') != 'history':\n"
    "\t\treturn {'rows': [], 'info': '', 'infoColor': '#5F696B'}\n"
    "\ttry:\n"
    "\t\treturn forensics.alarmHistory.rows(value.f, value.h, value.m, value.s)\n"
    "\texcept:\n"
    "\t\treturn {'rows': [], 'info': 'the history needs forensics.alarmHistory 1.0.0', 'infoColor': '#C02026'}\n")


def column(field, title, width, justify='left'):
    return {'align': 'center', 'field': field,
            'header': {'align': 'center', 'justify': justify,
                       'style': {'backgroundColor': '#F6F7F7', 'color': '#5F696B', 'fontSize': '10px', 'fontWeight': 700,
                                 'letterSpacing': '0.05em'}, 'title': title},
            'justify': justify, 'sortable': False, 'style': {'fontSize': '12px'}, 'visible': True, 'width': width}


def alarms_popup():
    v = load('Application/Booth/Popups/Alarms')
    before = copy.deepcopy(v)
    v['custom'].update({'version': '1.1.0', 'tab': 'active', 'hours': 24, 'mode': 'all', 'search': '',
                        'hist': {'info': '', 'infoColor': '#5F696B', 'rows': []}})
    v['propConfig']['custom.tab'] = {'persistent': True}
    v['propConfig']['custom.hours'] = {'persistent': True}
    v['propConfig']['custom.mode'] = {'persistent': True}
    v['propConfig']['custom.search'] = {'persistent': True}
    v['propConfig']['custom.hist'] = {'binding': {'config': {'struct': {
        'f': '{view.params.filter}', 'h': '{view.custom.hours}', 'm': '{view.custom.mode}', 's': '{view.custom.search}',
        'tab': '{view.custom.tab}', 't': 'now(15000)'}, 'waitOnAll': True},
        'transforms': [{'code': HIST_TRANSFORM, 'type': 'script'}], 'type': 'expr-struct'}, 'persistent': True}
    root = v['root']
    head = find(root, 'Head')
    names = [c['meta']['name'] for c in head['children']]
    i = names.index('Badge') + 1
    tab_active = chip('TabActive', 'ACTIVE', "coalesce({view.custom.tab}, 'active') != 'history'",
                      "\tself.view.custom.tab = 'active'")
    tab_hist = chip('TabHistory', 'HISTORY - 30 DAYS', "coalesce({view.custom.tab}, 'active') = 'history'",
                    "\tself.view.custom.tab = 'history'")
    tab_active['position'] = {'shrink': 0}
    head['children'][i:i] = [tab_active, tab_hist]
    head['position'] = {'basis': '28px', 'shrink': 0}
    # the live table: only on the ACTIVE tab
    tbl = find(root, 'AlarmStatusTable')
    tbl.setdefault('propConfig', {})['position.display'] = expr("coalesce({view.custom.tab}, 'active') != 'history'")
    # the HISTORY panel
    rng = [('R1', '1 H', 1), ('R8', '8 H', 8), ('R24', '24 H', 24), ('R168', '7 DAYS', 168), ('R720', '30 DAYS', 720)]
    modes = [('MAll', 'ALL', 'all'), ('MAlarms', 'ALARMS', 'alarms'), ('MSafety', 'SAFETY + RESETS', 'safety')]
    filt = []
    filt.append(label('RangeCap', 'RANGE', {'color': '#80878A', 'fontSize': '10px', 'fontWeight': 700,
                                            'letterSpacing': '0.05em', 'lineHeight': '28px', 'whiteSpace': 'nowrap'}))
    for n, t, h in rng:
        filt.append(chip(n, t, 'coalesce({view.custom.hours}, 24) = %d' % h, '\tself.view.custom.hours = %d' % h))
    filt.append({'meta': {'name': 'Gap'}, 'position': {'basis': '10px', 'shrink': 0}, 'props': {}, 'type': 'ia.container.flex'})
    filt.append(label('ShowCap', 'SHOW', {'color': '#80878A', 'fontSize': '10px', 'fontWeight': 700,
                                          'letterSpacing': '0.05em', 'lineHeight': '28px', 'whiteSpace': 'nowrap'}))
    for n, t, m in modes:
        filt.append(chip(n, t, "coalesce({view.custom.mode}, 'all') = '%s'" % m, "\tself.view.custom.mode = '%s'" % m))
    filt.append({'meta': {'name': 'Spacer'}, 'position': {'basis': '0px', 'grow': 1, 'shrink': 1}, 'props': {},
                 'type': 'ia.container.flex'})
    filt.append({'meta': {'name': 'Search', 'tooltip': {'enabled': True, 'text': 'Search the history - alarm, device, '
                          'group or who - then Enter'}},
                 'position': {'basis': '230px', 'shrink': 0},
                 'propConfig': {'props.text': {'binding': {'config': {'bidirectional': True, 'path': 'view.custom.search'},
                                                           'type': 'property'}}},
                 'props': {'placeholder': 'Search, then Enter', 'style': {'border': '1px solid #D5DADA', 'borderRadius': '6px',
                           'boxSizing': 'border-box', 'fontSize': '12px', 'height': '28px', 'padding': '0px 8px'}, 'text': ''},
                 'type': 'ia.input.text-field'})
    filters = {'children': filt, 'meta': {'name': 'Filters'}, 'position': {'basis': '28px', 'shrink': 0},
               'props': {'alignItems': 'center', 'direction': 'row', 'style': {'gap': '6px', 'overflow': 'hidden'}},
               'type': 'ia.container.flex'}
    info = label('Info', '', {'fontSize': '11.5px', 'fontWeight': 600, 'lineHeight': '18px', 'overflow': 'hidden',
                              'textOverflow': 'ellipsis', 'whiteSpace': 'nowrap'}, {'basis': '18px', 'shrink': 0},
                 {'props.text': expr("try({view.custom.hist.info}, '')"),
                  'props.style.color': expr("try({view.custom.hist.infoColor}, '#5F696B')")})
    table = {'meta': {'name': 'Table'}, 'position': {'basis': '0px', 'grow': 1, 'shrink': 1},
             'propConfig': {'props.data': {'binding': {'config': {'path': 'view.custom.hist.rows'}, 'type': 'property'}}},
             'props': {
                 'bodyStyle': {'backgroundColor': '#FFFFFF'},
                 'cells': {'style': {'borderStyle': 'none', 'fontSize': 12, 'outlineStyle': 'none', 'padding': '0px 8px'}},
                 'columns': [column('when', 'WHEN', 126), column('type', 'TYPE', 70, 'center'), column('what', 'WHAT', 296),
                             column('detail', 'DETAIL', 272), column('state', 'STATE', 128),
                             column('lasted', 'LASTED', 80, 'center'), column('by', 'BY', 84)],
                 'emptyMessage': {'noData': {'text': 'nothing in this range'}},
                 'headerStyle': {'backgroundColor': '#F6F7F7'},
                 'pager': {'bottom': False},
                 'rows': {'height': 24, 'striped': {'enabled': False}},
                 'style': {'backgroundColor': '#FFFFFF', 'border': '1px solid #DDE1E1', 'borderRadius': '6px',
                           'fontSize': '12px', 'overflow': 'hidden'}},
             'type': 'ia.display.table'}
    hist = {'children': [filters, info, table], 'meta': {'name': 'History'},
            'position': {'basis': '0px', 'grow': 1, 'shrink': 1},
            'propConfig': {'position.display': expr("coalesce({view.custom.tab}, 'active') = 'history'")},
            'props': {'direction': 'column', 'style': {'gap': '6px', 'minHeight': '0px', 'overflow': 'hidden'}},
            'type': 'ia.container.flex'}
    root['children'].append(hist)
    report('Alarms popup', before, v)
    return save(v, 'BoothAlarmsPopup_view_v1_1_0.json')


# ======================================================================= 2. AlarmPanel 1.3.0
def alarm_panel():
    v = load('Application/Booth/Components/AlarmPanel')
    before = copy.deepcopy(v)
    v['custom']['version'] = '1.3.0'
    find(v['root'], 'All')['props']['text'] = 'All alarms + 30-day history'
    v['root']['meta']['tooltip']['text'] = 'Tap for all the alarms and the 30-day history - tap outside to close'
    report('AlarmPanel', before, v)
    return save(v, 'BoothAlarmPanel_view_v1_3_0.json')


# ======================================================================= 3. MessageAckButton 1.1.0
MSGACK_SCRIPT = (
    "\t# Engineer / Sparky only (the button is hidden for everyone else - checked again here)\n"
    "\tif not system.perspective.isAuthorized(False, ['Authenticated/Roles/Engineer', 'Authenticated/Roles/Sparky']):\n"
    "\t\treturn\n"
    "\tpath = self.view.custom.path\n"
    "\tif not path:\n"
    "\t\treturn\n"
    "\t# 1.0.1: one press per 1.5 s, and the HMI writes False 1 s after the press (the PLC clears it after 1 s\n"
    "\t# too) - otherwise the tag keeps the written True when the 1 s pulse falls between two tag group polls\n"
    "\tnow = system.date.now().getTime()\n"
    "\tif now - (self.view.custom.sentAt or 0) < 1500:\n"
    "\t\treturn\n"
    "\tself.view.custom.sentAt = now\n"
    "\tarea = self.view.params.Area\n"
    "\tuser = self.session.props.auth.user.userName\n"
    "\tq = system.tag.writeBlocking([path], [True])[0]\n"
    "\tsystem.util.getLogger('booth.msgack').info('Message acknowledge %s by %s: %s' % (area, user, q))\n"
    "\tif not q.isGood():\n"
    "\t\treturn\n"
    "\t# 1.1.0: each press goes into the HMI alarm history (forensics.alarmHistory) with who and which screen\n"
    "\tstation = str(self.page.props.path)\n"
    "\tareaText = str(self.view.custom.areaText)\n"
    "\tbutton = str(self.view.custom.button)\n"
    "\n"
    "\tdef release(path=path, area=area, user=user, station=station, areaText=areaText, button=button):\n"
    "\t\timport time\n"
    "\t\ttime.sleep(1.0)\n"
    "\t\tq2 = system.tag.writeBlocking([path], [False])[0]\n"
    "\t\tif not q2.isGood():\n"
    "\t\t\tsystem.util.getLogger('booth.msgack').warn('Message acknowledge %s release: %s' % (area, q2))\n"
    "\t\ttry:\n"
    "\t\t\tforensics.alarmHistory.logAction('msgack', area, 'MESSAGE ACK - ' + areaText, value='SENT', who=user,\n"
    "\t\t\t\tstation=station, detail=button, source=path)\n"
    "\t\texcept:\n"
    "\t\t\tpass\n"
    "\tsystem.util.invokeAsynchronous(release)")


def msgack():
    v = load('Application/Booth/Components/MessageAckButton')
    before = copy.deepcopy(v)
    v['custom']['version'] = '1.1.0'
    old = v['root']['events']['dom']['onClick']['config']['script']
    assert 'invokeAsynchronous(release)' in old
    v['root']['events']['dom']['onClick']['config']['script'] = MSGACK_SCRIPT
    report('MessageAckButton', before, v)
    return save(v, 'BoothMessageAckButton_view_v1_1_0.json')


# ======================================================================= 4. SafetyDiag popup 1.2.0
RESET_CLICK = (
    "\t# 1.2.0: RESET ALL IGs for the area on screen in one press - booth.safetyreset holds the area's HMI reset 3.5 s\n"
    "\t# (clears a safety fault), waits out the PLC's fault-reset pulse, then taps it 0.2 s (resets the groups).\n"
    "\t# It runs on the gateway, refuses a second press while one is running, and writes the HMI alarm history.\n"
    "\tbooth.safetyreset.press(self.view.custom.area, self.session.props.auth.user.userName,\n"
    "\t\t'Safety Diagnostics popup %s' % self.page.props.path)")


def safety_diag():
    v = load('Application/Booth/Popups/SafetyDiag')
    before = copy.deepcopy(v)
    v['custom']['version'] = '1.2.0'
    v['custom']['reset'] = {'area': 'SDB', 'bg': '#DEBF7A', 'border': '#D4A863', 'busy': False, 'can': True, 'fg': '#242E30',
                            'note': '', 'sub': '', 'text': 'RESET ALL IGs', 'tip': ''}
    v['propConfig']['custom.reset'] = {'binding': {'config': {'expression':
        "runScript('booth.safetyreset.state', 500, {view.custom.area})"}, 'type': 'expr'}, 'persistent': True}
    gc = find(v['root'], 'GroupsCard')
    btn = {
        'children': [
            {'meta': {'name': 'Icon'}, 'position': {'basis': '22px', 'shrink': 0},
             'propConfig': {'props.color': expr("try({view.custom.reset.fg}, '#242E30')")},
             'props': {'path': 'material/restart_alt', 'style': {'height': '22px', 'width': '22px'}},
             'type': 'ia.display.icon'},
            label('Text', 'RESET ALL IGs', {'fontSize': '14px', 'fontWeight': 800, 'letterSpacing': '0.06em',
                                            'lineHeight': '22px', 'whiteSpace': 'nowrap'}, None,
                  {'props.text': expr("if(try({view.custom.reset.text}, 'RESET ALL IGs') = 'RESET ALL IGs', "
                                      "'RESET ALL IGs - ' + {view.custom.area}, try({view.custom.reset.text}, ''))"),
                   'props.style.color': expr("try({view.custom.reset.fg}, '#242E30')")})],
        'events': ev_click(RESET_CLICK),
        'meta': {'name': 'ResetBtn', 'tooltip': {'enabled': True}},
        'position': {'basis': '46px', 'shrink': 0},
        'propConfig': {
            'meta.tooltip.text': expr("try({view.custom.reset.tip}, '')"),
            'props.style.backgroundColor': expr("try({view.custom.reset.bg}, '#DEBF7A')"),
            'props.style.borderColor': expr("try({view.custom.reset.border}, '#D4A863')"),
            'props.style.opacity': expr("if(try({view.custom.reset.can}, false) || try({view.custom.reset.busy}, false), 1, 0.6)")},
        'props': {'alignItems': 'center', 'direction': 'row', 'justify': 'center',
                  'style': {'borderRadius': '8px', 'borderStyle': 'solid', 'borderWidth': '1px', 'boxSizing': 'border-box',
                            'cursor': 'pointer', 'gap': '10px', 'overflow': 'hidden'}},
        'type': 'ia.container.flex'}
    sub = label('ResetSub', '', {'color': '#4A5558', 'fontSize': '11.5px', 'fontWeight': 600, 'lineHeight': '16px',
                                 'overflow': 'hidden', 'textOverflow': 'ellipsis', 'whiteSpace': 'nowrap'},
                {'basis': '16px', 'shrink': 0}, {'props.text': expr("try({view.custom.reset.sub}, '')")})
    note = label('ResetNote', '', {'color': '#5F696B', 'fontSize': '11px', 'fontWeight': 400, 'lineHeight': '15px',
                                   'overflow': 'hidden', 'whiteSpace': 'normal'},
                 {'basis': '30px', 'shrink': 0}, {'props.text': expr("try({view.custom.reset.note}, '')")})
    box = {'children': [btn, sub, note], 'meta': {'name': 'ResetBox'}, 'position': {'basis': '118px', 'shrink': 0},
           'props': {'direction': 'column', 'style': {'borderTop': '1px solid #DDE1E1', 'boxSizing': 'border-box', 'gap': '6px',
                                                     'overflow': 'hidden', 'paddingTop': '10px'}},
           'type': 'ia.container.flex'}
    gc['children'].append(box)
    report('SafetyDiag', before, v)
    return save(v, 'BoothSafetyDiag_view_v1_2_0.json')


# ======================================================================= 5. AreaSafetyCard 1.5.0
CARD_RESET = (
    "\t# 1.5.0: one press - booth.safetyreset holds the area's HMI reset 3.5 s (clears a safety fault), waits out the\n"
    "\t# PLC's fault-reset pulse, then taps it 0.2 s (resets the groups). Runs on the gateway; a second press while it\n"
    "\t# runs is refused. Replaces the press-and-hold button (DDB: monitoring only - press() does nothing).\n"
    "\tbooth.safetyreset.press(self.view.params.Area, self.session.props.auth.user.userName,\n"
    "\t\t'Diag view card %s' % self.page.props.path)")
CARD_OPEN = (
    "\t# 1.5.0: the Safety Diagnostics popup on this area (was: navigate to the old /Safety/<area> page)\n"
    "\tbooth.safety.openDiag(self.view.params.Area)")


def area_card():
    v = load('Application/Safety/Components/AreaSafetyCard')
    before = copy.deepcopy(v)
    assert v['root']['meta']['name'] == 'AreaSafetyCard_v1_4_1'
    assert '/root/' not in json.dumps(v)
    v['root']['meta']['name'] = 'AreaSafetyCard_v1_5_0'
    v['custom']['reset'] = {'area': 'SDB', 'bg': '#DEBF7A', 'border': '#D4A863', 'busy': False, 'can': True,
                            'cardBg': '', 'cardFg': '#F6E6B8', 'cls': 'gbtn gbtn-gold', 'fg': '#242E30', 'note': '',
                            'sub': '', 'text': 'RESET ALL IGs', 'tip': ''}
    v['propConfig']['custom.reset'] = {'binding': {'config': {'expression':
        "runScript('booth.safetyreset.state', 500, {view.params.Area})"}, 'type': 'expr'}, 'persistent': True}
    # the reset becomes a tap target (flex container + label, like OpenButton): mouse or touch only, so a keyboard
    # Enter / Space on a focused button cannot start a reset; the class is bound, so the result colours show (the
    # glass gold class sets its background and colour !important - it is on only while idle)
    footer = parent_of(v['root'], 'ResetButton')
    names = [c['meta']['name'] for c in footer['children']]
    i = names.index('ResetButton')
    old_rb = footer['children'][i]
    assert old_rb['type'] == 'ia.input.button' and old_rb['props']['style']['classes'] == 'gbtn gbtn-gold'
    footer['children'][i] = {
        'children': [label('Text', 'RESET ALL IGs', {'fontSize': '11px', 'fontWeight': 700, 'letterSpacing': '0.5px',
                                                     'lineHeight': '32px', 'overflow': 'hidden', 'textAlign': 'center',
                                                     'textOverflow': 'ellipsis', 'whiteSpace': 'nowrap'},
                           {'basis': '0px', 'grow': 1, 'shrink': 1},
                           {'props.text': expr("try({view.custom.reset.text}, 'RESET ALL IGs')"),
                            'props.style.color': expr("try({view.custom.reset.cardFg}, '#F6E6B8')")})],
        'events': ev_click(CARD_RESET),
        'meta': {'name': 'ResetButton', 'tooltip': {'enabled': True}},
        'position': dict(old_rb['position']),
        'propConfig': {
            'meta.tooltip.text': expr("try({view.custom.reset.tip}, '')"),
            'props.style.backgroundColor': expr("try({view.custom.reset.cardBg}, '')"),
            'props.style.classes': expr("try({view.custom.reset.cls}, 'gbtn gbtn-gold')"),
            'props.style.cursor': expr("if(try({view.custom.reset.can}, false), 'pointer', 'default')")},
        'props': {'alignItems': 'center', 'direction': 'row', 'justify': 'center',
                  'style': {'borderColor': 'rgba(255,255,255,0.14)', 'borderRadius': '12px', 'borderStyle': 'solid',
                            'borderWidth': '1px', 'boxSizing': 'border-box', 'classes': 'gbtn gbtn-gold',
                            'cursor': 'pointer', 'height': '34px', 'overflow': 'hidden', 'padding': '0px 8px'}},
        'type': 'ia.container.flex'}
    ob = find(v['root'], 'OpenButton')
    ob['events'] = ev_click(CARD_OPEN)
    ob['meta']['tooltip'] = {'enabled': True}
    ob.setdefault('propConfig', {})['meta.tooltip.text'] = expr("'Safety Diagnostics - ' + {view.params.Area}")
    report('AreaSafetyCard', before, v)
    return save(v, 'AreaSafetyCard_view_v1_5_0.json')


# ======================================================================= 6. SafetyPlantOverview 1.25.0
OVERVIEW_OPEN = (
    "\t# 1.25.0: the Safety Diagnostics popup - on the area that needs attention most (a fault, then needs reset or\n"
    "\t# stopped, then isolated), else SDB. The popup's tabs reach every area.\n"
    "\tarea = 'SDB'\n"
    "\ttry:\n"
    "\t\trank = {'flt': 4, 'rst': 3, 'stp': 3, 'act': 2}\n"
    "\t\tbest, top = 'SDB', 0\n"
    "\t\tfor t in booth.safety.model('SDB').get('tabs', []):\n"
    "\t\t\tr = rank.get(t.get('tone'), 0)\n"
    "\t\t\tif r > top:\n"
    "\t\t\t\tbest, top = t.get('code', 'SDB'), r\n"
    "\t\tarea = best\n"
    "\texcept:\n"
    "\t\tpass\n"
    "\tbooth.safety.openDiag(area)")


def overview():
    v = load('Application/Safety/SafetyPlantOverview')
    before = copy.deepcopy(v)
    assert v['root']['meta']['name'] == 'SafetyPlantOverview_v1_24_1'
    assert '/root/' not in json.dumps(v)
    v['root']['meta']['name'] = 'SafetyPlantOverview_v1_25_0'
    row = find(v['root'], 'CardsRow')
    gold = '#DEBF7A'
    tile = {
        'children': [
            {'meta': {'name': 'icon'}, 'position': {'basis': '34px', 'shrink': 0},
             'props': {'color': gold, 'path': 'material/health_and_safety', 'style': {'height': '34px', 'width': '34px'}},
             'type': 'ia.display.icon'},
            {'meta': {'name': 'value'}, 'position': {'shrink': 0},
             'props': {'text': 'SAFETY', 'textStyle': {'color': gold, 'fontSize': 15, 'fontWeight': '800'}},
             'type': 'ia.display.label'},
            {'meta': {'name': 'caption'}, 'position': {'shrink': 0},
             'props': {'text': 'DIAGNOSTICS', 'textStyle': {'color': '#C2C7C7', 'fontSize': 8, 'fontWeight': '600',
                                                            'letterSpacing': '1px'}},
             'type': 'ia.display.label'},
            {'meta': {'name': 'hint'}, 'position': {'shrink': 0},
             'props': {'style': {'marginTop': '6px', 'textAlign': 'center', 'whiteSpace': 'normal'},
                       'text': 'groups, devices, log, one-press reset',
                       'textStyle': {'color': '#80878A', 'fontSize': 10, 'textAlign': 'center'}},
             'type': 'ia.display.label'}],
        'events': ev_click(OVERVIEW_OPEN),
        'meta': {'name': 'SafetyDiagButton', 'tooltip': {'enabled': True, 'text': 'Safety Diagnostics - every area: '
                 'isolation groups, devices, isolation log and RESET ALL IGs'}},
        'position': {'basis': '118px', 'shrink': 0},
        'props': {'alignItems': 'center', 'direction': 'column', 'justify': 'center',
                  'style': {'backgroundColor': 'rgba(222,191,122,0.12)', 'borderBottomColor': gold, 'borderBottomStyle': 'solid',
                            'borderBottomWidth': 1, 'borderLeftColor': gold, 'borderLeftStyle': 'solid', 'borderLeftWidth': 1,
                            'borderRadius': '10px', 'borderRightColor': gold, 'borderRightStyle': 'solid',
                            'borderRightWidth': 1, 'borderTopColor': gold, 'borderTopStyle': 'solid', 'borderTopWidth': 1,
                            'classes': 'stem-eng-chip', 'cursor': 'pointer', 'gap': '2px', 'overflow': 'hidden',
                            'padding': '10px 8px 10px 8px'}},
        'type': 'ia.container.flex'}
    row['children'].append(tile)
    report('SafetyPlantOverview', before, v)
    return save(v, 'SafetyPlantOverview_view_v1_25_0.json')


if __name__ == '__main__':
    for f in (alarms_popup, alarm_panel, msgack, safety_diag, area_card, overview):
        print('  ->', f())
