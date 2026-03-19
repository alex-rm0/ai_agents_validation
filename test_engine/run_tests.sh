#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GBM_LIB="$(ls /nix/store/*mesa-libgbm*/lib 2>/dev/null | head -1)"

if [ -n "$GBM_LIB" ]; then
  export LD_LIBRARY_PATH="${GBM_LIB}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi

export DOTNET_CLI_TELEMETRY_OPTOUT=1

exec dotnet test "$SCRIPT_DIR/FunctionalTests.csproj" --nologo "$@"
