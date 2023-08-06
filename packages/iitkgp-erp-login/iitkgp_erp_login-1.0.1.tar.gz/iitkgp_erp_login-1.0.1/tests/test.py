import requests
import time
import creds
import iitkgp_erp_login.erp as erp

headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

session = requests.Session()

while True:
    if not erp.session_alive(session):
        erp.login(headers, creds, 2, session)
    else:
        print("Session is alive.")

    time.sleep(2)
