#!/usr/bin/python
import requests
import sys
import re
import subprocess

registry_url = "https://your-docker-registry"
username = "username"
password = "password"

if len(sys.argv) != 4:
    print "Usage: " + sys.argv[0] + " reg_exp_of_repository_to_find reg_exp_of_tag_to_find history_to_maintain"
    print "Example: " + sys.argv[0] + " '^repo/sitor*' '^0.1.*' 2"
    sys.exit(0)

repos2find = sys.argv[1]
tags2find = sys.argv[2]
history2maintain = int(sys.argv[3])

# Get catalog
r = requests.get(registry_url + "/v2/_catalog",
                 auth=(username, password), verify=False)
repositories = r.json()["repositories"]
# For each repository check it matches with $1
for repository in repositories:
    if re.search(repos2find, repository):
        # Get tags
        r = requests.get(registry_url + "/v2/" + repository + "/tags/list",
                         auth=(username, password), verify=False)
        tags = r.json()["tags"]
        # For each tag, check it matches with $2
        matching_tags = []
        for tag in tags:
            if re.search(tags2find, tag):
                matching_tags.append(tag)

        # Sort tags
        # http://stackoverflow.com/questions/2574080/sorting-a-list-of-version-strings
        # but ... the format will be always (\d\.\d\.\d\./?
        # matching_tags.sort(key=lambda s: map(int, s.split('.')))

        # Delete all except $3 last items
        for tag in matching_tags[:-history2maintain]:
            command2run = "/usr/local/bin/delete_docker_registry_image --image " + repository + ":" + tag
            print (("Deleting: " + command2run))
            subprocess.Popen(command2run, shell=True, stdout=subprocess.PIPE).stdout.read()
