import subprocess

connector = subprocess.Popen(["python", "app.py"])
ipget = subprocess.Popen(["python", "ip.py"])
ipget.wait()
connector.wait()