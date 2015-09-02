# delete-docker-registry-image

## Install

curl https://raw.githubusercontent.com/burnettk/delete-docker-registry-image/master/delete_docker_registry_image | sudo tee /usr/local/bin/delete_docker_registry_image >/dev/null
sudo chmod a+x /usr/local/bin/delete_docker_registry_image

## Run

REGISTRY_DATA_DIR=/opt/registry_data/docker/registry/v2 delete_docker_registry_image --image testrepo/awesomeimage --dry-run
