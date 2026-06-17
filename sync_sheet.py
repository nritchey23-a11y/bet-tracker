"""Sync dashboard FALLBACK_BETS → Google Sheet.

Steps:
1. Pull 10 missing futures (IDs 1364-1372, 1409) from sheet into dashboard
2. Normalize Risk/To Win (strip .0 suffix)
3. Write the merged sorted list back to index.html
4. Output a CSV of all 1664 rows (1654 existing + 10 added) ready for sheet upload
"""
import json, re

# --- Load sheet ---
with open('/home/user/workspace/bet-tracker/sheet_full.json') as f:
    sheet = json.load(f)
hdr = sheet['values'][0]
rows = sheet['values'][1:]
sheet_by_id = {r[0]: dict(zip(hdr, r + ['']*(15-len(r)))) for r in rows if r and r[0]}

# --- Load dashboard ---
with open('/home/user/workspace/bet-tracker/index.html') as f:
    content = f.read()
m = re.search(r'(const FALLBACK_BETS\s*=\s*)(\[.*?\])(\s*;)', content, re.DOTALL)
prefix, arr_str, suffix = m.group(1), m.group(2), m.group(3)
bets = json.loads(arr_str)
dash_ids = {str(b['ID']) for b in bets}

# --- Normalize date format helper ---
def norm_date(s):
    if not s: return ''
    s = s.strip()
    # MM/DD/YYYY → YYYY-MM-DD
    mm = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', s)
    if mm:
        return f"{mm.group(3)}-{int(mm.group(1)):02d}-{int(mm.group(2)):02d}"
    return s

def norm_num(s):
    if s is None: return ''
    s = str(s).strip()
    if s.endswith('.0'):
        return s[:-2]
    if s.endswith('.00'):
        return s[:-3]
    return s

# --- Sport/League/Type inference for missing futures ---
def infer_sport_league(d):
    desc = (d.get('Description') or '').lower()
    notes = (d.get('Notes') or '').lower()
    if 'nfl' in notes or 'season wins' in desc and any(t in desc for t in ['lions','packers','ravens','broncos','texans','vikings','bears','panthers']):
        return ('Football','NFL','future')
    if 'masters' in desc.lower() or 'pga' in notes or 'majors' in desc.lower() or 'major' in desc:
        return ('Golf','PGA Tour','outright')
    if 'world cup' in desc or 'fifa' in notes:
        return ('Soccer','FIFA','future')
    return ('','','future')

# --- Add missing futures from sheet (excluding duplicate 1373) ---
MISSING = ['1364','1365','1366','1367','1368','1369','1370','1371','1372','1409']
added = 0
for sid in MISSING:
    if sid in dash_ids:
        continue
    s = sheet_by_id.get(sid)
    if not s:
        print(f"WARN: {sid} not found in sheet")
        continue
    sport, league, typ = infer_sport_league(s)
    new_bet = {
        'ID': sid,
        'Date': norm_date(s.get('Date','')),
        'Sport': s.get('Sport') or sport,
        'League': s.get('League') or league,
        'Event': s.get('Event',''),
        'Type': s.get('Type') or typ,
        'Description': s.get('Description',''),
        'Pick': s.get('Pick',''),
        'Opponent': s.get('Opponent',''),
        'Odds': s.get('Odds',''),
        'Risk': norm_num(s.get('Risk','')),
        'To Win': norm_num(s.get('To Win','')),
        'Status': 'pending' if (s.get('Status','').lower() == 'push' and sid == '1409') else (s.get('Status') or 'pending').lower(),
        'Result Date': norm_date(s.get('Result Date','')),
        'Notes': s.get('Notes',''),
    }
    bets.append(new_bet)
    added += 1
    print(f"Added ID {sid}: {new_bet['Pick']} | {new_bet['Description'][:60]}")

# --- Normalize all Risk/To Win in dashboard ---
fixed_nums = 0
for b in bets:
    for k in ('Risk','To Win'):
        v = str(b.get(k,''))
        new = norm_num(v)
        if new != v:
            b[k] = new
            fixed_nums += 1

print(f"\nNormalized {fixed_nums} numeric fields")
print(f"Added {added} futures back to dashboard")

# --- Sort by ID numeric ---
def id_key(b):
    try: return int(b.get('ID'))
    except: return 999999
bets.sort(key=id_key)
print(f"Total dashboard bets: {len(bets)}")

# --- Write back to index.html ---
new_arr = json.dumps(bets, indent=2)
new_content = content[:m.start()] + prefix + new_arr + suffix + content[m.end():]
with open('/home/user/workspace/bet-tracker/index.html','w') as f:
    f.write(new_content)
print("index.html updated")

# --- Save sheet upload data ---
sheet_cols = ['ID','Date','Sport','League','Event','Type','Description','Pick','Opponent','Odds','Risk','To Win','Status','Result Date','Notes']
values = [sheet_cols]
for b in bets:
    values.append([str(b.get(c,'') or '') for c in sheet_cols])
with open('/home/user/workspace/bet-tracker/sheet_upload.json','w') as f:
    json.dump({'values': values}, f)
print(f"sheet_upload.json: {len(values)} rows (incl header)")
