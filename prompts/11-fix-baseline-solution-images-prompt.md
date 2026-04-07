# Prompt: Fix Image Paths in baseline-solution/baseline-solution.md

## Problem

The file `baseline-solution/baseline-solution.md` contains `<img>` tags with paths like:

```
baseline-solution/data/schematics/images/10-dual-led-flasher.png
```

These paths are relative to the repo root. The file was originally written at the root level and then moved into the `baseline-solution/` directory. Now that it lives at `baseline-solution/baseline-solution.md`, those paths are broken — the images do not render when the file is viewed on GitHub or in any Markdown viewer that resolves paths relative to the file's own location.

## Fix Required

Update every `<img src="...">` tag in `baseline-solution/baseline-solution.md` so the `src` path is relative to the file's current location inside `baseline-solution/`.

### Mapping

| Current (broken) path | Corrected path |
|---|---|
| `baseline-solution/data/schematics/images/10-dual-led-flasher.png` | `data/schematics/images/10-dual-led-flasher.png` |
| `baseline-solution/data/schematics/images/15-triac-timer.png` | `data/schematics/images/15-triac-timer.png` |
| `baseline-solution/data/schematics/images/20-led-chaser.jpg` | `data/schematics/images/20-led-chaser.jpg` |
| `baseline-solution/data/schematics/images/25-transistor-equalizer.png` | `data/schematics/images/25-transistor-equalizer.png` |
| `baseline-solution/data/schematics/images/30-simple-inverter.png` | `data/schematics/images/30-simple-inverter.png` |
| `baseline-solution/data/schematics/images/35-lm386-amplifier.jpg` | `data/schematics/images/35-lm386-amplifier.jpg` |

## Action

1. Open `baseline-solution/baseline-solution.md`.
2. Replace every `src="baseline-solution/data/schematics/images/` with `src="data/schematics/images/`.
3. Verify all six `<img>` tags are updated.
4. Commit and push.
