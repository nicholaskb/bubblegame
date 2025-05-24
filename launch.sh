#!/bin/bash
set -e

# Build the Docker image
echo "Building Docker image 'bubble-game:py312'..."
docker build -t bubble-game:py312 .

# Allow local containers to connect to your X server
echo "Allowing local containers to access the X11 display..."
xhost +local: || {
    echo "Warning: xhost command failed."
}

# Run the container with X11 forwarding and launch the game
echo "Starting the bubble game container..."
docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/baro/Desktop/FrankieBubble:/app \
  -v /home/baro/Desktop/FrankieBubble/pokemon_dataset:/app/pokemon_dataset \
  --network=host \
  bubble-game:py312 \
  poetry run python /app/bubble_game.py

