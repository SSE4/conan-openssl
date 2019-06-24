import requests
from requests.auth import HTTPBasicAuth
import os
import time
import sys

def do_sleep(count):
    for i in range(0, count):
        time.sleep(1)
        sys.stdout.write(".")
        sys.stdout.flush()

s = requests.Session()

def make():

    url = "https://api.bintray.com/conan/conan-community/conan/v1/users/authenticate"

    headers = {
        'X-Client-Anonymous-Id': '43eaa1e46ddfbeeb50abdcee05c580e260df073f',
        'X-Client-Id': 'conanbot',
        'User-Agent': 'Conan/1.17.0-dev (Python 3.7.3) python-requests/2.22.0'
        }
    auth = HTTPBasicAuth('conanbot', os.environ["CONAN_PASSWORD"])
    timeout = 60

    r = s.get(url, headers=headers, timeout=timeout, auth=auth)
    print(r.status_code)


make()
do_sleep(310)
make()
