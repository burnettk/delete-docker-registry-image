# delete-docker-registry-image

## Install

    curl https://raw.githubusercontent.com/burnettk/delete-docker-registry-image/master/delete_docker_registry_image.py | sudo tee /usr/local/bin/delete_docker_registry_image >/dev/null
    sudo chmod a+x /usr/local/bin/delete_docker_registry_image

## Run

Set up your data directory via an environment variable:

    export REGISTRY_DATA_DIR=/opt/registry_data/docker/registry/v2

You can also just edit the script where this variable is set to make it work
for your setup.

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

## Run tests for this project

    ./test/start_up_vagrant_box_for_running_tests
    vagrant ssh
    cd /vagrant
    ./test/clean_and_run

Known test-passing configurations:
 1. docker: 1.9.1, registry:2.2.1

Known test-failing configurations:
 1. docker: 1.10.2, registry:2.2.1
 2. docker: 1.10.2, registry:2.3.0

When tests are run with a new docker daemon and an older registry,
architecture-specific config files are created, but they are not referenced
anywhere, so tests fail when we delete a tag or repo and expect all files to be
deleted, but these architecture-specific config files are still hanging around.
With the newer registry, these config files are referenced in the schema
version 2 manifest, so we can easily delete them. It's probably best to avoid
use of this script with the version combinations that fail tests.
