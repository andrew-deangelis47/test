# This script checks for new tags and if a new release tag is found, will build a release image
# Expects the format: release/customer_name/version_number
# Ex: release/metalcraft/1.0

import os
import json
import sys

payload = os.environ.get('BITBUCKET_PAYLOAD')
if not payload:
    raise ValueError("Bitbucket payload not found! Not starting job")
payload_dict = json.loads(payload)
if "push" in payload_dict and "changes" in payload_dict["push"] and len(payload_dict["push"]["changes"]) > 0:
    tag = payload_dict["push"]["changes"][0]["new"]["name"]
    if "release/" not in tag:
        print("release/ not in tag, exiting")
        sys.exit(0)
    customer_name = tag.split("/")[1]
    git_repo = f"git@bitbucket.org:paperlessparts/{customer_name}.git"
    os.system(f"git clone {git_repo}")
    os.chdir(customer_name)
    # replace https w ssh gitmodule
    os.system("perl -i -p -e 's|https://(.*?)/|git@\1:|g' .gitmodules")
    os.system("git submodule sync")
    os.system("git submodule update --init --remote --merge")
    os.chdir("integrations")
    os.system("git fetch --all")
    os.system(f"git checkout {tag}")
    os.chdir("..")
    x = os.system(f"bash integrations/push.sh {customer_name} pushrelease")
    if x != 0:
        print("Docker build and push exited with: " + x)
        sys.exit(1)
else:
    raise ValueError("Bitbucket payload was malformed. Please try again")
