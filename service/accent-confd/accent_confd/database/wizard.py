# Copyright 2023 Accent Communications

from accent_dao.alchemy.infos import Infos
from accent_dao.alchemy.netiface import Netiface
from accent_dao.alchemy.resolvconf import Resolvconf
from accent_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings
from accent_dao.alchemy.staticiax import StaticIAX
from accent_dao.helpers.db_manager import Session


def set_language(language):
    row = Session.query(StaticIAX).filter(StaticIAX.var_name == 'language').first()
    row.var_val = language
    Session.add(row)

    row = (
        Session.query(SCCPGeneralSettings)
        .filter(SCCPGeneralSettings.option_name == 'language')
        .first()
    )
    row.option_value = language
    Session.add(row)


def set_timezone(timezone):
    row = Session.query(Infos).first()
    row.timezone = timezone
    Session.add(row)


def set_resolvconf(hostname, domain, nameservers):
    row = Session.query(Resolvconf).first()
    row.hostname = hostname
    row.domain = domain
    row.search = domain
    row.description = 'Wizard Configuration'
    row.nameserver1 = nameservers[0]
    if len(nameservers) > 1:
        row.nameserver2 = nameservers[1]
        if len(nameservers) > 2:
            row.nameserver3 = nameservers[2]

    Session.add(row)


def set_netiface(interface, address, netmask, gateway):
    Session.add(
        Netiface(
            ifname=interface,
            hwtypeid=1,
            networktype='voip',
            type='iface',
            family='inet',
            method='static',
            address=address,
            netmask=netmask,
            broadcast='',
            gateway=gateway,
            mtu=1500,
            options='',
            description='Wizard Configuration',
        )
    )


def set_accent_configured():
    row = Session.query(Infos).first()
    row.configured = True
    Session.add(row)


def get_accent_configured():
    return Session.query(Infos).first()


def create(wizard):
    network = wizard['network']

    set_language(wizard['language'])
    set_netiface(
        network['interface'],
        network['ip_address'],
        network['netmask'],
        network['gateway'],
    )
    set_resolvconf(network['hostname'], network['domain'], network['nameservers'])
    set_timezone(wizard['timezone'])
