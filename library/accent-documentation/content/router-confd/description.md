# [router-confd](https://github/ryanwclark1/accent-router-confd)

This is the configuration, management, and routing API server of the Accent Platform C4 (Class 4).

* Carrier and Carrier Trunks
* CDR
* DIDs
* Domains
* IPBX
* Normalization profiles and rules
* Routing groups and rules
* Tenants

It exposes the end-points used by the Accent Router as well.

## Schema

![C4 schema](diagram-c4.svg)

## Part of the Accent Platform C4

A Class 4 Softswitch routes large volumes of usually long-distance VoIP calls. For businesses that want to interconnect their VoIP servers, a Class 4 Softswitch is used to relay VoIP traffic and services over multiple IP networks. C4 soft switches provide intelligent call routing, which reduces congestion, latency, and costs while improving the quality of VoIP calls. They have several security features to protect the C5 switches.

The main characteristics of a C4 Softswitch are:

* route large volume of calls
* protocol support and conversion
* transcoding
* billing interface
* security management
* call authentication
* call authorization

Accent Platform aims to offer to service providers, enterprises, and digital natives a coherent and complete reference platform for the design, deployment, and management of a telecom infrastructure that can support massive volumes of simultaneous calls by interconnecting millions of users.

The solution must be able to handle mission-critical needs by providing robust and efficient mechanisms for availability and scalability.

## API documentation

The REST API for accent-router-confd is available [here](../api/router-confd.html)

## Related

* [accent-c4-sbc](c4-sbc.html)
* [accent-c4-router](c4-router.html)
* [accent-rtpe](rtpe-config.html)
