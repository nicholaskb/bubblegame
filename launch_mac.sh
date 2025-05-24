#!/bin/bash
set -e

# Build the Docker image
echo "Building Docker image 'pokemon-game'..."
docker build -t pokemon-game .

# Run the container with X11 forwarding
echo "Starting the game container..."
docker run --rm -it \
  -e DISPLAY=host.docker.internal:0 \
  -v "$(pwd):/app" \
  --network host \
  pokemon-game 