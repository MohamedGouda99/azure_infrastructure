#!/bin/bash

# Stop and remove all Podman containers
containers=$(sudo podman ps -q)
if [ -n "$containers" ]; then
    for container_id in $containers; do
        sudo podman stop $container_id
        sudo podman rm $container_id
    done
    echo "All Podman containers stopped and removed."
else
    echo "No running Podman containers found."
fi
