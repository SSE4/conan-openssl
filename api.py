from __future__ import print_function
import requests
from requests.auth import HTTPBasicAuth
import os
import time
import sys
import ssl
import platform
import ctypes
import socket

print("sys version", sys.version_info)
print("platform version", platform.python_version())
print("SSL version", ssl.OPENSSL_VERSION)


class _OSVERSIONINFOEXW(ctypes.Structure):
    _fields_ = [('dwOSVersionInfoSize', ctypes.c_ulong),
                ('dwMajorVersion', ctypes.c_ulong),
                ('dwMinorVersion', ctypes.c_ulong),
                ('dwBuildNumber', ctypes.c_ulong),
                ('dwPlatformId', ctypes.c_ulong),
                ('szCSDVersion', ctypes.c_wchar * 128),
                ('wServicePackMajor', ctypes.c_ushort),
                ('wServicePackMinor', ctypes.c_ushort),
                ('wSuiteMask', ctypes.c_ushort),
                ('wProductType', ctypes.c_byte),
                ('wReserved', ctypes.c_byte)]

os_version = _OSVERSIONINFOEXW()
os_version.dwOSVersionInfoSize = ctypes.sizeof(os_version)
if hasattr(ctypes, "windll"):
    retcode = ctypes.windll.Ntdll.RtlGetVersion(ctypes.byref(os_version))

    print(os_version.dwMajorVersion,
          os_version.dwMinorVersion,
          os_version.dwBuildNumber,
          os_version.dwPlatformId,
          os_version.szCSDVersion,
          os_version.wServicePackMajor,
          os_version.wServicePackMinor,
          os_version.wSuiteMask,
          os_version.wProductType,
          os_version.wReserved)

def do_sleep(count):
    for i in range(0, count):
        time.sleep(1)
        sys.stdout.write(".")
        sys.stdout.flush()

class HTTPAdapterWithSocketOptions(requests.adapters.HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.socket_options = kwargs.pop("socket_options", None)
        super(HTTPAdapterWithSocketOptions, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_options is not None:
            kwargs["socket_options"] = self.socket_options
        super(HTTPAdapterWithSocketOptions, self).init_poolmanager(*args, **kwargs)

adapter = HTTPAdapterWithSocketOptions(socket_options=[(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)])

s = requests.Session()

s.mount("http://", adapter)
s.mount("https://", adapter)

def make():

    #url = "https://api.bintray.com/conan/conan-community/conan/v1/users/authenticate"
    #url = "https://google.com"
    url = "https://bintray.com"

    headers = {
        'X-Client-Anonymous-Id': '43eaa1e46ddfbeeb50abdcee05c580e260df073f',
        'X-Client-Id': 'conanbot',
        'User-Agent': 'Conan/1.17.0-dev (Python 3.7.3) python-requests/2.22.0'
        }
    auth = HTTPBasicAuth('conanbot', os.environ["CONAN_PASSWORD"])
    timeout = 60

    r = s.get(url, headers=headers, timeout=timeout, auth=auth)
    print(r.status_code)

hostname = 'bintray.com'
port = 80

request = b"GET / HTTP/1.1\nHost: %s\n\n" % hostname
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname, port))

def make2():
    s.send(request)
    result = s.recv(10000)
    print(result)

make2()
do_sleep(310)
make2()
