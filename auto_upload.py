import os
import qbittorrentapi
import subprocess
import time
import logging

QB_HOST = os.environ.get("QB_HOST", "localhost:8080")
QB_USER = os.environ.get("QB_USER", "admin")
QB_PASS = os.environ.get("QB_PASS", "adminadmin")
DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "/downloads")
RCLONE_REMOTE = os.environ.get("RCLONE_REMOTE", "movies_gdrive:")
SLEEP_INTERVAL = int(os.environ.get("SLEEP_INTERVAL", 60))
LOG_PATH = os.environ.get("QB_LOG_PATH", "/logs")
LOG_FILE = LOG_PATH + os.environ.get("LOG_FILE_NAME", "/qb_upload.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("Automatically movie uploading script has been started")

qb = qbittorrentapi.Client(
    host=QB_HOST,
    username=QB_USER,
    password=QB_PASS
)
qb.auth_log_in()

while True:
    try:
        torrents = qb.torrents_info()
        for torrent in torrents:
            if torrent.progress >= 1.0:
                logging.info(f"{torrent.name} download complete, now uploading to {RCLONE_REMOTE}")

                result = subprocess.run([
                  "rclone",
                  "copy",
                  DOWNLOAD_DIR,
                  RCLONE_REMOTE,
                  "--ignore-existing"  
                ])

                if result.returncode == 0:
                    logging.info(f"{torrent.name} has been uploaded, now delete local document")
                    qb.torrents_delete(torrent_hashes=torrent.hash, delete_files=True)
                else:
                    logging.error(f"{torrent.name} uploaded failed, now retry")
    except Exception as e:
        logging.error(f"something wrong with the script: {e}")

    time.sleep(SLEEP_INTERVAL)
