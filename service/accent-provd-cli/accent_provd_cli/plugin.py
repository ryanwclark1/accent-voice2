# Copyright 2023 Accent Communications

# importing <module> as _<module> so that import are not autocompleted in the CLI
from pprint import pprint as _pprint

# list of (test config info, test config factory) tuples
_TEST_CONFIGS = []
# test certificate
_TEST_CERT = """\
-----BEGIN CERTIFICATE-----
MIICgjCCAiygAwIBAgIJAJwF1KTBOPBuMA0GCSqGSIb3DQEBBQUAMGExCzAJBgNV
BAYTAkNBMQ8wDQYDVQQIEwZRdWViZWMxDzANBgNVBAcTBlF1ZWJlYzEhMB8GA1UE
ChMYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMQ0wCwYDVQQDEwRUZXN0MB4XDTEx
MDgxMTEyMzEzNFoXDTE0MDgxMDEyMzEzNFowYTELMAkGA1UEBhMCQ0ExDzANBgNV
BAgTBlF1ZWJlYzEPMA0GA1UEBxMGUXVlYmVjMSEwHwYDVQQKExhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQxDTALBgNVBAMTBFRlc3QwXDANBgkqhkiG9w0BAQEFAANL
ADBIAkEAxlYKKK/mUcvR8qR/EvaVu108pLw4wuPCrqzfhLAoprGerXfZP2YhhyYs
GlbrQtbY35OfXgaQlka0GHaJ451JYwIDAQABo4HGMIHDMB0GA1UdDgQWBBTkhtbv
aTHnKF74IAIOiug0940DmzCBkwYDVR0jBIGLMIGIgBTkhtbvaTHnKF74IAIOiug0
940Dm6FlpGMwYTELMAkGA1UEBhMCQ0ExDzANBgNVBAgTBlF1ZWJlYzEPMA0GA1UE
BxMGUXVlYmVjMSEwHwYDVQQKExhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQxDTAL
BgNVBAMTBFRlc3SCCQCcBdSkwTjwbjAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEB
BQUAA0EAbtlcPsrcsuXvxDq60D5AloZhFJoPsvpEcpqz4F9h4JkHWpJLqmXucoAr
hI3UQIC7ov7+c//RAE5gVACKtLNlIQ==
-----END CERTIFICATE-----
"""
# test key (goes with the test certificate by the way)
_TEST_KEY = """\
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAMZWCiiv5lHL0fKkfxL2lbtdPKS8OMLjwq6s34SwKKaxnq132T9m
IYcmLBpW60LW2N+Tn14GkJZGtBh2ieOdSWMCAwEAAQI/aiOhTCTWHO/2auOdHYjY
mGxNB9uyhJlelhvtghTDrHBvAXIIja/yBt2L87BNFErqK7ICRK5geHAwD5AHt5Xx
AiEA+fPWMBmqJU1AMuEpagpy7U6GrOdWqlmvAbifD+FW8xkCIQDLIn/z5NrRyEQz
feBrOwSh0y4/JQwf4WBG7lKimHtL2wIhAKi6QUwXBxRHIZ82/43ln88xwxfU0lwM
TmcLCdTeeKOBAiEApMDMimHZYEBPoHu9ovrxHNcNMUW4+bpvvdfZyepmRfUCIQCU
vTY4cAbxNt/187RFuZU/B3NqiQS/OyktZyIoaZ4QTQ==
-----END RSA PRIVATE KEY-----
"""


def _init_module(configs, devices, plugins):
    # MUST be called from another module before the function in this module
    # are made available in the CLI
    global _configs
    global _devices
    global _plugins
    _configs = configs
    _devices = devices
    _plugins = plugins


def remove_all():
    """Remove all the plugins, devices and configs."""
    _plugins.uninstall_all()
    _devices.remove_all()
    _configs.remove_all()


def remove_test_objects():
    """Remove all devices and configs."""
    remove_test_devices()
    remove_test_configs()


def remove_test_configs():
    """Remove all test configs, i.e. all configs which have a key 'X_test'
    set to True.

    """
    for config in _configs.find({'X_test': True}, fields=['id']):
        config_id = config['id']
        print(f'Removing config {config_id}')
        _configs.remove(config_id)


def remove_test_devices():
    """Remove all test devices, i.e. all devices which have a key 'X_test'
    set to True.

    """
    for device in _devices.find({'X_test': True}, fields=['id']):
        device_id = device['id']
        print(f'Removing device {device_id}')
        _devices.remove(device_id)


def exec_config_tests(device_id):
    """Execute the config tests using the device with the given device ID."""
    device = _devices[device_id]
    for info, cfg_factory in _TEST_CONFIGS:
        desc = info['description']
        config = cfg_factory()
        while True:
            s = input(f'Test {desc} config ? [Y/n/p] ')
            if not s or s[0].lower() == 'y':
                config['X_test'] = True
                cfg_id = _configs.add(config)
                device.set({'config': cfg_id})
                configured = device.get()['configured']
                print(f'   configured: {configured}')
                break
            elif s[0].lower() == 'n':
                break
            elif s[0].lower() == 'p':
                _pprint(config)
            else:
                print(f'Invalid input {input}')
            print()


def add_test_devices(plugin_id):
    """Add the tests device using plugin with the given ID."""
    _devices.add({'id': 'empty', 'X_test': True, 'plugin': plugin_id})
    _devices.add(
        {'id': 'min', 'X_test': True, 'mac': '00:11:22:33:44:00', 'plugin': plugin_id}
    )


def _test_config(fun):
    description = fun.__name__.lstrip('_').replace('_', ' ')
    _TEST_CONFIGS.append(({'description': description}, fun))
    return fun


@_test_config
def _minimalist():
    return {'parent_ids': [], 'raw_config': {}}


@_test_config
def _minimalist_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            }
        },
    }


@_test_config
def _minimalist_global_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_proxy_ip': '1.1.1.1',
            'sip_lines': {
                '1': {
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _minimalist_mixed_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_proxy_ip': '1.1.1.0',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _standard_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'registrar_ip': '1.1.1.1',
                    'username': 'username1',
                    'auth_username': 'authusername1',
                    'password': 'password1',
                    'display_name': 'User 1',
                    'number': 'number1',
                }
            }
        },
    }


@_test_config
def _different_proxy_and_registrar_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'registrar_ip': '1.1.1.2',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            }
        },
    }


@_test_config
def _backup_proxy_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'backup_proxy_ip': '1.1.1.2',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            }
        },
    }


@_test_config
def _backup_proxy_and_registrar_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'backup_proxy_ip': '1.1.1.2',
                    'backup_registrar_ip': '1.1.1.3',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            }
        },
    }


@_test_config
def _non_standard_ports_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'proxy_port': 15060,
                    'registrar_port': 15061,
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            }
        },
    }


@_test_config
def _multiple_lines_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                },
                '2': {
                    'proxy_ip': '1.1.2.1',
                    'username': 'username2',
                    'password': 'password2',
                    'display_name': 'User 2',
                },
                '3': {
                    'proxy_ip': '1.1.3.1',
                    'username': 'username3',
                    'password': 'password3',
                    'display_name': 'User 3',
                },
            }
        },
    }


@_test_config
def _tcp_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_transport': 'tcp',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _tls_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_transport': 'tls',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _tls_with_certificate_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_transport': 'tls',
            'sip_servers_root_and_intermediate_certificates': _TEST_CERT,
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _global_srtp_preferred_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_srtp_mode': 'preferred',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _global_srtp_required_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_srtp_mode': 'required',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _per_line_srtp_preferred_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                    'srtp_mode': 'preferred',
                }
            }
        },
    }


@_test_config
def _per_line_srtp_required_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                    'srtp_mode': 'required',
                }
            }
        },
    }


@_test_config
def _subscribe_mwi_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_subscribe_mwi': True,
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                    'voicemail': '*981',
                }
            },
        },
    }


@_test_config
def _global_dtmf_inband_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_dtmf_mode': 'RTP-in-band',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _global_dtmf_rfc2833_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_dtmf_mode': 'RTP-out-of-band',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _global_dtmf_sip_info_sip():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_dtmf_mode': 'SIP-INFO',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _dns_enabled():
    return {
        'parent_ids': [],
        'raw_config': {
            'dns_enabled': True,
            'dns_ip': '2.2.2.2',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _ntp_enabled():
    return {
        'parent_ids': [],
        'raw_config': {
            'ntp_enabled': True,
            'ntp_ip': '2.2.2.2',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _vlan_enabled():
    return {
        'parent_ids': [],
        'raw_config': {
            'vlan_enabled': True,
            'vlan_id': '100',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _vlan_with_priority():
    return {
        'parent_ids': [],
        'raw_config': {
            'vlan_enabled': True,
            'vlan_id': '100',
            'vlan_priority': '5',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _vlan_with_pc_port():
    return {
        'parent_ids': [],
        'raw_config': {
            'vlan_enabled': True,
            'vlan_id': '100',
            'vlan_pc_port_id': '200',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _syslog_enabled():
    return {
        'parent_ids': [],
        'raw_config': {
            'syslog_enabled': True,
            'syslog_ip': '2.2.2.2',
            'syslog_port': 515,
            'syslog_level': 'info',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _admin_username_and_password():
    return {
        'parent_ids': [],
        'raw_config': {
            'admin_username': 'ausername',
            'admin_password': 'apassword',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _user_username_and_password():
    return {
        'parent_ids': [],
        'raw_config': {
            'user_username': 'uusername',
            'user_password': 'upassword',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _timezone_paris():
    return {
        'parent_ids': [],
        'raw_config': {
            'timezone': 'Europe/Paris',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _timezone_montreal():
    return {
        'parent_ids': [],
        'raw_config': {
            'timezone': 'America/Montreal',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _locale_fr_FR():
    return {
        'parent_ids': [],
        'raw_config': {
            'locale': 'fr_FR',
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _config_encryption_enabled():
    return {
        'parent_ids': [],
        'raw_config': {
            'config_encryption_enabled': True,
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
        },
    }


@_test_config
def _funckey_speeddial():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
            'funckeys': {
                '1': {
                    'type': 'speeddial',
                    'value': 'value1',
                    'label': 'label1',
                }
            },
        },
    }


@_test_config
def _funckey_blf():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
            'funckeys': {
                '1': {
                    'type': 'blf',
                    'value': 'value1',
                    'label': 'label1',
                }
            },
        },
    }


@_test_config
def _funckey_park():
    return {
        'parent_ids': [],
        'raw_config': {
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.1.1',
                    'username': 'username1',
                    'password': 'password1',
                    'display_name': 'User 1',
                }
            },
            'funckeys': {
                '1': {
                    'type': 'park',
                    'value': 'value1',
                    'label': 'label1',
                }
            },
        },
    }


@_test_config
def _full():
    return {
        'parent_ids': [],
        'raw_config': {
            'dns_enabled': True,
            'dns_ip': '1.1.1.1',
            'ntp_enabled': True,
            'ntp_ip': '1.1.1.2',
            'vlan_enabled': True,
            'vlan_id': 1,
            'vlan_priority': 2,
            'vlan_pc_port_id': 3,
            'syslog_enabled': True,
            'syslog_ip': '1.1.1.3',
            'syslog_port': 515,
            'syslog_level': 'warning',
            'admin_username': 'adminu',
            'admin_password': 'adminp',
            'user_username': 'useru',
            'user_password': 'userp',
            'timezone': 'Europe/Paris',
            'locale': 'fr_FR',
            'sip_proxy_ip': '1.1.1.4',
            'sip_proxy_port': 5061,
            'sip_backup_proxy_ip': '1.1.1.5',
            'sip_backup_proxy_port': 5062,
            'sip_registrar_ip': '1.1.1.5',
            'sip_registrar_port': 5063,
            'sip_backup_registrar_ip': '1.1.1.6',
            'sip_backup_registrar_port': 5063,
            'sip_outbound_proxy_ip': '1.1.1.7',
            'sip_outbound_proxy_port': 5064,
            'sip_dtmf_mode': 'SIP-INFO',
            'sip_subscribe_mwi': True,
            'sip_lines': {
                '1': {
                    'proxy_ip': '1.1.2.1',
                    'proxy_port': 5160,
                    'backup_proxy_ip': '1.1.2.2',
                    'backup_proxy_port': 5161,
                    'registrar_ip': '1.1.2.3',
                    'registrar_port': 5162,
                    'backup_registrar_ip': '1.1.2.4',
                    'backup_registrar_port': 5163,
                    'outbound_proxy_ip': '1.1.2.5',
                    'outbound_proxy_port': 5164,
                    'username': 'username1',
                    'auth_username': 'ausername1',
                    'password': 'password1',
                    'display_name': 'User 1',
                    'number': '1',
                    'dtmf_mode': 'SIP-INFO',
                    'voicemail': '*981',
                },
                '2': {
                    'proxy_ip': '1.1.3.1',
                    'proxy_port': 5260,
                    'backup_proxy_ip': '1.1.3.2',
                    'backup_proxy_port': 5261,
                    'registrar_ip': '1.1.3.3',
                    'registrar_port': 5262,
                    'backup_registrar_ip': '1.1.3.4',
                    'backup_registrar_port': 5263,
                    'outbound_proxy_ip': '1.1.3.5',
                    'outbound_proxy_port': 5264,
                    'username': 'username2',
                    'auth_username': 'ausername2',
                    'password': 'password2',
                    'display_name': 'User 2',
                    'number': '2',
                    'dtmf_mode': 'SIP-INFO',
                    'voicemail': '*982',
                },
            },
            'exten_dnd': '*dnd',
            'exten_fwd_unconditional': '*fwdunc',
            'exten_fwd_no_answer': '*fwdnoans',
            'exten_fwd_busy': '*fwdbusy',
            'exten_fwd_disable_all': '*fwddisable',
            'exten_park': '*park',
            'exten_pickup_group': '*pckgrp',
            'exten_pickup_call': '*pckcall',
            'exten_voicemail': '*vmail',
            'funckeys': {
                '1': {
                    'type': 'speeddial',
                    'value': 'fkv1',
                    'label': 'fkl1',
                },
                '2': {
                    'type': 'blf',
                    'value': 'fkv2',
                    'label': 'fkl2',
                },
                '3': {'type': 'park', 'value': 'fkv3', 'label': 'fkl3'},
            },
            'X_accent_phonebook_ip': '1.1.1.8',
        },
    }


@_test_config
def _minimalist_sccp():
    return {
        'parent_ids': [],
        'raw_config': {'sccp_call_managers': {'1': {'ip': '1.1.1.1'}}},
    }
