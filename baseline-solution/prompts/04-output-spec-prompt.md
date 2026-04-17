# Output Specification — Circuit Schematic Pipeline

For each schematic image you analyse, produce exactly **four files** in `simulations/<agent>/`:

| File | Description |
|------|-------------|
| `<stem>_generated-by-<agent>_falstad.txt` | Falstad plain-text netlist (starts with `$`) |
| `<stem>_generated-by-<agent>_falstad.xml` | Falstad `<cir>` XML format |
| `<stem>_generated-by-<agent>.asc` | LTSpice schematic file |
| `<stem>_generated-by-<agent>_report.md` | Markdown report |

Where `<agent>` is your model identifier and `<stem>` is the image filename without extension.

That's it.
