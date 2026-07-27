"""Append new backlog bets to FALLBACK_BETS in index.html."""
import json, re
from pathlib import Path

ROOT = Path("/home/user/workspace/bet-tracker")
HTML = ROOT / "index.html"

# Load the 30 bets we already assembled by re-executing the builder (extract new_bets list only)
add_script = (ROOT / "add_backlog_bets.py").read_text()
# Strip trailing write section to get just the data
add_script_no_write = add_script.split("# --------- Now write ----------")[0]
namespace = {}
exec(add_script_no_write, namespace)
new_bets = namespace["new_bets"]

# Assign IDs 1758-1787
for i, b in enumerate(new_bets):
    b["ID"] = str(1758 + i)

# Read index.html
html = HTML.read_text()
m = re.search(r"const FALLBACK_BETS\s*=\s*(\[[\s\S]*?\]);", html)
if not m:
    raise SystemExit("FALLBACK_BETS not found in index.html")

bets = json.loads(m.group(1))
print(f"Current FALLBACK_BETS count: {len(bets)}")
existing_ids = {b.get("ID") for b in bets}

# Filter out any accidental dupes by ticket id in notes
existing_tickets = set()
for b in bets:
    notes = b.get("Notes", "")
    for tid in re.findall(r"#([A-Z0-9_]+)", notes):
        existing_tickets.add(tid)

to_add = []
for b in new_bets:
    if b["ID"] in existing_ids:
        print(f"  SKIP dupe ID {b['ID']}")
        continue
    # Check ticket collision
    dupe_by_ticket = False
    for tid in re.findall(r"#([A-Z0-9_]+)", b.get("Notes", "")):
        if tid in existing_tickets:
            print(f"  SKIP dupe ticket #{tid} (ID {b['ID']})")
            dupe_by_ticket = True
            break
    if dupe_by_ticket:
        continue
    to_add.append(b)

print(f"Adding {len(to_add)} new bets")
bets.extend(to_add)
print(f"New FALLBACK_BETS count: {len(bets)}")

# Serialize with same format as existing
new_json = json.dumps(bets, indent=2, ensure_ascii=False)
new_html = html[:m.start(1)] + new_json + html[m.end(1):]
HTML.write_text(new_html)
print(f"Wrote {HTML}")
