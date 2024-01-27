import subprocess

packages_to_install = ["discord.py", "python-dotenv", "google-auth-oauthlib","google-api-python-client"]

for package in packages_to_install:
    subprocess.call(["pip", "install", package])

from main import run
run()