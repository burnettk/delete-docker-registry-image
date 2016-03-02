# delete-docker-registry-image

## Install

    curl https://raw.githubusercontent.com/burnettk/delete-docker-registry-image/master/delete_docker_registry_image | sudo tee /usr/local/bin/delete_docker_registry_image >/dev/null
    sudo chmod a+x /usr/local/bin/delete_docker_registry_image

## Run

Set up your data directory via an environment variable:

    export REGISTRY_DATA_DIR=/opt/registry_data/docker/registry/v2

You can also just edit the script where this variable is set to make it work for your setup.

Almost delete a repo:

    delete_docker_registry_image --image testrepo/awesomeimage --dry-run

Actually delete a repo (remember to shut down your registry first):

    delete_docker_registry_image --image testrepo/awesomeimage

Delete one tag from a repo:

    delete_docker_registry_image --image testrepo/awesomeimage:supertag


## clean_old_version.py

This complimentary script is made to remove tags in repository based on
regexp pattern.

Usage:

    ./clean_old_versions.py --image reg_exp_of_repository_to_find --include reg_exp_of_tag_to_find -l history_to_maintain

Example:

    ./clean_old_versions.py --image '^repo/sitor*' --include '^0.1.*' -l 2
