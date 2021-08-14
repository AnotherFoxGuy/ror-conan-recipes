#!/usr/bin/env python3
import os, sys
import platform
from glob import glob
import yaml
import subprocess

def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)


dirs = glob("./*/")

packages = []

for p in dirs:
    path = f'{p}/config.yml'
    if not os.path.isfile(path):
        continue
    with open(path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

        for val in config.values():
            for v, y in val.items():
                packages.append(f"{p}{y['folder']} {v}@anotherfoxguy/stable")

for pkg in packages:
    system(f"conan export {pkg}")

for pkg in packages:
    system(f"conan create {pkg} -s=build_type=Release -k -b=missing")
    system(f"conan create {pkg} -s=build_type=Debug   -k -b=missing")


data = list(filter(lambda k: 'anotherfoxguy' in k, subprocess.run(['conan','search','*','--raw'], stdout=subprocess.PIPE).stdout.decode("utf-8").split()))

for d in data:
    system(f"conan upload {d} -r ror-v2 --all --force")