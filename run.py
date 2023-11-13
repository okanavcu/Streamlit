import os
import subprocess
import sys

def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

if __name__ == "__main__":
    # Streamlit uygulamasını çalıştır
    subprocess.run(
        ["streamlit", "run", resolve_path("AnaSayfa.py"), "--global.developmentMode=false"],
        creationflags=subprocess.CREATE_NO_WINDOW,  # Konsol penceresini gizle
    )
