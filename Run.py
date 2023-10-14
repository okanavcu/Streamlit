import os
import subprocess

os.system(".\\.venv\\Scripts\\activate")
subprocess.run(["streamlit run SGK.py --server.enableWebsocketCompression=false --server.runOnSave"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)