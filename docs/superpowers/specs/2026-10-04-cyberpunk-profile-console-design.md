# Cyberpunk Profile Console — Design

**Date:** 2026-10-04
**Status:** Approved
**Reference:** "I Turned My GitHub Profile Into a Cyberpunk Console With a City Built From My Contributions" (dev.to, georgekobaidze)

## Goal

Replace the `JaisonJecinthVincent/JaisonJecinthVincent` profile with a self-updating cyberpunk
console: one continuous neon terminal, built from stacked SVG slices, containing a contribution
graph rendered as an isometric city built from real GitHub data.

## Context

The current profile is three hand-authored SVGs (`cyber-header.svg`, `contribution-city.svg`,
`cyber-footer.svg`) with plain Markdown sections between them. The city is decorative and its own
README admits it is "a hand-crafted baseline." It does not update.

The reference implementation was verified directly rather than taken on prose: its
`contribution-city.svg` is 880×680 with `role="img"` and `aria-labelledby`; its slices embed
base64 `data:font/woff2` JetBrains Mono subsets under a `'JBM', ui-monospace, SFMono-Regular,
Menlo, Consolas, monospace` stack; its `@keyframes` are `fadein, blink, pulse, type, flicker`.

### Account facts

- Login `JaisonJecinthVincent`, account created 2024-05-05, ~2.3 years of history
- 30 public repositories, 1 star total, 0 followers
- No `dev.to` account, no website, no public email
- Primary language mix: Python, TypeScript, JavaScript, Java, C++, Jupyter Notebook, CSS, HTML

### Divergences from the reference

1. **No DEV integration.** The reference devotes a full section and a stats block to the Forem API
   (articles, reactions, comments, views, followers). There is no dev.to account to query, so this
   is removed entirely, not stubbed.
2. **No project cards in v1.** Deferred by explicit decision. The slice registry is designed so they
   can be appended later without touching the frame primitives.
3. **No link buttons in v1.** Deferred by explicit decision. GitHub, LinkedIn, email, and the velxio
   Discord invite all exist as possibilities but none are included.
4. **Smaller history.** Two years, not a decade. The all-time query still handles any number of years.
5. **Honest framing.** The profile presents as a final-year CSE student at College of Engineering
   Guindy, Anna University. The previous README's "software engineer" framing was unsupported by the
   account bio and is not carried over.

## Non-goals

- No games (snake, pac-man, tetris) — deliberately avoided as overused
- No hover or click states inside slices; an `<img>` cannot provide them
- No external resources of any kind inside SVGs, including web fonts
- No third-party Python runtime dependencies

## Approach

Chosen: **frame-first renderer with a system monospace stack.**

Rejected alternatives:

- *Embedded font subsets.* Visually closer to the reference and gives deterministic glyph metrics,
  but costs ~400KB of base64 across slices, requires shipping an OFL license file, and adds a
  silent-breakage surface. Because SVG supports `ch` units and `1ch` is exactly one glyph advance in
  a monospace font, no metric is actually needed. Revisit only if the system-font rendering looks
  wrong; it is a single-module change.
- *SVG template files with string substitution.* Splits layout logic across two file types that
  drift apart, with nothing testing the templates. This is the likely origin of the reference's
  40KB single-file `render.py`.

## Architecture

```
tools/profile/
  __init__.py
  config.py          identity copy, palette, dimensions, slice registry
  gh.py              GraphQL client, all-time calendar, streak math
  frame.py           seam primitives: rails, grid, glow, title bar, text helpers
  slices/
    __init__.py      ordered registry
    header.py        top edge + title bar + typing animation
    about.py
    stats.py
    city.py
    matrix.py
    footer.py        bottom edge
  data/
    stats.json
    calendar.json
  fetch.py           pipeline entry: GitHub -> data/*.json
  render.py          pipeline entry: data/*.json -> assets/*.svg
  readme.py          pipeline entry: rewrite marked README zones
tests/
.github/workflows/update-profile.yml
assets/*.svg         generated, committed
```

Every module is independently testable and has one responsibility. `frame.py` knows nothing about
any specific section; `slices/*` know nothing about rails, grid, or glow.

### The seam invariant

Two rules make slice seams invisible by construction rather than by careful arithmetic:

1. Every slice shares viewBox width `SLICE_W = 880`.
2. Every slice height is a multiple of `GRID = 40`.

`frame.py` owns the rails, the background grid, and the glow, so no section places them by hand.
The grid is drawn in slice-local coordinates starting at `y = 0`, so it continues across a cut
instead of restarting. Each slice's rail glow runs from `y = -24` to `y = height + 24` and is
clipped by the viewBox, so the neon does not fade out at a seam like a broken fluorescent tube.

README assembly uses `<p align="center">` with `align="top"` on every image. The `align="top"`
removes the descender gap browsers reserve under images for glyphs like `g` and `y`.

### Slice registry

| Slice | Height | Grid units | Draws | Content |
|---|---|---|---|---|
| `header.svg` | 240 | 6 | top edge, title bar | `$ whoami` typed to `jaison@netrunner`, blinking cursor, glitch on name |
| `about.svg` | 240 | 6 | rails | identity and focus copy |
| `stats.svg` | 240 | 6 | rails | six stat cells |
| `city.svg` | 720 | 18 | rails | isometric contribution city |
| `matrix.svg` | 240 | 6 | rails | tech chips + language bar |
| `footer.svg` | 160 | 4 | bottom edge | `$ exit`, `connection closed` |

Total console height 1840px. The reference needed 23 images for 8 sections; 6 suffice here because
project cards, writing cards, and link buttons are out of scope.

### Slice interface

Each module exposes `render(ctx) -> Slice`, where `ctx` carries parsed stats, the calendar, and
config, and `Slice` is `(filename, svg_body, height, alt_text)`. `render.py` walks the registry in
order, wraps each body in `frame.slice(...)`, and writes to `assets/`.

## Visual system

### Palette

Near-black with electric blue and cyan. One sparing amber accent (`WARN`) for the streak figure only,
to avoid an all-blue monotone.

```
BG      = "#05070d"   near-black, blue-shifted
PANEL   = "#080d17"
RAIL    = "#12304f"
GRID    = "#0c1826"
PRIMARY = "#2f81ff"   electric blue
ACCENT  = "#00d9ff"   cyan
TEXT    = "#d3e9ff"
DIM     = "#6d8fb5"
WARN    = "#ffb454"   amber, streak highlight only
```

### Typography

```
MONO = ui-monospace, SFMono-Regular, Menlo, Consolas, "DejaVu Sans Mono", monospace
```

Weights 400 for body, 700 for headings and figures. No font files are embedded or subset.

Everything that would normally need font metrics is instead done metric-free:

- **Centering** uses `text-anchor`, which is independent of advance widths.
- **The typing reveal** animates `clip-path: inset(0 100% 0 0)` down to `0` in `ch` steps. In a
  monospace font `1ch` is exactly one glyph, so character count maps linearly to percentage.
- **The cursor** is a `<tspan>` at the end of the same `<text>` node, so it inherits its position
  for free and blinks via its own opacity animation.

### Animations

| Keyframe | Duration | Target |
|---|---|---|
| `type` | 40ms per char | clip-path inset on the typed line |
| `blink` | 1.1s step-end | cursor `<tspan>` opacity |
| `glitch` | 6s infinite | name RGB-split via `feOffset` + animated channel offsets |
| `flicker` | 4–9s infinite, per-building delay | a small seeded subset of windows |
| `sweep` | 9s infinite | scanline band translating down the full console |
| `fadein` | 600ms | slice entrance opacity |

`prefers-reduced-motion` is honoured inside each SVG's `<style>` block: animations are disabled and
elements render at their final state.

## Content

All copy and all figures live in `config.py` or `data/*.json`. The values below are the defaults, not
placeholders — they are meant to render a finished profile on first run, and are edited in place
whenever the wording should change.

### header

Typing target: `jaison@netrunner`. Preceded by a static prompt line `$ whoami`. Title bar reads
`jaison@github — ~/profile`.

### about

Heading `// about`. Three lines of body copy:

```
Final-year CSE student at College of Engineering Guindy, Anna University.
I build AI agents, developer tooling, and browser-based hardware emulators —
velxio lets you compile and run code for 19 real boards with no hardware attached.
Currently learning: agentic AI, compilers, and how much of a browser you can bend.
```

### stats

Heading `// telemetry`. Exactly six cells in a 3×2 grid, in this order:

| Cell | Source |
|---|---|
| `contributions_ytd` | sum of `totalContributions` for the current year |
| `contributions_all` | sum of `totalContributions` across all active years |
| `streak_current` | current consecutive-day streak |
| `streak_longest` | longest streak ever |
| `repos` | count of owned, non-fork, public repositories |
| `member_since` | year of `createdAt` (2024) |

Followers and stars are deliberately excluded. At 0 followers and 1 star they would render as
zeros, which reads worse than omitting them. Both become worth adding if the numbers grow.

`streak_current` and `streak_longest` render in `WARN` amber; the rest in `PRIMARY`.

### matrix

Heading `// stack`. Two parts:

- A horizontal language bar, segment widths proportional to summed language bytes across all owned
  non-fork public repositories, coloured by interpolating `PRIMARY` to `ACCENT` across the segment
  index. Segments below 2% are merged into an `other` segment so the bar never degenerates into
  hairlines.
- Technology chips on two rows, drawn from a hand-curated list in `config.py` grouped as
  `languages`, `frontend`, `ai`, `platform`. These are editorial, not derived from the API.

### footer

Prompt line `$ exit`, then `connection to github closed. // EOF`.

## The contribution city

### Data window

Last 53 weeks × 7 days from `calendar.json`, starting on a Sunday, matching GitHub's own graph
alignment.

### Projection

True 2:1 dimetric. `c` is week column `0..52`, `r` is day row `0..6`:

```
x     = (c - r) * sx + x0
y     = (c + r) * sy + y0
depth = c + r

sx = 14   (tile width 28)
sy = 7    (tile depth 14, i.e. 2:1)
y0 = 280
x0 = 118
```

The sign convention is the load-bearing part. Both plan axes project downward (`+c` goes right-down,
`+r` goes left-down), so a larger `c + r` is nearer the viewer. Buildings are sorted ascending by
`c + r` and drawn in that order, so nearer buildings naturally occlude farther ones. Inverting this
sign shears the entire skyline incorrectly.

`x0` exists because `c - r` ranges over `[-6, 52]`, which is not symmetric about zero, so the raw
projection is off-centre. `x0 = SLICE_W / 2 - ((C_MAX - R_MAX) / 2) * sx` centres the tile extents
rather than the cell origins. Forgetting the `SLICE_W / 2` term puts the city at negative
coordinates, entirely off the left edge of the canvas.

Verified extents: tiles span `x = 20..860` (840px wide, an even 20px margin each side), the lowest
tile sits at `y = 686`, and the tallest tower tops out at `y = 162`. The band `y = 0..162` is sky,
and 34px of ground margin sits below the lowest tile.

Each building is three shapes: a roof rhombus and two side walls, each shaded independently so the
form reads as 3D. Left wall darker, right wall mid, roof lightest.

### Height

```
h = 8 + 110 * sqrt(count / c_max)
```

`c_max` is the busiest single day within the 53-week window. The square root lifts quiet days so they
remain visible; a linear scale yields one dominant tower surrounded by flat slabs, which reads as a
parking lot rather than a city.

Zero-contribution days get no building and remain empty lots.

**Edge case:** if `c_max == 0` — a new account, or a 53-week window with no activity — `h` falls
back to a flat 8px slab for every non-zero day rather than dividing by zero.

### Determinism

Window placement and flicker selection use `random.Random(<date string>)` seeded per building from
that building's own ISO date, never from one scene-wide seed.

This is deliberate. As the 53-week window slides forward, every pre-existing building keeps its
exact window pattern and only genuinely new days differ. A scene-wide seed would redraw the entire
city daily and produce an empty "refresh" commit every morning.

### Lighting and sky

Each building gets a window grid on its two visible walls, some lit and some dark, from the seeded
RNG. Buildings whose seed falls below 0.03 receive the `flicker` animation with a seed-derived
delay. The sky carries twinkling stars, a moon with a soft halo, and a plane crossing on a long loop
with blinking navigation lights.

### Sizing

~371 buildings × 3 shapes plus windows yields roughly 200–230KB, consistent with the reference's
227KB. The city is a single unsplit slice; it is the one image where the size is justified.

## Data pipeline

```
fetch.py   ->  GitHub GraphQL  ->  data/stats.json, data/calendar.json
render.py  ->  data/*.json     ->  assets/*.svg
readme.py  ->  marked zones    ->  README.md
git        ->  commit only if something changed
```

### fetch.py

Two GraphQL round trips.

**Query 1** retrieves, in one request: `createdAt`, `followers.totalCount`, `pullRequests.totalCount`,
merged PR count, `contributionsCollection.contributionYears`, and owned non-fork public repositories
with `stargazerCount`, `forkCount`, and `languages(first: 20) { edges { size node { name } } }`.

**Query 2** is constructed at runtime. `contributionsCollection` covers at most one year per request,
so the builder emits one aliased field per active year:

```graphql
y2024: contributionsCollection(from: "2024-01-01T00:00:00Z", to: "2024-12-31T23:59:59Z") {
  totalCommitContributions
  contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
}
```

All years therefore arrive in a single round trip. From the merged result:

- contributions this year and all time are sums of `totalContributions`
- the city window is the last 53 weeks, Sunday-aligned
- the language bar sums language bytes across all repositories

### Stats merge semantics

`fetch.py` loads the previous `stats.json` and overwrites only what it successfully fetched. Each
source is wrapped independently:

- GitHub fetch fails → warn, keep all previous GitHub values
- Both fail → exit non-zero, having written nothing

The profile is therefore at worst one day stale and never blank. A bot that renders "0 stars,
0 contributions" because GitHub returned a 502 is worse than no automation.

### Determinism of render.py

Identical JSON input produces byte-identical SVG output. No timestamps, no `random` without a fixed
seed, no dict iteration over unordered sets. This is what makes the commit guard reliable.

### readme.py

Rewrites only HTML-comment-delimited zones and requires each to match exactly once:

```
<!-- stats:start --> ... <!-- stats:end -->
```

`re.subn` returns a match count; any count other than 1 exits non-zero with a clear message. Text
outside the markers is never touched, so hand-edits survive and a deleted marker fails loudly rather
than silently mangling the file.

## Automation

`.github/workflows/update-profile.yml`:

- `schedule: cron "17 12 * * *"` with `timezone: "Asia/Kolkata"`. The off-hour minute avoids the
  GitHub Actions runner flood at `:00`. IST matches the account owner's location.
- `workflow_dispatch` for manual runs
- `permissions: contents: write` only
- `actions/checkout@v5`, `actions/setup-python@v6`, Python 3.12
- `pip install pytest` is not needed in CI; the pipeline itself has no third-party dependencies
- Auth: `PROFILE_TOKEN` secret when present, otherwise the built-in `GITHUB_TOKEN`. Public data
  works with zero setup; adding a read-only fine-grained PAT later enables private contributions with
  no code change.
- Commit guard: `git diff --cached --quiet || (git commit -m "Refresh profile stats" && git push)`

Secrets are referenced by name only and never written to the repository. GitHub masks them in logs.

## Accessibility

- Every generated SVG root carries `role="img"` with `<title>` and `<desc>` referenced by
  `aria-labelledby`
- Every README `<img>` receives descriptive alt text generated by `readme.py` from the same stats,
  so screen readers encounter the numbers
- The README ends with a collapsed `<details>` block containing the same stats as plain text, making
  the profile useful with images disabled
- `prefers-reduced-motion` disables all animation inside each SVG

## Error handling

| Failure | Behaviour |
|---|---|
| GitHub GraphQL returns `errors` | Raise with joined messages; caught by the merge guard |
| GitHub rate limit or 5xx | Warn, retain previous stats |
| Network timeout | Warn, retain previous stats |
| All sources fail | Exit non-zero, write nothing |
| `c_max == 0` | Flat 8px slabs |
| README zone count != 1 | Exit non-zero with a clear message |
| Rate-limit budget exhausted | GraphQL is two requests per run; no budget concern |

## Testing

`tests/`, pytest, no network access. Every case below protects a specific failure mode identified
during design.

| Test | Guards against |
|---|---|
| Every slice has `width == 880` and `height % 40 == 0` | The entire seam-misalignment class, in one property |
| Larger `c + r` is always drawn later | The projection sign error that shears the skyline |
| 2:1 ratio holds; known `(c, r)` maps to known `(x, y)` | Projection drift |
| `c_max == 0` yields 8px and no `ZeroDivisionError` | New-account crash |
| Same date string yields identical window pattern | Non-determinism |
| Window slides forward; day N's building is unchanged | Pointless daily commits |
| Streak with zero contributions today still counts through yesterday | Streak resetting to 0 every morning until the first commit |
| All-time query emits exactly one alias per active year and is well-formed | Silent history truncation |
| `readme.py` replaces a zone exactly once | Silent README mangling |
| `readme.py` fails loudly on 0 or 2 matches | Same |
| `readme.py` leaves text outside markers untouched | Loss of hand-edits |
| GitHub fetch raising preserves previous values | Profile blanking on a transient API error |
| render.py output is byte-identical across two runs | Spurious commits |

## Repository changes

**Delete:** `assets/cyber-header.svg`, `assets/contribution-city.svg`, `assets/cyber-footer.svg` —
superseded hand-authored assets.

**Add:** `tools/profile/**`, `tests/**`, `.github/workflows/update-profile.yml`, `.gitignore`
entries for `__pycache__` and `.pytest_cache`.

**Rewrite:** `README.md`.

**Commit:** `assets/*.svg` and `tools/profile/data/*.json`. The committed JSON makes
`git log -p tools/profile/data/stats.json` a free archive of the account's stats over time.

## Local development

```
python tools/profile/fetch.py
python tools/profile/render.py
python tools/profile/readme.py
```

Iterates without waiting for Actions. Requires only Python 3.11+ on `PATH`.

## Risks

- **GitHub image caching** masks fixes for several minutes. Expect to see a stale render after
  editing; verify locally before concluding a change did not work.
- **System font variance.** Windows renders Consolas, macOS SF Mono, Linux DejaVu Sans Mono. All are
  acceptable terminal faces, but line lengths will differ slightly across viewers. Centered and
  `text-anchor`-positioned text is unaffected; left-aligned columns may vary by a few pixels.
- **The city is the heaviest asset.** ~227KB served on every profile view.
