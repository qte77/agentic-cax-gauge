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
package's own file listing). The file below is the unminified `build/three.module.js`
verbatim; it is still small enough that the "~1 MB total" budget holds with room to spare.

## Files

| File | Source | Size | sha256 |
|---|---|---|---|
| `three.module.js` | `https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js` | 662,772 B | `9052042d676cb0fdc1ddfefe193053f34b7ac0513a616fdac4535d49987812ea` |
| `examples/jsm/loaders/STLLoader.js` | `https://cdn.jsdelivr.net/npm/three@0.186.1/examples/jsm/loaders/STLLoader.js` | 10,715 B | `023ed97f848b633d8bcd53d4db3b996d29d0c644088700691297c552257d480b` |
| `LICENSE` | `https://cdn.jsdelivr.net/npm/three@0.186.1/LICENSE` | 1,081 B | `8b378ebe60e2fe500158cb0ac71cb5e8b7d92953c2abcc63a0eb90499653b5bc` |

Total vendored payload: ~675 KB.

## Licence

MIT (`LICENSE` in this directory, copied verbatim from the npm package). Compatible with this
repo's Apache-2.0 licence — no action needed beyond carrying the notice, which this directory
does.

## Verifying

```bash
sha256sum viewer/vendor/three.module.js
sha256sum viewer/vendor/examples/jsm/loaders/STLLoader.js
sha256sum viewer/vendor/LICENSE
```

Compare against the table above.

## Updating the pin

1. Download the new version's `build/three.module.js`, `examples/jsm/loaders/STLLoader.js`
   and `LICENSE` from `https://cdn.jsdelivr.net/npm/three@<version>/...` into a fresh empty
   directory (not this one, and not run from inside it).
2. Compute sha256 for each file.
3. Copy the files into this directory, overwriting the old ones.
4. Update the version number and the table above with the new sizes/hashes.
5. Re-run the viewer smoke test (`viewer/README.md`) before committing.
