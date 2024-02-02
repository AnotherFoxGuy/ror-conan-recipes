#!/usr/bin/env python3
import os
import yaml
from git import Repo
import re
from conan.api.conan_api import ConanAPI


def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)


conan_profile = os.getenv("CONAN_PROFILE") or "ubuntu-release"
conan = ConanAPI()

regex = r'name *= *"([\w-]+)"$'

dirs = []
packages = []

repo = Repo(os.getcwd())

for c in repo.head.commit.stats.files:
    if (
        c.endswith("conanfile.py")
        or c.endswith("conandata.yml")
        or c.endswith("config.yml")
    ):
        dirs.append(c.split("/")[0])

dirs = list(dict.fromkeys(dirs))

for p in dirs:
    path = os.path.join(os.getcwd(), p, "config.yml")
    if not os.path.isfile(path):
        continue
    with open(path) as file:
        config = yaml.safe_load(file)

        for val in config["versions"].items():
            version = val[0]
            folder = val[1]["folder"]

            cpath = os.path.join(os.getcwd(), p, folder, "conanfile.py")
            with open(cpath) as cf:
                name = re.findall(regex, cf.read(), re.MULTILINE)[0]

            r, _ = conan.export.export(
                name=name,
                path=cpath,
                version=version,
                user="anotherfoxguy",
                channel="stable",
            )
            packages.append(r.repr_notime())


for pkg in packages:
    print(pkg)
    f = open("conanfile.txt", "w")
    f.write(f"[requires]\n{pkg}")
    f.close()
    system(
        f'conan install . -pr="./.conan-profiles/{conan_profile}" -b=missing -of tmp -c tools.system.package_manager:mode=install -c tools.system.package_manager:sudo=True'
    )

for pkg in packages:
    system(f"conan upload {pkg} -r rigs-of-rods-deps")
