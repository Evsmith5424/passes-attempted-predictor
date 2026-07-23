"""
generate_rosters.py

Automates Step 2 + Step 3 of the "Adding Real Data" guide: turns a CSV of raw,
match-by-match passing data into the exact ROSTERS JavaScript object the
worldcup_passes_predictor.html tool expects — with each player's average
passes attempted already computed over their most recent 30 games (or fewer,
if they haven't played 30).

------------------------------------------------------------------------------
INPUT CSV FORMAT (one row per player, per match):

    team_code,position,player_id,player_name,number,match_date,passes_attempted,rating

    - team_code        : must match a `code` in the TEAMS array in the HTML file (e.g. "ESP")
    - position          : one of CB, RB, LB, CDM, CM, CAM, RW, LW, ST
    - player_id          : any stable unique id per player (e.g. "sergio-ramos")
    - player_name        : display name
    - number             : jersey number (int)
    - match_date          : YYYY-MM-DD
    - passes_attempted    : integer, that player's passes attempted in that match
    - rating              : optional. A card rating 0-99. Leave blank if unknown —
                             the script will fill a placeholder and flag it for manual review.

You do not need to pre-sort or pre-filter to "last 30 games" — the script does
that automatically per player, using match_date to find the most recent games.

------------------------------------------------------------------------------
USAGE

    python3 generate_rosters.py raw_passing_data.csv > rosters_snippet.js

Then paste the printed `const ROSTERS = {...}` block into worldcup_passes_predictor.html,
replacing the existing ROSTERS/generateRoster mechanism (see the guide, Step 2).
------------------------------------------------------------------------------
"""

import sys
import csv
import json
from collections import defaultdict
from datetime import datetime

VALID_POSITIONS = {"CB", "RB", "LB", "CDM", "CM", "CAM", "RW", "LW", "ST"}
MAX_GAMES = 30
PLACEHOLDER_RATING = 75  # used only when the CSV doesn't supply one; flagged in stderr


def load_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"team_code", "position", "player_id", "player_name",
                    "number", "match_date", "passes_attempted"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"ERROR: CSV is missing required column(s): {sorted(missing)}")
        rows = list(reader)
    if not rows:
        sys.exit("ERROR: CSV has no data rows.")
    return rows


def build_rosters(rows):
    # group rows by (team_code, position, player_id)
    by_player = defaultdict(list)
    meta = {}

    for i, r in enumerate(rows, start=2):  # start=2: row 1 is the header
        pos = r["position"].strip().upper()
        if pos not in VALID_POSITIONS:
            sys.exit(f"ERROR: row {i} has invalid position '{r['position']}'. "
                      f"Must be one of {sorted(VALID_POSITIONS)}.")
        try:
            passes = int(float(r["passes_attempted"]))
        except ValueError:
            sys.exit(f"ERROR: row {i} has non-numeric passes_attempted '{r['passes_attempted']}'.")
        try:
            date = datetime.strptime(r["match_date"].strip(), "%Y-%m-%d")
        except ValueError:
            sys.exit(f"ERROR: row {i} has bad match_date '{r['match_date']}' (expected YYYY-MM-DD).")

        key = (r["team_code"].strip(), pos, r["player_id"].strip())
        by_player[key].append((date, passes))
        meta[key] = {
            "name": r["player_name"].strip(),
            "number": int(r["number"]) if str(r["number"]).strip() else None,
            "rating": r.get("rating", "").strip(),
        }

    missing_ratings = []
    rosters = defaultdict(lambda: defaultdict(list))

    for (team_code, pos, player_id), games in by_player.items():
        games.sort(key=lambda g: g[0], reverse=True)   # most recent first
        recent = games[:MAX_GAMES]
        caps_used = len(recent)
        avg_passes = round(sum(p for _, p in recent) / caps_used, 1)

        m = meta[(team_code, pos, player_id)]
        rating = m["rating"]
        if rating == "":
            missing_ratings.append(f"{m['name']} ({team_code} {pos})")
            rating_val = PLACEHOLDER_RATING
        else:
            rating_val = int(rating)

        rosters[team_code][pos].append({
            "id": f"{team_code}-{pos}-{player_id}",
            "name": m["name"],
            "number": m["number"],
            "rating": rating_val,
            "avgPasses": avg_passes,
            "capsPlayed": caps_used,
        })

    # sort each position's players by avgPasses descending, just for readability
    for team_code in rosters:
        for pos in rosters[team_code]:
            rosters[team_code][pos].sort(key=lambda p: -p["avgPasses"])

    return rosters, missing_ratings


def to_js(rosters):
    # json.dumps gives valid JS object syntax for this data shape
    plain = {team: dict(positions) for team, positions in rosters.items()}
    body = json.dumps(plain, indent=2)
    return "const ROSTERS = " + body + ";\n"


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 generate_rosters.py <input_csv_path>")
    rows = load_rows(sys.argv[1])
    rosters, missing_ratings = build_rosters(rows)

    js = to_js(rosters)
    print(js)

    # Summary + warnings go to stderr so they don't pollute the JS output on stdout
    total_players = sum(len(v) for team in rosters.values() for v in team.values())
    print(f"--- Summary ---", file=sys.stderr)
    print(f"Teams: {len(rosters)}", file=sys.stderr)
    print(f"Players: {total_players}", file=sys.stderr)
    for team_code, positions in rosters.items():
        counts = ", ".join(f"{pos}:{len(v)}" for pos, v in sorted(positions.items()))
        print(f"  {team_code}: {counts}", file=sys.stderr)
    if missing_ratings:
        print(f"\nWARNING: {len(missing_ratings)} player(s) had no rating in the CSV "
              f"and were set to the placeholder {PLACEHOLDER_RATING}. Fill these in manually:",
              file=sys.stderr)
        for name in missing_ratings:
            print(f"  - {name}", file=sys.stderr)


if __name__ == "__main__":
    main()
