#!/usr/bin/env python3
import http.cookiejar as cookiejar
import sys
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener

SWITCH_IP = "192.168.0.0"
PASSWORD = "password"

LOGIN_URL = f"http://{SWITCH_IP}/base/main_login.html"
VLAN_URL = f"http://{SWITCH_IP}/switching/dot1q/qnp_port_cfg_rw.html"

cookie_handler = HTTPCookieProcessor(cookiejar.CookieJar())
browser = build_opener(cookie_handler)


def login_post(password):
    params = {'pwd': password, 'login.x': 0, 'login.y': 0, 'err_flag': 0, 'err_msg': ''}

    return urlencode(params).encode('utf-8')


def port_vlan_post(vlan, ports):
    params = {
        'cncel': '',
        'err_flag': '0',
        'err_msg': '',
        'filter': 'Blank',
        'ftype': 'Blank',
        'inputBox_interface1': '',
        'inputBox_interface2': '',
        'java_port': '',
        'multiple_ports': '3',
        'priority': '',
        'pvid': vlan,
        'refrsh': '',
        'submt': '16',
        'unit_no': '1',
    }

    post = list(params.items())
    post.extend(('CBox_1', 'checkbox') for x in ports)
    gports = ('selectedPorts', ';'.join('g%s' % x for x in ports))
    post.append(gports)

    return urlencode(post).encode('utf-8')


def open_url(url, post):
    resp = browser.open(url, post)
    if resp.getcode() >= 400:
        raise Exception(f"Error {resp.getcode()} while opening {url}")


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print(f"Usage: {sys.argv[0]} vlan ports")
        sys.exit(0)

    vlan = int(sys.argv[1])
    ports = [int(x) for x in sys.argv[2].split(",")]

    print("Connecting to switch...")
    open_url(LOGIN_URL, login_post(PASSWORD))

    print("Adjusting VLAN ports...")
    open_url(VLAN_URL, port_vlan_post(vlan, ports))

    print("Done")
