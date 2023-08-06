import re
import subprocess

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa


def install_package(package_name: str) -> bool:
    if re.search(r"[|&;\\]", package_name):
        ic()
        return False
    package_name = re.sub(r"\s+", "", package_name)

    command = f"pip install {package_name}"
    print(f"running `{command}`")
    if subprocess.run(
        ["pip", "install", package_name], shell=False
    ).returncode:
        ic()
        return False
    return True
