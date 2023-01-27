#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser();
parser.add_argument("port_name", type=str)
parser.add_argument("port_version", type=str)

args = parser.parse_args()

print("port_name: " + args.port_name)
print("port_version: " + args.port_version)

versions_dir = args.port_name[0] + "-"

vcpkg_json_path = Path("ports") / args.port_name / "vcpkg.json"
portfile_path = Path("ports") / args.port_name / "portfile.cmake"
port_versions_path = Path("versions") / versions_dir / (args.port_name + ".json")
baseline_path = Path("versions/baseline.json")

with open(vcpkg_json_path, "r") as F:
    vcpkg_json = json.load(F)

with open(portfile_path, "r") as F:
    portfile = F.read()

with open(port_versions_path, "r") as F:
    port_versions = json.load(F)

with open(baseline_path, "r") as F:
    baseline = json.load(F)

# Say we get a job kicked off for beicode because there has been a new tag made
# in that repository. Order of updates:
#   1. Replace the SHA in the portfile.cmake to pull the commit of the new tag.
#   2. Update version in vcpkg.json
#   3. Make a git commit and grab the git_tag = "git rev-parse HEAD:ports/<port_name>"
#   4. Add a new version in port_versions with the git_tag.
#   5. Update the baseline version number in baseline.json
#   6. Make a git commit
#   7. Print the "git rev-parse HEAD" to be used in the package's vcpkg.json
#      and vcpkg-configuration.json
#
# Stretch:
#   How can we now automatically update the packages that rely on this to
#   update their vcpkg.json and vcpkg-configuration.json? Is this even
#   necessary?
