#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export COPYFILE_DISABLE=1
SOURCE="$(cd "$(dirname "$0")/.." && pwd)"
VERSION=0.1.0
OUTPUT="${1:-$SOURCE/dist}"
mkdir -p "$OUTPUT"
OUTPUT="$(cd "$OUTPUT" && pwd)"
BUILD="$(mktemp -d /private/tmp/brother-native-build.XXXXXX)"
trap 'rm -rf "$BUILD"' EXIT
ROOT="$BUILD/root"
BASE="$ROOT/Library/Printers/leelk/BrotherT220"
BIN="$BASE/versions/$VERSION"
APP="$ROOT/Applications/Brother T220 Native Setup.app"
mkdir -p "$BIN" "$ROOT/Library/Printers/PPDs/Contents/Resources" "$APP/Contents/MacOS" "$APP/Contents/Resources" "$BUILD/scripts"
xcrun clang++ -std=c++17 -arch arm64 -mmacosx-version-min=14.0 -O2 -Wall -Wextra -Werror -pedantic "$SOURCE/cups_filter.cpp" -lcups -o "$BIN/brother-t220-native"
xcrun swiftc -parse-as-library -O -target arm64-apple-macos14.0 "$SOURCE/packaging/Setup.swift" -o "$APP/Contents/MacOS/BrotherT220Setup"
cp "$SOURCE/config/Brother_DCP_T220_Native.ppd" "$ROOT/Library/Printers/PPDs/Contents/Resources/"
cp "$SOURCE/packaging/manage-driver.sh" "$BASE/"
cp "$SOURCE/../LICENSE" "$BASE/LICENSE"
cp "$SOURCE/packaging/preinstall" "$SOURCE/packaging/postinstall" "$BUILD/scripts/"
chmod 755 "$BIN/brother-t220-native" "$BASE/manage-driver.sh" "$BUILD/scripts/"* "$APP/Contents/MacOS/BrotherT220Setup"
cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleIdentifier</key><string>com.leelk.brother-t220-native.setup</string>
<key>CFBundleName</key><string>Brother T220 Native Setup</string>
<key>CFBundleExecutable</key><string>BrotherT220Setup</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleShortVersionString</key><string>$VERSION</string>
<key>CFBundleVersion</key><string>1</string>
<key>LSMinimumSystemVersion</key><string>14.0</string>
<key>NSHighResolutionCapable</key><true/>
</dict></plist>
PLIST
plutil -lint "$APP/Contents/Info.plist"
# The test root resolves the absolute cupsFilter2 path without installing anything.
cupstestppd -W filters -R "$ROOT" "$ROOT/Library/Printers/PPDs/Contents/Resources/Brother_DCP_T220_Native.ppd"
SIGN_ID="${BROTHER_APP_SIGN_IDENTITY:--}"
codesign --force --options runtime --sign "$SIGN_ID" "$BIN/brother-t220-native"
codesign --force --options runtime --sign "$SIGN_ID" "$APP"
codesign --verify --strict "$BIN/brother-t220-native"
codesign --verify --strict "$APP"
# Root ownership is recorded in the package; building does not require root installation.
PKG="$OUTPUT/Brother-T220-Native-$VERSION-development.pkg"
args=(--root "$ROOT" --scripts "$BUILD/scripts" --identifier com.leelk.brother-t220-native --version "$VERSION" --install-location / --ownership recommended --filter '/\._' --filter '/\.DS_Store$')
if [ -n "${BROTHER_INSTALLER_SIGN_IDENTITY:-}" ]; then
    if [ "$SIGN_ID" = - ]; then echo 'Developer ID Application signing is also required for a signed installer.' >&2; exit 1; fi
    args+=(--sign "$BROTHER_INSTALLER_SIGN_IDENTITY")
fi
pkgbuild "${args[@]}" "$PKG"
shasum -a 256 "$PKG"
echo 'Development candidate only. Not notarized; physical tests and supported-OS acceptance remain pending.'
