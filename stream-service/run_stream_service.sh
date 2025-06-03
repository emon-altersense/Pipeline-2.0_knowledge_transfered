#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the base directory (Pipeline-2.0) and stream-service directory
BASE_DIR="$SCRIPT_DIR/.."
STREAM_SERVICE_DIR="$BASE_DIR/stream-service"

# Ensure we're in the stream-service directory
if [[ ! -d "$STREAM_SERVICE_DIR" ]]; then
  echo "Error: stream-service directory not found."
  exit 1
fi

# Remove and recreate the build directory safely
BUILD_DIR="$STREAM_SERVICE_DIR/build"
rm -rf "$BUILD_DIR" && mkdir -p "$BUILD_DIR"

# Navigate to the build directory
cd "$BUILD_DIR" || { echo "Failed to change directory to $BUILD_DIR"; exit 1; }

# Run CMake and Ninja
cmake -G Ninja .. && ninja && ./stream-service
