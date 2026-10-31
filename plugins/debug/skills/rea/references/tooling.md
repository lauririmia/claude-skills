# Tooling check for the rea skill

Source of truth is REA's own docs (github.com/morluto/rea, `docs/installation.md`). Versions
move quickly; if something here disagrees with `rea doctor`, trust `rea doctor`.

## 1. Node and REA

```bash
node --version   # needs 22.x (>=22.23.4), 24.x (>=24.22.1) or 26.12.1+
npm --version
rea --version || npx --yes rea-agents --help
```

Install if missing (tell the user first):

```bash
npm install --global rea-agents
rea doctor --json
```

Registering REA as an MCP server for an agent is done with `npx rea-agents setup`. It edits agent
configuration (with backups) and needs a restart of the agent afterwards, so only run it if the user
agrees; the `rea` CLI alone is enough for this skill.

On Linux, REA needs a procps-compatible `ps` on `PATH` for process-ownership checks.

## 2. Is a native engine needed?

| Target | Native engine needed? |
|---|---|
| Chrome/Edge extension, Electron app, any JS | No — static JavaScript inspection |
| Website | A Chrome-family browser for observation |
| .NET assemblies | No |
| Native binary (ELF/PE/Mach-O), native modules, firmware | Yes — Ghidra (default), Hopper/IDA/Kuna alternatives |
| Android APK | JADX (headless) and a full JDK |

For a desktop folder whose runtime is unknown, start with REA's `inspect_desktop_application`; it reports
runtime candidates without any native provider.

## 3. Ghidra (only when required)

REA does not install Ghidra. Check:

```bash
echo "$GHIDRA_INSTALL_DIR"; ls "$GHIDRA_INSTALL_DIR/ghidraRun" 2>&1
java -version 2>&1; javac -version 2>&1
```

If missing: download the latest release from github.com/NationalSecurityAgency/ghidra/releases
into a user-writable directory (e.g. `~/tools/`), extract it, install a JDK within the
version bounds that release declares (see its `README.md`; commonly JDK 21 or newer), then
`export GHIDRA_INSTALL_DIR=...` (and `JAVA_HOME` if `java` isn't on PATH), persist it in the shell
profile with the user's consent, and re-run `rea doctor --json` — the `ghidra-*` checks must be
healthy. On macOS arm64 the doctor may report a missing native decompiler; REA's installation doc
describes building `ghidra_opt` from the Ghidra source tree.

Large binaries: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`. Select the engine explicitly with
`--provider ghidra` when more than one is available.

## 4. macOS and Hopper

Hopper Disassembler is commercial (the free demo is time- and feature-limited). Ghidra covers the
same ground for free, so default to Ghidra. Mention Hopper to macOS users only when the target is a
Mach-O binary where Ghidra's result is insufficient, and let the user decide about buying it.
REA can install Hopper but only with explicit approval; don't do that on the user's behalf.

## 5. What to report back

A short table: tool, required?, found/installed, version, notes. Include what you decided *not*
to install and why.
