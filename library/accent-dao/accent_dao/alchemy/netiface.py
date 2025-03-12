# file: accent_dao/models/netiface.py
# Copyright 2025 Accent Communications

from typing import Literal

from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base

NetifaceNetworktype = Literal["data", "voip"]
NetifaceFamily = Literal["inet", "inet6"]
NetifaceMethod = Literal["static", "dhcp", "manual"]
NetifaceType = Literal["iface"]  # Added


class Netiface(Base):
    """Represents a network interface configuration.

    Attributes:
        id: The unique identifier for the network interface.
        ifname: The name of the interface.
        hwtypeid: The hardware type ID.
        networktype: The network type ('data' or 'voip').
        type: The interface type ('iface').
        family: The address family ('inet' or 'inet6').
        method: The configuration method ('static', 'dhcp', 'manual').
        address: The IP address.
        netmask: The netmask.
        broadcast: The broadcast address.
        gateway: The gateway address.
        mtu: The MTU (Maximum Transmission Unit).
        vlanrawdevice: The raw device for VLAN configuration.
        vlanid: The VLAN ID.
        options: Additional options.
        disable: Indicates if the interface is disabled.
        dcreate: Indicates if the interface should be dynamically created.
        description: A description of the interface.

    """

    __tablename__: str = "netiface"

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    ifname: Mapped[str] = mapped_column(
        String(64), nullable=False, server_default="", unique=True
    )
    hwtypeid: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="65534"
    )
    networktype: Mapped[NetifaceNetworktype] = mapped_column(
        Enum("data", "voip", name="netiface_networktype"), nullable=False
    )
    type: Mapped[NetifaceType] = mapped_column(String, nullable=False)
    family: Mapped[NetifaceFamily] = mapped_column(
        Enum("inet", "inet6", name="netiface_family"), nullable=False
    )
    method: Mapped[NetifaceMethod] = mapped_column(
        Enum("static", "dhcp", "manual", name="netiface_method")
    )
    address: Mapped[str | None] = mapped_column(String(39), nullable=True)
    netmask: Mapped[str | None] = mapped_column(String(39), nullable=True)
    broadcast: Mapped[str | None] = mapped_column(String(15), nullable=True)
    gateway: Mapped[str | None] = mapped_column(String(39), nullable=True)
    mtu: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vlanrawdevice: Mapped[str | None] = mapped_column(String(64), nullable=True)
    vlanid: Mapped[int | None] = mapped_column(Integer, nullable=True)
    options: Mapped[str] = mapped_column(Text, nullable=False)
    disable: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    dcreate: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
