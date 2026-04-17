# LTspice Launch Guide

This document records the process used to run LTspice on Ubuntu through Wine.

## Environment

- Host OS: Ubuntu 24.04.2 LTS
- Wine version: `wine-11.0`
- LTspice executable:
  `~/.wine/drive_c/Program Files/ADI/LTspice/LTspice.exe`

## Launch LTspice

Run:

```bash
wine start /unix "$HOME/.wine/drive_c/Program Files/ADI/LTspice/LTspice.exe"
```

This starts the Windows LTspice executable from the default Wine prefix.

## Shared `.asc` Files

Wine is not running LTspice inside a fully separate virtual machine. Instead, LTspice can access mapped Linux folders directly.

A dedicated shared folder has been created at:

```text
/home/daniel/ltspice-share
```

This folder is mapped inside Wine as:

```text
X:\
```

### Copy a Circuit File into the Shared Folder

Example:

```bash
cp my-circuit.asc /home/daniel/ltspice-share/
```

### Open the Shared Folder from LTspice

1. Launch LTspice.
2. Choose `File` -> `Open`.
3. Navigate to `X:\`.
4. Open the required `.asc` file.

### Direct File Launch Workflow

You can also keep `.asc` files in the shared Linux folder and point LTspice at them from inside Wine.

Example shared path:

```text
X:\my-circuit.asc
```

## Alternative Launch Command

If `wine start` is not suitable, run the executable directly:

```bash
wine "$HOME/.wine/drive_c/Program Files/ADI/LTspice/LTspice.exe"
```

## First-Run Notes

- The first Wine-based launch may take longer than later launches.
- Wine may print `fixme:` messages in the terminal. These are common and do not necessarily indicate a failure.
- The default Wine prefix used here is `~/.wine`.

## Install Context

LTspice was installed from the official Windows MSI into the default Wine prefix.

Installer used:

```bash
/tmp/LTspice64.msi
```

Silent install command:

```bash
wine msiexec /i /tmp/LTspice64.msi /qn
```

## Quick Verification

To confirm the executable exists:

```bash
find "$HOME/.wine/drive_c" -iname "LTspice.exe"
```

Expected result:

```text
/home/daniel/.wine/drive_c/Program Files/ADI/LTspice/LTspice.exe
```

To confirm the shared drive mapping exists:

```bash
find "$HOME/.wine/dosdevices" -maxdepth 1 -type l -printf '%f -> %l\n' | sort | rg '^x:'
```

Expected result:

```text
x: -> /home/daniel/ltspice-share
```

## Troubleshooting

- If Wine has not been installed yet, install Wine first and confirm `wine --version` works.
- If LTspice does not open, retry the direct executable command shown above to surface terminal output.
- If you cannot find your `.asc` file inside LTspice, check whether it was copied into `/home/daniel/ltspice-share` and then browse to `X:\` from the LTspice file dialog.
- If the Wine prefix becomes inconsistent, remove or rename `~/.wine` only if you are prepared to recreate the Wine environment from scratch.
