"""
CourseCraft AI — Main Entry Point
Run `streamlit run coursecraft/app.py` or `python main.py` to start the studio.
"""

import sys
import subprocess


def main():
    print("🚀 Starting CourseCraft AI Studio on port 8503...")
    cmd = [sys.executable, "-m", "streamlit", "run", "coursecraft/app.py", "--server.port", "8503"]
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
