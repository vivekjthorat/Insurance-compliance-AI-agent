import os
import subprocess

def run_app():
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    run_app() 