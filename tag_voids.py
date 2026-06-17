"""Add [VOID:Type] / [PUSH:Type] tags to Notes field for all 36 pushes + 2 leg-voided non-push bets."""
import json, re, copy

with open('/home/user/workspace/bet-tracker/index.html') as f:
    content = f.read()

m = re.search(r'(const FALLBACK_BETS\s*=\s*)(\[.*?\])(\s*;)', content, re.DOTALL)
prefix, arr_str, suffix = m.group(1), m.group(2), m.group(3)
bets = json.loads(arr_str)

# Categorization map
MUST_START = {'1509','1510','1511','1512','1578','1579','1580','1581'}
WEATHER = {'1663'}
SCRATCH = {'1379'}
NO_ACTION = {'1609'}
ONE_FIVE_TIE = {'1556','1603','1605','1619','1627'}
TOTAL_EXACT = {'1468','1490'}
ATS_TIE = {'141','180','315','350','357','428','625','664','683','757','809','826','1015','1046'}
HALF_TOTAL_TIE = {'455'}
H2H_TIE = {'29','48','1407'}
# Non-push but leg-voided
LEG_VOID_MUSTSTART = {'1536','1586'}

def tag_for(bet_id):
    if bet_id in MUST_START: return '[VOID:MustStart]'
    if bet_id in WEATHER: return '[VOID:Weather]'
    if bet_id in SCRATCH: return '[VOID:Scratch]'
    if bet_id in NO_ACTION: return '[VOID:NoAction]'
    if bet_id in ONE_FIVE_TIE: return '[PUSH:1st5Tie]'
    if bet_id in TOTAL_EXACT: return '[PUSH:TotalExact]'
    if bet_id in ATS_TIE: return '[PUSH:ATSTie]'
    if bet_id in HALF_TOTAL_TIE: return '[PUSH:1HTotalTie]'
    if bet_id in H2H_TIE: return '[PUSH:H2HTie]'
    if bet_id in LEG_VOID_MUSTSTART: return '[LEG_VOID:MustStart]'
    return None

# Strip any existing tag (in case of re-run)
tag_pattern = re.compile(r'^\[(VOID|PUSH|LEG_VOID):[A-Za-z0-9]+\]\s*')

count = 0
for b in bets:
    bid = str(b.get('ID'))
    tag = tag_for(bid)
    if tag is None:
        continue
    notes = b.get('Notes') or ''
    notes = tag_pattern.sub('', notes).strip()
    new_notes = f"{tag} {notes}".strip() if notes else tag
    b['Notes'] = new_notes
    count += 1

print(f"Tagged {count} bets")

# Write back — preserve formatting style (2-space indent)
new_arr = json.dumps(bets, indent=2)
new_content = content[:m.start()] + prefix + new_arr + suffix + content[m.end():]
with open('/home/user/workspace/bet-tracker/index.html','w') as f:
    f.write(new_content)
print("index.html updated")

# Summary by category
from collections import Counter
cats = Counter()
for b in bets:
    notes = b.get('Notes') or ''
    mm = tag_pattern.match(notes)
    if mm:
        cats[mm.group(0).strip()] += 1
print("\nCategory counts:")
for k,v in sorted(cats.items()):
    print(f"  {k}: {v}")
