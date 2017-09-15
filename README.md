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


## clean_old_versions.py

This complimentary script is made to remove tags in repository based on
regexp pattern.

Usage:

    ./clean_old_versions.py --image reg_exp_of_repository_to_find --include reg_exp_of_tag_to_find -l history_to_maintain --registry-url location_of_docker_registry -o tag_ordering -b only_tags_before_date -a only_tags_after_date

Example:
Search for all images whose name start with 'repo/sitor' and delete all tags
whose name start with '0.1.' keeping the last 2 tags and of the remaining tags
deletes only those having an image creation time between January 1, 2016 12 a.m.
and June 25, 2016 12 p.m. (both datetimes are exclusive).

    ./clean_old_versions.py --image '^repo/sitor*' --include '^0.1.*' -l 2 -b 2016-06-25T12:00:00 -a 2016-01-01T00:00:00 --registry-url http://localhost:5000

Add `--dry-run` as argument for a test run without actual removal of tags.

## Run tests for this project

    ./test/start_up_vagrant_box_for_running_tests
    vagrant ssh
    cd /vagrant
    ./test/clean_and_run

Known test-passing configurations:
 1. docker: 1.9.1, registry:2.2.1
 2. docker: 1.10.2, registry:2.3.0
 1. docker: 1.11.2, registry:2.3.0
 1. docker: 1.12.1, registry:2.5.0

Known test-failing configurations:
 1. docker: 1.10.2, registry:2.2.1

When tests are run with a new docker daemon and an older registry,
architecture-specific config files are created, but they are not referenced
anywhere, so tests fail when we delete a tag or repo and expect all files to be
deleted, but these architecture-specific config files are still hanging around.
With the newer registry, these config files are referenced in the schema
version 2 manifest, so we can easily delete them. It's probably best to avoid
use of this script with the version combinations that fail tests.

## Alternatives

Docker is building or has built much of this functionality in newer versions of
docker and the registry.

The ability to delete the metadata for a manifest was added in registry:2.2. Make
sure you give the registry the environment variable
REGISTRY_STORAGE_DELETE_ENABLED=true. Follow the instructions at
https://github.com/docker/docker-registry/issues/988#issuecomment-224280919 to
delete a tag by name. Once the metadata is deleted, follow the instructions at
https://github.com/docker/distribution/blob/master/docs/configuration.md to run
garbage collection, which will clean up the binary data (the big stuff).
