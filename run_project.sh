#!/bin/bash
set -e

echo "Creating tables and importing data..."
python read_data.py
echo "Done."

echo "Running queries..."
python queries.py
echo "All queries finished running."