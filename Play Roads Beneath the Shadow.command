#!/bin/zsh

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required to play Roads Beneath the Shadow."
  echo "Install Python 3, then open this launcher again."
  read -r "?Press Return to close..."
  exit 1
fi

python3 -m roads_beneath_shadow
STATUS=$?

if [[ $STATUS -ne 0 ]]; then
  echo
  echo "The game stopped with an error (code $STATUS)."
  read -r "?Press Return to close..."
fi

exit $STATUS
