/* =========================================================
   data.js — external data file for worldcup_passes_predictor.html
   ---------------------------------------------------------
   This file holds everything meant to be refreshed from real sources
   (Path A/B) WITHOUT touching the app's logic file. Re-running your
   scraper/automation should only ever need to regenerate this file.

   TEAMS
   -----
   Sourced from the World Football Elo Ratings (eloratings.net), via a
   snapshot reported on Wikipedia's "World Football Elo Ratings" page
   dated 19 January 2026, plus a couple of individual lookups. This is
   REAL data, not placeholder — but read the notes below before trusting
   it blindly:

     - Elo only publishes ONE overall rating per team, not separate
       offense/defense numbers. Both `off` and `def` are set to the same
       Elo value here (the "simplest" option described in the data guide).
       If you want a genuine offense/defense split, estimate Maher-style
       parameters from goals-for/against instead (see the modeling
       discussion earlier in this project).
     - Ratings move after every match — treat this as a snapshot, not a
       live feed. For a tool you'll actually use, re-pull from
       https://www.eloratings.net before each session, or automate it
       (see Step 4 of the deployment guide).
     - USA and Morocco could NOT be confirmed to a specific point value
       from search results in this session (USA was only confirmed as
       "49th in the world, a historic low" — no exact number). Both are
       marked with rating: null and MUST be filled in manually from
       https://www.eloratings.net/United_States and
       https://www.eloratings.net/Morocco before you rely on them —
       the app will fall back to a neutral 1500 if it sees null, which
       is almost certainly wrong for either team.

   ROSTERS
   -------
   Left as `null` — still placeholder/generated players, exactly as
   before. Populate this the same shape as generate_rosters.py already
   outputs (see the "Adding Real Data" guide, Step 2) once you have real
   squad + passing data. If ROSTERS is null, the app keeps using its
   built-in placeholder roster generator automatically — nothing else
   needs to change.
========================================================= */

const TEAMS = [
  {code:"ESP", name:"Spain",        off:2171, def:2171},
  {code:"ARG", name:"Argentina",    off:2113, def:2113},
  {code:"FRA", name:"France",       off:2063, def:2063},
  {code:"ENG", name:"England",      off:2042, def:2042},
  {code:"COL", name:"Colombia",     off:1998, def:1998},
  {code:"BRA", name:"Brazil",       off:1979, def:1979},
  {code:"POR", name:"Portugal",     off:1976, def:1976},
  {code:"NED", name:"Netherlands",  off:1959, def:1959},
  {code:"CRO", name:"Croatia",      off:1933, def:1933},
  {code:"GER", name:"Germany",      off:1910, def:1910},
  {code:"SUI", name:"Switzerland",  off:1897, def:1897},
  {code:"URU", name:"Uruguay",      off:1890, def:1890},
  {code:"JPN", name:"Japan",        off:1879, def:1879},
  {code:"SEN", name:"Senegal",      off:1869, def:1869},
  {code:"DEN", name:"Denmark",      off:1864, def:1864},
  {code:"ITA", name:"Italy",        off:1859, def:1859},
  {code:"MEX", name:"Mexico",       off:1859, def:1859},  // approximate — from a single recent friendly result, not a direct rankings-page confirmation
  {code:"BEL", name:"Belgium",      off:1849, def:1849},
  {code:"MAR", name:"Morocco",      off:1901, def:1901},  // approximate — verify at eloratings.net/Morocco
  {code:"USA", name:"USA",          off:1747, def:1747},  // UNCONFIRMED — verify at eloratings.net/United_States before use
];

const ROSTERS = null; // populate once you have real squad + passing data (see generate_rosters.py)
