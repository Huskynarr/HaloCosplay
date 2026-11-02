#!/usr/bin/env python3
"""Map selected equipment to accessible mounting zones and separate circuits."""
from copy import deepcopy
import json
from pathlib import Path

try:
    from . import suit_engineering, suit_thermal
except ImportError:
    import suit_engineering, suit_thermal

OPTIONS = {
    'helmet_light': ('none', 'pixel', 'power-rgb'),
    'nozzle_light': ('none', 'power-rgb'),
    'helmet_ventilation': ('passive', 'dual-40mm'),
    'torso_ventilation': ('passive', 'dual-60mm'),
    'nozzle_air': ('none', 'dry-dual-40mm'),
    'hud': ('none', 'combiner'),
    'camera': ('none', 'usb-uvc', 'csi-local'),
    'audio': ('none', 'chest-speaker'),
}


def configure(fit, config_path=None):
    build = fit['build']
    features = build['features']
    cfg = {'helmet_light': 'power-rgb' if features['lighting'] else 'none',
           'nozzle_light': 'power-rgb' if features['lighting'] and build['fog_system'] != 'none' else 'none',
           'helmet_ventilation': 'dual-40mm', 'torso_ventilation': 'dual-60mm',
           'nozzle_air': 'dry-dual-40mm' if build['fog_system'] != 'none' else 'none',
           'hud': 'combiner' if features['hud'] else 'none', 'camera': 'none',
           'audio': 'chest-speaker' if features['audio'] else 'none'}
    if config_path is not None:
        custom = json.loads(Path(config_path).read_text(encoding='utf-8'))
        if not isinstance(custom, dict) or set(custom) - set(OPTIONS):
            raise ValueError('Unbekannte Integrationsoption')
        cfg.update(custom)
    for key, choices in OPTIONS.items():
        if not isinstance(cfg[key], str) or cfg[key] not in choices:
            raise ValueError('Ungueltige Integrationsoption: ' + key)
    for key, feature in (('helmet_light', 'lighting'), ('nozzle_light', 'lighting'), ('hud', 'hud'), ('audio', 'audio')):
        if cfg[key] != 'none' and not features[feature]:
            raise ValueError(key + ': zugehoerige Ausstattung im Profil ist ausgeschaltet')
    return cfg


def plan(fit, cfg):
    modules = []
    def add(ident, label, zone, circuit, access, quantity=1):
        modules.append({'id': ident, 'label': label, 'quantity': quantity, 'mounting_zone': zone,
                        'circuit': circuit, 'access': access, 'measured_mass_g': None,
                        'envelope_mm': {'width': None, 'height': None, 'depth': None},
                        'connector': None, 'installed_and_tested': False})
    if cfg['helmet_ventilation'] != 'passive':
        add('HELM_FANS', 'Helmluefter und Visierkanaele', 'Kiefer-/Wangenpods, Auslass oben hinten',
            'COMFORT_5V', 'Helm abnehmbar, Schutzgitter und herausnehmbare Kanaele', 2)
    if cfg['torso_ventilation'] != 'passive':
        add('TORSO_FANS', 'Torsoluefter', 'Untere Flanken, getrennt von Akkufach und Nebelauslass',
            'COMFORT_5V', 'Seitliche Serviceklappen bei offenem Torso', 2)
    if cfg['helmet_light'] != 'none':
        add('HELM_LIGHT', 'Helmlicht links/rechts', 'Aussen in seitlichen Helmlichtpods',
            'EFFECT_15V' if cfg['helmet_light'] == 'power-rgb' else 'EFFECT_5V',
            'Lichtfenster nach vorn, eigene abgeschirmte Kuehlkoerper nach aussen', 2)
    if cfg['nozzle_light'] != 'none':
        add('NOZZLE_LIGHT', 'RGB-Licht links/rechts', 'Trockene Duesenumrandung am Ruecken',
            'EFFECT_15V', 'Nebelkanal bleibt frei; optischer Zugang zum ausgetretenen Nebel', 2)
    if cfg['nozzle_air'] != 'none':
        add('NOZZLE_FANS', 'Trockene Effektluefter', 'Seitlicher Luftkanal neben jedem Nebelauslass',
            'EFFECT_5V', 'Kein Anschluss an Nebelschlauch; Nebelruecksog am Versuch pruefen', 2)
    if cfg['helmet_light'] != 'none' or cfg['nozzle_light'] != 'none' or cfg['nozzle_air'] != 'none':
        add('EFFECT_CONTROL', 'Effektcontroller, Pegelstufen und Temperaturueberwachung',
            'Seitliches trockenes Servicefach am Traeger', 'EFFECT_5V',
            'Reset-/Abschaltpfad hardwareseitig pruefen, Taster vorne erreichbar')
    if cfg['hud'] != 'none':
        add('HUD', 'Monokulares HUD mit Optik', 'Seitlich oberhalb Hauptsicht, mechanisch wegklappbar',
            'COMFORT_5V', 'Mit einer Hand wegklappen; Optik, Brille und Augenabstand separat abstimmen')
        add('HUD_HOST', 'HUD-Bildgeber und Ansteuerung', 'Beluefteter Helm-Servicepod nahe Display',
            'COMFORT_5V', 'Passende kurze Displayschnittstelle; Abwaerme und Zugang separat pruefen')
    if cfg['camera'] != 'none':
        add('CAMERA', 'Helmkamera', 'Stirn-/Sensormodul mit freiem optischen Fenster',
            'COMFORT_5V', 'Aufnahmeanzeige nach aussen; Service ohne Demontage des Visiers')
        add('RECORDER', 'Recorder und Kameraelektronik',
            'Seitlicher Ruecken-Servicepod' if cfg['camera'] == 'usb-uvc' else 'Beluefteter lokaler Helmpod',
            'COMFORT_5V', 'USB-Leitung mit Zugentlastung' if cfg['camera'] == 'usb-uvc' else 'Kurze CSI-Verbindung, lokaler Waermenachweis')
    if cfg['audio'] != 'none':
        add('MIC', 'Mikrofon mit Vorverstaerker', 'Innerer Wangen-/Mundbereich abseits Luefterstrahl',
            'COMFORT_5V', 'Am abnehmbaren Helmeinsatz; Kabel zugentlastet')
        add('AUDIO', 'Sprachverstaerker und Lautsprecher', 'Verstaerker seitlich, Lautsprecher vorderer Brustgrill',
            'COMFORT_5V', 'Frontseitige Lautstaerke/Stummschaltung, akustisch von Mikrofon getrennt')
    if fit['build']['fog_system'] == 'pmi-cloud':
        add('FOG', 'OEM-Nebler mit Originalakku', 'Herstellerhuelle auf seitlich erreichbarer Traegerkassette',
            'FOG_OEM', 'Originalbedienung direkt erreichbar; Fernbedienung ersetzt diesen Zugang nicht')
    circuits = sorted({m['circuit'] for m in modules})
    if 'COMFORT_5V' in circuits:
        add('B_COMFORT', 'Komfort-Powerbank', 'Tief an linker Flanke am Huefttraeger', 'SOURCE_COMFORT',
            'Nach vorn/seitlich herausziehbar; separater Schalter vorne links')
    if any(c.startswith('EFFECT_') for c in circuits):
        add('B_EFFECT', 'Effekt-Powerbank und Verteilung', 'Tief an rechter Flanke am Huefttraeger', 'SOURCE_EFFECT',
            'Nach vorn/seitlich herausziehbar; Schalter vorne rechts, LED-Treiber im separaten Servicefach')
    return {'schema_version': 1, 'project': fit['profile'], 'configuration': deepcopy(cfg),
            'status': 'PLACEMENT_PLAN_NOT_VALIDATED', 'hardware_approved': False,
            'solo_donning_verified': False, 'budget_covers_integration': False,
            'mounts': modules, 'circuits': circuits,
            'constraints': [
                'Zonen sind Einbauvorschlaege ohne Koordinaten- oder Kollisionsnachweis.',
                'Kein Akkublock am Sternum oder direkt auf der Wirbelsaeule; keine Last an duennen Zierschalen.',
                'Komfortversorgung unabhaengig vom Effektschalter; keine Powerbank-Ausgaenge zusammenschalten.',
                '15 V nur nach verifiziertem USB-PD-Profil und geeignetem PD-Sink; 5 V separat geregelt.',
                'USB-/Audio-/Display-Komponenten muessen die vorgeschlagene Versorgung tatsaechlich unterstuetzen.',
                'Highpower-RGB benoetigt Konstantstromtreiber; PWM-Pin und LED-Leistungsausgang sind verschiedene Schnittstellen.',
                'Helm- und Duesen-RGB je Paar farbweise in Reihe gemaess Lichtguide; keine gemeinsame LED-Ausgangsmasse.',
                'Jede Arm-/Beinkassette und jeder darin laufende Gurt muss vollstaendig oeffnen.',
                'Nebel, trockene Duesenluft und Komfortluft bleiben getrennte Wege.',
                'Alle Leistungs-, Groessen- und Massedaten sowie physische Tests bleiben projektbezogen offen.'
            ]}


def engineering_inputs(integration):
    data = suit_engineering.new_project(integration['project'])
    circuits = integration['circuits']
    data['rails'], data['batteries'] = [], []
    for source, required in [('B_COMFORT', 'COMFORT_5V' in circuits),
                             ('B_EFFECT', any(c.startswith('EFFECT_') for c in circuits)),
                             ('B_FOG', 'FOG_OEM' in circuits)]:
        if required: data['batteries'].append({'id': source, 'usable_energy_wh': None})
    for circuit in circuits:
        battery = 'B_COMFORT' if circuit == 'COMFORT_5V' else 'B_FOG' if circuit == 'FOG_OEM' else 'B_EFFECT'
        consumers = [{'id': m['id'], 'quantity': m['quantity'], 'power_w': None,
                      'duty_fraction': None, 'peak_power_w': None}
                     for m in integration['mounts'] if m['circuit'] == circuit]
        data['rails'].append({'id': circuit, 'battery_id': battery,
                              'voltage_v': 5 if circuit.endswith('5V') and circuit != 'EFFECT_15V' else 15 if circuit == 'EFFECT_15V' else None,
                              'efficiency_fraction': None, 'idle_input_w': None, 'consumers': consumers})
    data['notes'] = ('Ausgewaehlte Verbraucher mit unbekannten Leistungen. power_w gilt pro Positionseinheit; '
                     'bei RGB die anteilige Treiber-/Wandlerleistung auf den Modulen erfassen, nicht doppelt zaehlen. '
                     'Recorder/Host nur ohne bereits getrennt erfasste Kamera/Displayleistung eintragen; '
                     'bei gemeinsamer Eingangsmessung als eine Baugruppe zusammenfassen. '
                     'Spannungen sind Entwurfsziele, keine nachgemessenen USB-PD- oder Geraeteeigenschaften.')
    return data


def thermal_inputs(integration):
    data = suit_thermal.new_project(integration['project'])
    module = deepcopy(data['modules'][0]); vent = deepcopy(data['vents'][0])
    data['modules'], data['vents'] = [], []
    for mount in integration['mounts']:
        if mount['id'] in ('HELM_LIGHT', 'NOZZLE_LIGHT') and mount['circuit'] == 'EFFECT_15V':
            for side in ('L', 'R'):
                row = deepcopy(module); row['id'] = mount['id'] + '_' + side
                die = deepcopy(row['junction_paths'][0])
                row['junction_paths'] = [dict(deepcopy(die), id=color) for color in ('R', 'G', 'B')]
                data['modules'].append(row)
        if mount['id'] in ('HELM_FANS', 'TORSO_FANS', 'RECORDER', 'HUD_HOST', 'EFFECT_CONTROL'):
            row = deepcopy(vent); row['id'] = mount['id']
            data['vents'].append(row)
    return data


def render(integration):
    lines = ['# Einbau- und Versorgungsplan', '', 'Projekt: ' + integration['project'], '',
             'Status: **PLACEMENT_PLAN_NOT_VALIDATED**. Einbauorte sind Vorschlaege; noch keine Passprobe.', '',
             '| Modul | Anzahl | Einbauzone | Stromkreis | Zugang |', '| --- | ---: | --- | --- | --- |']
    for m in integration['mounts']:
        lines.append(f"| {m['label']} | {m['quantity']} | {m['mounting_zone']} | {m['circuit']} | {m['access']} |")
    lines += ['', '## Auslegung', '',
              'engineering.local.json enthaelt die ausgewaehlten Verbraucher; unbekannte Leistungen bleiben null.',
              'thermal.local.json trennt gemeinsame LED-Kuehlkoerper, einzelne Farbchips und gemessene Luftwege.',
              'Integration.json fuehrt unbekannte Bauraummasse, Masse und Stecker. Eine Zonenzuordnung ist keine CAD-Kollisionserkennung.',
              'Die bestehende Budgetvorlage muss an diese Ausstattung angepasst werden; sie deckt diese Auswahl nicht automatisch ab.', '',
              '## Schnittstellenregeln', ''] + ['- ' + rule for rule in integration['constraints']]
    return '\n'.join(lines) + '\n'
