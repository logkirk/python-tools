import urllib.request
import shutil
from requests import get
from os import rename, remove
from pathlib import Path
from plyer import notification

VERSION_URL = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
DOWNLOAD_URL_TEMPLATE = (
    "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip"
)
PROXY_DICT = {"http": "http://", "https": "http://"}
CHROMEDRIVER_FILE_NAME = "chromedriver.exe"
CHROMEDRIVER_DIR = r""
VERSION_RECORD_PATH = r""
VERSION_RECORD_BKP_PATH = r""

version = get(VERSION_URL, proxies=PROXY_DICT).text
download_url = DOWNLOAD_URL_TEMPLATE.format(version)
print("Latest chromedriver version found: {}".format(version))

# Check for version difference
old_version = None
try:
    with open(VERSION_RECORD_PATH, "r+") as f:
        old_version = f.read()
except FileNotFoundError:
    pass
if old_version == version:
    print("Done. No update available.")
    exit()

# Back up old chromedriver
print("Backing up old chromedriver...")
chromedriver_path = Path(CHROMEDRIVER_DIR, CHROMEDRIVER_FILE_NAME)
chromedriver_backup_path = Path(CHROMEDRIVER_DIR, CHROMEDRIVER_FILE_NAME).with_suffix(
    chromedriver_path.suffix + ".bkp"
)
try:
    remove(chromedriver_backup_path)
except FileNotFoundError:
    pass
try:
    rename(src=chromedriver_path, dst=chromedriver_backup_path)
except FileNotFoundError:
    pass

# Download new chromedriver
proxy_handler = urllib.request.ProxyHandler(PROXY_DICT)
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
with urllib.request.urlopen(download_url) as response, open(
    chromedriver_path, "wb"
) as out_file:
    shutil.copyfileobj(response, out_file)

with open(VERSION_RECORD_PATH, "w") as f:
    f.write(version)
if old_version is not None:
    with open(VERSION_RECORD_BKP_PATH, "w") as f:
        f.write(old_version)
notification.notify(
    title="Chromedriver updated",
    message="Chromedriver updated to version {}".format(version),
    timeout=10,
)

print("Done. Chromedriver updated.")
