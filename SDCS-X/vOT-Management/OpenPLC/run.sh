#!/bin/bash

# Navigate to the OpenPLC directory
cd /home/openplc/OpenPLC_v3

# Start OpenPLC runtime with your .st file
./openplc -r webserver/st_files/Machine_Statistics.st

