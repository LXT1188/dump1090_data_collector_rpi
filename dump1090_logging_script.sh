#!/bin/bash

# Function to handle ctrl-c. trap function introduces a signal handler that does something related to the script when the signal is received. The signal will kill DUMP1090_PID and DATA_RECORDER_PID when the signal is received, and then exit the script. The "INT" keyword specifies that Ctrl-C is the signal to be listening for.
trap 'kill $DUMP1090_PID $DATA_RECORDER_PID; exit' INT 

# Navigate to the dump1090 directory and start dump1090 in the background
cd dump1090/dump1090
./dump1090 --interactive  --net --metric & 
DUMP1090_PID=$!

# Navigate to the data_collector directory and start the data recorder
cd ./data_collector/venv_data_collector
python dump1090_data_recorder.py &
DATA_RECORDER_PID=$!

# Wait for both processes to finish - not needed but just in case
wait $DUMP1090_PID $DATA_RECORDER_PID
