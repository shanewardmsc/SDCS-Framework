#!/bin/bash

PROGRAM_PATH="/home/openplc/program/Machine_Statistics.st"

echo "[INFO] Waiting for OpenPLC service to start..."
/home/openplc/OpenPLC_v3/openplc start

sleep 3

echo "[INFO] Uploading program..."
/home/openplc/OpenPLC_v3/openplc upload $PROGRAM_PATH

sleep 2

echo "[INFO] Starting PLC runtime..."
/home/openplc/OpenPLC_v3/openplc start runtime

# Keep container alive
tail -f /dev/null

