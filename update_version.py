import re
import sys

from new_app import __version__

if __version__ == "0+unknown":
    print("No commits made to this repo. Using whatever is defined in pyproject")
    sys.exit()
re_version = re.search(r"^\d+\.\d+\.\d+\.post(\d+)", __version__)
if re_version is None:
    raise ValueError(
        "Version from versioneer not in supported format. Check if you have set a tag with the version number, which is what versioneer uses to create the version number."
    )
num_post_versioneer = re_version.groups()[0]

# update pyproject
with open("pyproject.toml") as f:
    data = f.readlines()
for i, line in enumerate(data):
    re_project_version = re.search(
        r"^version = \"\d+\.\d+\.\d+(?:\.post(\d+).+)?\"\n$", line
    )
    if re_project_version is None:
        continue
    num_pos_pyproject = re_project_version.groups()[0]
    if not (
        int(num_post_versioneer) > 0 and num_pos_pyproject is None
    ):  # non-production version as it includes the dev version info
        data[i] = f'version = "{__version__}"\n'
        print(f"Updated pyproject version to {__version__}")
        with open("pyproject.toml", "w") as f:
            f.write("".join(data))
    break
assert re_project_version is not None
