# Vendored three.js

Pinned, offline, deterministic — no CDN fetch at render time (plan
[`docs/plans/001-v0.md`](../../docs/plans/001-v0.md) §9.2). Downloaded into a fresh empty
directory, sha256'd, then copied in; the hashes below were recomputed independently after the
copy and matched.

## Version

`three@0.186.1` (published 2026-09-24 per the npm registry — chosen as a recent, already-aged
stable release, not the bleeding-edge tip).

**Deviation from the usual `three.module.min.js` name:** as of this release three.js no longer
ships a minified ESM build in the npm package (`build/` contains only `three.module.js`,
`three.core.js`, `three.cjs`, the WebGPU builds and `three.tsl.js` — confirmed against the
package's own file listing). The files below are the unminified `build/three.module.js` and
`build/three.core.js` verbatim (the npm/ESM build is split across these two files —
`three.module.js` re-exports everything from `./three.core.js`, which `index.html`'s import
map does not need to know about: that relative import is resolved by the browser against
`three.module.js`'s own URL, so `three.core.js` only has to sit next to it on disk).

**Deliberately not using jsdelivr's on-the-fly `.min.js` minification.** jsdelivr can minify
any file by requesting a `.min.js` URL (confirmed: `three.module.min.js` and
`three.core.min.js` both resolve, ~390 KB + ~416 KB ≈ 810 KB combined — under the original
budget). Rejected anyway: those bytes are generated per-request by jsdelivr's own Terser
pass, not an artifact three.js publishes — nothing to pin against a release, only against
"whatever jsdelivr's minifier did this month." Worse, `three.module.min.js`'s minified source
still contains the literal, unrewritten string `./three.core.js` (jsdelivr minifies one file
at a time; it does not rewrite cross-file import specifiers) — so using it would force a file
named `three.core.js` whose *content* is actually the minified `three.core.min.js` output, a
name/content mismatch this repo's own clarity principle (name things for what they are) rules
out. If the ~1 MB budget ever becomes a hard constraint, that pair is the documented fallback;
for now, unminified and verifiably-official wins.

## Files

| File | Source | Size | sha256 |
|---|---|---|---|
| `three.module.js` | `https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js` | 662,772 B | `9052042d676cb0fdc1ddfefe193053f34b7ac0513a616fdac4535d49987812ea` |
| `three.core.js` | `https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.core.js` | 1,458,113 B | `9edde002b066a9a05676a6127f67735b62baf399bdea529f2f7e31657da769e6` |
| `examples/jsm/loaders/STLLoader.js` | `https://cdn.jsdelivr.net/npm/three@0.186.1/examples/jsm/loaders/STLLoader.js` | 10,715 B | `023ed97f848b633d8bcd53d4db3b996d29d0c644088700691297c552257d480b` |
| `LICENSE` | `https://cdn.jsdelivr.net/npm/three@0.186.1/LICENSE` | 1,081 B | `8b378ebe60e2fe500158cb0ac71cb5e8b7d92953c2abcc63a0eb90499653b5bc` |

Total vendored payload: ~2.1 MB (`three.module.js` + `three.core.js` together are the full
ESM runtime; this is roughly double the brief's original "~1 MB is fine" estimate, which
assumed a minified build ships from npm — it does not, for any currently-maintained release).
Still small in absolute terms; see the minification note above for a documented, smaller
fallback if this budget is ever enforced as a hard limit.

## Licence

MIT (`LICENSE` in this directory, copied verbatim from the npm package). Compatible with this
repo's Apache-2.0 licence — no action needed beyond carrying the notice, which this directory
does.

## Verifying

```bash
sha256sum viewer/vendor/three.module.js
sha256sum viewer/vendor/three.core.js
sha256sum viewer/vendor/examples/jsm/loaders/STLLoader.js
sha256sum viewer/vendor/LICENSE
```

Compare against the table above.

## Updating the pin

1. Download the new version's `build/three.module.js`, `build/three.core.js`,
   `examples/jsm/loaders/STLLoader.js` and `LICENSE` from
   `https://cdn.jsdelivr.net/npm/three@<version>/...` into a fresh empty directory (not this
   one, and not run from inside it).
2. Compute sha256 for each file.
3. Copy the files into this directory, overwriting the old ones.
4. Update the version number and the table above with the new sizes/hashes.
5. Re-run the viewer smoke test (`viewer/README.md`) before committing.
