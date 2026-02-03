ximport os
import platform
import subprocess

def build_executable(html_file="index.html"):
    separator = ";" if platform.system() == "Windows" else ":"
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--add-data={html_file}{separator}.",
        "main.py"
    ]
    subprocess.run(" ".join(cmd), shell=True)

if __name__ == "__main__":
    build_executable()
