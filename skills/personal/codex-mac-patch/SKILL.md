---
name: codex-mac-patch
description: >
  Codex Desktop macOS feature unlock — patches app.asar to bypass authMethod
  and Statsig gates, enabling Fast Mode, Computer Use, browser plugins, mobile
  remote, and i18n. Run this skill whenever the user mentions: Codex Desktop
  patch, Codex unlock, Codex Fast Mode not working, Codex features blocked,
  Sparkle update broke patches, re-patch Codex, 解限, codex 补丁, codex 修复,
  codex 快速模式, codex 插件解锁, or any variation of "fix Codex features
  after update." Also trigger when the user asks to patch an Electron app's
  asar for feature gating bypass on macOS.
---

# Codex Desktop Mac Unlock Patch

Patches `/Applications/Codex.app` (Electron) to unlock features gated behind `authMethod==='chatgpt'` or Statsig flags. Works by rewriting `app.asar` with a template-based approach that preserves header structure, unpacked file split, and per-file integrity blocks.

**Platform**: macOS only. Ad-hoc codesign required (drops hardened runtime).

**When to use**: After every Sparkle auto-update, fresh install, or when the user reports blocked features (Fast Mode grayed out, Computer Use unavailable, plugins page auth-blocked).

## Paths

```
CODEX_HOME    = ~/.codex
SKILL_DIR     = ${CODEX_HOME:-$HOME/.codex}/skills/codex-mac-patch, fallback to ~/.claude/skills/codex-mac-patch
SCRIPTS       = SKILL_DIR/scripts
WORK_DIR      = CODEX_HOME/desktop-patch-backup
APP_BUNDLE    = /Applications/Codex.app
APP_ASAR      = APP_BUNDLE/Contents/Resources/app.asar
APP_PLIST     = APP_BUNDLE/Contents/Info.plist
```

## Prerequisites

Before starting, verify:

```bash
# Codex Desktop must NOT be running
pgrep -f Codex.app && echo "ERROR: Quit Codex Desktop first" && exit 1

# App must exist
test -f /Applications/Codex.app/Contents/Resources/app.asar

# Node.js available
node --version

# @electron/asar installed in work directory
test -d ~/.codex/desktop-patch-backup/node_modules/@electron/asar || (
  cd ~/.codex/desktop-patch-backup && npm install @electron/asar
)
```

## Workflow

### Step 1 — Backup

Create timestamped backups of the current official files:

```bash
TS=$(date +%Y%m%d-%H%M%S)
mkdir -p ~/.codex/desktop-patch-backup
cp /Applications/Codex.app/Contents/Resources/app.asar ~/.codex/desktop-patch-backup/app.asar.orig
cp /Applications/Codex.app/Contents/Info.plist ~/.codex/desktop-patch-backup/Info.plist.orig.$TS
cp ~/.codex/config.toml ~/.codex/desktop-patch-backup/config.toml.$TS.bak
codesign -dv /Applications/Codex.app > ~/.codex/desktop-patch-backup/codesign.orig.$TS.txt 2>&1
```

### Step 2 — Discover gates

Run the discovery script to locate gate files by content pattern (hash suffixes change per version):

```bash
CODEX_PATCH_SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/codex-mac-patch"
if [ ! -d "$CODEX_PATCH_SKILL_DIR" ]; then
  CODEX_PATCH_SKILL_DIR="$HOME/.claude/skills/codex-mac-patch"
fi
node "$CODEX_PATCH_SKILL_DIR/scripts/discover.mjs" \
  ~/.codex/desktop-patch-backup/app.asar.orig \
  ~/.codex/desktop-patch-backup
```

This outputs JSON. **All 6 gates must show `"status": "OK"`.** The output includes each gate's `file`, `find`, and `replace` strings — you'll need these for Step 3.

If any gate shows `PATTERN_MISMATCH`, `NOT_FOUND`, or `MULTIPLE_MATCHES`, the minified JS has changed in the new version. Read `references/gate-patterns.md` for the behavioral intent of each gate, then re-investigate by extracting the relevant file from the asar:

```bash
cd ~/.codex/desktop-patch-backup
npx @electron/asar extract-file app.asar.orig <path-from-discovery> /tmp/gate.js
# Then search for the behavioral marker and craft new find/replace
```

### Step 3 — Generate repack.mjs

Create `~/.codex/desktop-patch-backup/repack.mjs` using the template from `references/repack-template.mjs`. The only part that changes per version is the `PATCHES` array — fill it from the discovery output:

```javascript
const PATCHES = [
  { matchEnds: '<filename-from-discovery>', edits: [
    { name: '<gate-name>', find: '<find-from-discovery>', replace: '<replace-from-discovery>' },
  ]},
  // ... one entry per gate from discovery output
];
```

Then run:

```bash
cd ~/.codex/desktop-patch-backup
node repack.mjs ./app.asar.orig ./app.asar.patched
```

Capture the last line: `NEW_HEADER_SHA256=<hash>`. If any patch fails, the script exits with code 2 and prints which patches failed.

### Step 4 — Install, update integrity hash, resign

```bash
# Install patched asar
cp ~/.codex/desktop-patch-backup/app.asar.patched /Applications/Codex.app/Contents/Resources/app.asar

# Update ElectronAsarIntegrity hash (replace <HASH> with NEW_HEADER_SHA256 from Step 3)
/usr/libexec/PlistBuddy -c "Set :ElectronAsarIntegrity:Resources/app.asar:hash <HASH>" \
  /Applications/Codex.app/Contents/Info.plist

# Ad-hoc resign (required — breaks Developer ID signature, drops hardened runtime)
codesign --force --sign - /Applications/Codex.app
```

### Step 5 — Config.toml

Ensure `~/.codex/config.toml` has:

```toml
service_tier = "priority"

[features]
computer_use = true
```

If `[features]` exists with other keys, add `computer_use = true` without overwriting. Back up config before modifying.

### Step 6 — Verify

```bash
open -a /Applications/Codex.app
sleep 5 && pgrep -f Codex.app  # should show a PID
```

Check in the Codex Desktop UI:
- Fast Mode toggle visible and functional
- Computer Use shows "available" (not "statsig-disabled" or "config-requirement-disabled")
- Browser plugin available
- Plugins page accessible (not auth-blocked)
- i18n / locale features enabled

## Rollback

```bash
cp ~/.codex/desktop-patch-backup/app.asar.orig /Applications/Codex.app/Contents/Resources/app.asar
ORIG_HASH=$(plutil -extract ElectronAsarIntegrity.Resources/app.asar.hash raw ~/.codex/desktop-patch-backup/Info.plist.orig)
/usr/libexec/PlistBuddy -c "Set :ElectronAsarIntegrity:Resources/app.asar:hash $ORIG_HASH" /Applications/Codex.app/Contents/Info.plist
codesign --force --sign - /Applications/Codex.app
open -a /Applications/Codex.app
```

Or reinstall the official Codex Desktop.
