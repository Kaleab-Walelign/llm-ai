"""Cell 7 — Context builder and recommendations."""
RECOMMENDATIONS = {
    'rangeland': {
        'Very Low':  {'pastoral':'Reduce grazing immediately; move livestock; destock non-productive animals; seek emergency support.',
                      'expert':'Trigger drought/degradation alerts; recommend emergency destocking; identify restoration sites.',
                      'policy':'Declare high-risk status; mobilize emergency relief; enforce grazing restrictions.'},
        'Low':       {'pastoral':'Practice controlled grazing; begin early destocking; protect recovering areas.',
                      'expert':'Intensify monitoring; advise rotational grazing and water point management.',
                      'policy':'Support early warning; allocate funds for preventive actions.'},
        'Moderate':  {'pastoral':'Maintain planned grazing; avoid herd expansion; protect key reserves.',
                      'expert':'Continue routine monitoring; provide technical advice; support adaptive grazing.',
                      'policy':'Invest in capacity building; support community grazing institutions.'},
        'High':      {'pastoral':'Sustain good practices; use rangeland strategically; avoid uncontrolled growth.',
                      'expert':'Document best practices; monitor for early decline.',
                      'policy':'Incentivize sustainable management; scale up successful models.'},
        'Very High': {'pastoral':'Use as strategic reserve; maintain traditional conservation rules.',
                      'expert':'Use as reference benchmark; promote ecosystem service valuation.',
                      'policy':'Designate for conservation; invest in long-term sustainability.'},
    },
    'climate': {
        'Very Low':  {'pastoral':'Urgent destocking; move to drought refuges; seek emergency water and feed.',
                      'expert':'Declare severe drought; guide emergency response.',
                      'policy':'Declare emergency; mobilize contingency funds; coordinate humanitarian response.'},
        'Low':       {'pastoral':'Start early destocking; plan mobility routes; prioritize breeding animals.',
                      'expert':'Issue early drought warnings; intensify monitoring.',
                      'policy':'Release early-action financing; support market access for destocking.'},
        'Moderate':  {'pastoral':'Apply adaptive grazing; begin preparedness; avoid herd expansion.',
                      'expert':'Monitor rainfall and temperature anomalies.',
                      'policy':'Activate climate watch; ensure contingency plans are updated.'},
        'High':      {'pastoral':'Normal grazing; avoid concentration near water points.',
                      'expert':'Continue seasonal monitoring; advise against rapid herd growth.',
                      'policy':'Maintain routine NRMS reporting; strengthen early-warning systems.'},
        'Very High': {'pastoral':'Continue normal seasonal grazing; protect dry-season reserves.',
                      'expert':'Document climate-responsive practices; use as baseline reference.',
                      'policy':'Invest in resilience-building.'},
    },
    'livestock': {
        'Very Low':  {'pastoral':'Potential to increase herd carefully if forage allows.',
                      'expert':'Assess forage availability before recommending increases.',
                      'policy':'Support livelihood diversification.'},
        'Low':       {'pastoral':'Potential to increase herd carefully if forage allows.',
                      'expert':'Assess forage availability; monitor vegetation response.',
                      'policy':'Support livelihood diversification.'},
        'Moderate':  {'pastoral':'Maintain current herd size; avoid growth.',
                      'expert':'Monitor vegetation response to current stocking.',
                      'policy':'Support productivity and rangeland management.'},
        'High':      {'pastoral':'Begin gradual herd reduction; sell non-productive animals.',
                      'expert':'Advise herd restructuring; apply stocking rate analysis.',
                      'policy':'Incentivize destocking through market support.'},
        'Very High': {'pastoral':'Urgent destocking required; redistribute herds.',
                      'expert':'Apply strict stocking rate-based management.',
                      'policy':'Enforce stocking limits; provide market access for destocking.'},
    },
    '_default': {
        'Very Low':  {'pastoral':'Urgent attention. Seek support; avoid further pressure on this resource.',
                      'expert':'Immediate intervention needed. Assess causes and design recovery plan.',
                      'policy':'Prioritize for emergency support and restoration funding.'},
        'Low':       {'pastoral':'Be cautious; limit use and consider alternatives.',
                      'expert':'Recommend preventive measures and closer monitoring.',
                      'policy':'Allocate resources for early intervention.'},
        'Moderate':  {'pastoral':'Continue current practices with care; avoid overuse.',
                      'expert':'Maintain routine monitoring; advise on improvements.',
                      'policy':'Support extension services and community management.'},
        'High':      {'pastoral':'Good conditions; maintain practices sustainably.',
                      'expert':'Document practices and monitor for early changes.',
                      'policy':'Incentivize and scale up sustainable management.'},
        'Very High': {'pastoral':'Excellent; conserve as a strategic resource.',
                      'expert':'Use as reference site; promote as a model.',
                      'policy':'Invest in long-term conservation.'},
    },
}

def get_recommendation(layer_key, label):
    rec = RECOMMENDATIONS.get(layer_key, RECOMMENDATIONS['_default'])
    if layer_key == 'encroachment':
        label_map = {'None':'Very High','Low':'High','Moderate':'Moderate',
                     'High':'Low','Severe':'Very Low','Maximum':'Very Low'}
        label = label_map.get(label, label)
    return rec.get(label, RECOMMENDATIONS['_default'].get(label, {}))

def build_ai_context(result):
    if 'error' in result:
        return f'Error: {result["error"]}'
    area = result.get("area") or result.get("woreda", "")
    lines = [
        f'AREA: {area}',
        f'REGION: {result.get("region_display","")}',
        f'ADMIN LEVEL: {result.get("admin_level","woreda")}',
        f'FEATURES: {result.get("feature_count", 1)} polygon(s)',
        '', '=== LAYER RESULTS ===',
    ]
    for lk, data in result['layers'].items():
        lines.append('')
        nm = lk.upper().replace('_',' ')
        if 'error' in data:
            lines.append(f'[{nm}]: ERROR — {data["error"]}'); continue
        lines.append(f'[{nm}]')
        lines.append(f'  Value: {data["mean"]} (range {data["min"]}–{data["max"]})')
        lines.append(f'  Condition: {data["label"]} — {data["description"]}')
        rec = get_recommendation(lk, data['label'])
        if rec:
            if rec.get('pastoral'): lines.append(f'  → Pastoralists: {rec["pastoral"]}')
            if rec.get('expert'):   lines.append(f'  → Experts:      {rec["expert"]}')
            if rec.get('policy'):   lines.append(f'  → Policy:       {rec["policy"]}')
    return '\n'.join(lines)

