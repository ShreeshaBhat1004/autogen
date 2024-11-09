# filename: install_fpdf.py

import subprocess
import sys

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"'{package}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install '{package}'. Error: {e}")

if __name__ == "__main__":
    # Attempt to install the fpdf package
    install('fpdf')