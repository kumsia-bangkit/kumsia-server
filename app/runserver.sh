#!/bin/bash

# Activate the virtual environment
source ../env/Scripts/activate

# Run the Uvicorn server with the specified host and port
uvicorn main:app --reload --host 0.0.0.0 --port 2134
