# delete-docker-registry-image

## Install

    curl https://raw.githubusercontent.com/burnettk/delete-docker-registry-image/master/delete_docker_registry_image | sudo tee /usr/local/bin/delete_docker_registry_image >/dev/null
    sudo chmod a+x /usr/local/bin/delete_docker_registry_image

## Run

Optionally, set up your data directory via an environment variable:

    export REGISTRY_DATA_DIR=/opt/registry_data/docker/registry/v2

You can also just edit the script where this variable is set to make it work for your setup.

Almost delete an image:

    delete_docker_registry_image --image testrepo/awesomeimage --dry-run

Actually delete an image (remember to shut down your registry first):

    delete_docker_registry_image --image testrepo/awesomeimage
