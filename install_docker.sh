#!/usr/bin/env bash

set -e

# get.docker.com unfortunately no longer accepts a version
# curl -sSL https://get.docker.com | DOCKER_VERSION=1.11.2 sh

# apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
mkdir -p /etc/apt/sources.list.d
echo deb https://apt.dockerproject.org/repo ubuntu-trusty main > /etc/apt/sources.list.d/docker.list
apt-get update

# pick your docker version:
# apt-get install -y -q docker-engine=1.10.2-0~trusty
apt-get install -y -q docker-engine=1.11.2-0~trusty
# apt-get install -y -q docker-engine # latest

usermod -aG docker vagrant
