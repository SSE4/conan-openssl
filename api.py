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


socket_options=[(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
if hasattr(socket, "SIO_KEEPALIVE_VALS"):
    print("set SIO_KEEPALIVE_VALS")
adapter = HTTPAdapterWithSocketOptions(socket_options=socket_options)

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

request = b"GET / HTTP/1.1\nHost: %s\n\n" % hostname.encode()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if hasattr(socket, "TCP_KEEPIDLE"):
    print("set TCP_KEEPIDLE")
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 120)
if hasattr(socket, "TCP_KEEPINTVL"):
    print("set TCP_KEEPINTVL")
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30)
if hasattr(socket, "TCP_KEEPCNT"):
    print("set TCP_KEEPCNT")
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 8)
#if hasattr(socket, "SIO_KEEPALIVE_VALS"):
#    print("set SIO_KEEPALIVE_VALS")
#    socket.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 120 * 1000, 30 * 1000))

if os_version.dwMajorVersion == 10 and os_version.dwBuildNumber >= 15063:  # Windows 10 1703
    TCP_KEEPIDLE = 3
    TCP_KEEPINTVL = 17
    print("set TCP_KEEPIDLE (Windows)")
    sock.setsockopt(socket.IPPROTO_TCP, TCP_KEEPIDLE, 120)
    print("set TCP_KEEPINTVL (Windows)")
    sock.setsockopt(socket.IPPROTO_TCP, TCP_KEEPINTVL, 30)
    pass
if os_version.dwMajorVersion == 10 and os_version.dwBuildNumber >= 16299:  # Windows 10 1709
    print("set TCP_KEEPCNT (Windows)")
    TCP_KEEPCNT = 15
    sock.setsockopt(socket.IPPROTO_TCP, TCP_KEEPCNT, 8)
    pass

sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.connect((hostname, port))

def make2():
    sock.send(request)
    result = sock.recv(10000)
    print(result)

make2()
do_sleep(310)
make2()
