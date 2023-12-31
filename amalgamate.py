import os
import sys
import hashlib
import subprocess
import urllib.request

def exec(command, working_directory=None):
    result = subprocess.run(
        command,
        shell=True,
        cwd=working_directory
    )
    if result.returncode != 0:
        raise Exception(f"Command '{command}' failed with exit code {result.returncode}")

def download_file(url, save_path):
    with urllib.request.urlopen(url) as response:
        with open(save_path, 'wb') as file:
            file.write(response.read())

def sha256(file_path):
    hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        # Read the file in chunks to handle large files efficiently
        chunk = 0
        while chunk := file.read(8192):
            hash.update(chunk)
    return hash.hexdigest()

def main():
    # Sanity checks
    if not sys.platform.startswith("win"):
        raise Exception("This script only works on Windows...")
    if not os.path.exists(".git"):
        raise Exception("Clone this repository with git to use it...")

    # Get the current System Informer commit hash
    if not os.path.exists("systeminformer"):
        exec("git submodule update --init")
    commit = subprocess.run(
        "git rev-parse HEAD",
        stdout=subprocess.PIPE,
        text=True,
        shell=True,
        cwd="systeminformer"
    )
    if commit.returncode != 0:
        raise Exception(f"Failed to get commit hash, exit code {commit.returncode}")
    commit_hash = commit.stdout.strip()

    # Download cpp-amalgamate
    cpp_amalgamate = os.path.join(os.getcwd(), "cpp-amalgamate.exe")
    if not os.path.exists(cpp_amalgamate):
        print(f"Downloading cpp-amalgamate...")
        download_file("https://github.com/Felerius/cpp-amalgamate/releases/download/1.0.1/cpp-amalgamate-x86_64-pc-windows-gnu.exe", cpp_amalgamate)
    actual_hash = sha256(cpp_amalgamate)
    expected_hash = "cdb689a610b67f267a1b28733f975431083150f6cd01adfd5914f989508b0522"
    if actual_hash != expected_hash:
        raise Exception(f"cpp-amalgamate.exe hash mismatch (actual: {actual_hash}, expected: {expected_hash})")

    # Extract System Informer license
    license_file = "systeminformer/LICENSE.txt"
    if not os.path.exists(license_file):
        raise Exception(f"License file not found: {license_file}")
    with open(license_file, "r") as f:
        license = f.read().strip()

    # Create output folder
    os.makedirs("out", exist_ok=True)
    with open("out/LICENSE", "w") as f:
        f.write(license)
    out_path = "out/phnt.h"
    exec(f"\"{cpp_amalgamate}\" -d systeminformer/phnt/include phnt_amalgamate.h -o \"{out_path}\"")
    with open(out_path, "r") as f:
        header = f.read()
    with open(out_path, "w") as f:
        f.write("/*\n\n")
        f.write("+===========================================================+\n")
        f.write("|           THIS FILE WAS AUTOMATICALLY GENERATED           |\n")
        f.write("+===========================================================+\n")
        f.write("| Source: https://github.com/winsiderss/systeminformer      |\n")
        f.write(f"| Commit: {commit_hash}          |\n")
        f.write("| Generator: https://github.com/mrexodia/phnt-single-header |\n")
        f.write("+===========================================================+\n\n")
        f.write(license)
        f.write("\n*/\n\n")
        f.write(header)

if __name__ == "__main__":
    main()
