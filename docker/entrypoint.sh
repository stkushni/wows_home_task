#!/usr/bin/env bash
set -euo pipefail

python docker/init_db.py

DEFAULT_CMD=("pytest" "-v" "--alluredir=/app/allure-results")
if [ "$#" -gt 0 ]; then
  CMD=("$@")
else
  CMD=("${DEFAULT_CMD[@]}")
fi

KEEP_ALIVE=${KEEP_CONTAINER_ALIVE:-1}
PYTEST_STATUS_FILE=/tmp/pytest_exit_code

if [ "$KEEP_ALIVE" = "1" ]; then
  set +e
  "${CMD[@]}"
  status=$?
  set -e
  echo "$status" > "$PYTEST_STATUS_FILE"
  cat <<MSG
============================================================
Pytest finished with exit code: $status
Results are stored in /app/allure-results.
The last exit code is saved in $PYTEST_STATUS_FILE.
You are now in an interactive shell. Type 'exit' when done.
============================================================
MSG
  exec "/bin/bash"
else
  exec "${CMD[@]}"
fi
