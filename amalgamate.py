import os
import sys
import shutil
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
    if not sys.platform.startswith("win"):
        raise Exception("This script only works on Windows...")
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
    license_file = "systeminformer/LICENSE.txt"
    if not os.path.exists(license_file):
        raise Exception(f"License file not found: {license_file}")
    with open(license_file, "r") as f:
        license = f.read().strip()
    cpp_amalgamate = os.path.join(os.getcwd(), "cpp-amalgamate.exe")
    if not os.path.exists(cpp_amalgamate):
        print(f"Downloading cpp-amalgamate...")
        download_file("https://github.com/Felerius/cpp-amalgamate/releases/download/1.0.1/cpp-amalgamate-x86_64-pc-windows-gnu.exe", cpp_amalgamate)
    actual_hash = sha256(cpp_amalgamate)
    expected_hash = "cdb689a610b67f267a1b28733f975431083150f6cd01adfd5914f989508b0522"
    if actual_hash != expected_hash:
        raise Exception(f"cpp-amalgamate.exe hash mismatch (actual: {actual_hash}, expected: {expected_hash})")
    os.makedirs("out", exist_ok=True)
    out_path = os.path.join(os.getcwd(), "out", "phnt.h")
    exec(f"\"{cpp_amalgamate}\" -d . phnt_windows.h phnt.h -o \"{out_path}\"", "systeminformer/phnt/include")
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
