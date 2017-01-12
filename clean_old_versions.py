#!/usr/bin/env python
from __future__ import print_function
import re
import subprocess
import argparse
from distutils.version import LooseVersion
import requests


def main():
    """cli entrypoint"""
    parser = argparse.ArgumentParser(description="Cleanup docker registry")
    parser.add_argument("-e", "--exclude",
                        dest="exclude",
                        help="Regexp to exclude tags")
    parser.add_argument("-E", "--include",
                        dest="include",
                        help="Regexp to include tags")
    parser.add_argument("-i", "--image",
                        dest="image",
                        required=True,
                        help="Docker image to cleanup")
    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="verbose")
    parser.add_argument("-u", "--registry-url",
                        dest="registry_url",
                        default="http://localhost",
                        help="Registry URL")
    parser.add_argument("-s", "--script-path",
                        dest="script_path",
                        default="/usr/local/bin/delete_docker_registry_image",
                        help="delete_docker_registry_image full script path")
    parser.add_argument("-l", "--last",
                        dest="last",
                        default=5,
                        type=int,
                        help="Keep last N tags")
    parser.add_argument("-U", "--user",
                        dest="user",
                        help="User for auth")
    parser.add_argument("-P", "--password",
                        dest="password",
                        help="Password for auth")
    parser.add_argument("--no_check_certificate",
                        action='store_false')
    parser.add_argument("--dry-run",
                        dest='dry_run',
                        action='store_true',
                        help="Dry run - show which tags would have been deleted but do not delete them")
    args = parser.parse_args()

    # Get catalog
    if args.user and args.password:
        auth = (args.user, args.password)
    else:
        auth = None
    response = requests.get(args.registry_url + "/v2/_catalog",
                            auth=auth, verify=args.no_check_certificate)
    repositories = response.json()["repositories"]
    # For each repository check it matches with args.image
    for repository in repositories:
        if re.search(args.image, repository):
            # Get tags
            response = requests.get(args.registry_url + "/v2/" + repository + "/tags/list",
                                    auth=auth, verify=args.no_check_certificate)
            tags = response.json()["tags"]
            # For each tag, check it does not matches with args.exclude
            matching_tags = []
            for tag in tags:
                if not args.exclude or not re.search(args.exclude, tag):
                    if not args.include or re.search(args.include, tag):
                        matching_tags.append(tag)

            # Sort tags
            matching_tags.sort(key=lambda s: LooseVersion(re.sub('[^0-9.]', '9', s)))

            # Delete all except N last items
            if args.last > 0:
                tags_to_delete = matching_tags[:-args.last]
            else:
                tags_to_delete = matching_tags
            for tag in tags_to_delete:
                command2run = "{0} --image {1}:{2}". \
                    format(args.script_path, repository, tag)
                if args.dry_run :
                    print("Simulate deletion of {0}:{1}".format(repository, tag))
                    command2run += " --dry-run"
                print("Running: {0}".format(command2run))
                out = subprocess.Popen(command2run, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT).stdout.read()
                print(out)


if __name__ == '__main__':
    main()
