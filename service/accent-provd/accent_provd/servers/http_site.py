# Copyright 2023 Accent Communications

"""This module add support to returning Deferred in Resource getChild/getChildWithDefault.
Only thing you need to do is to use this Site class instead of twisted.web.server.Site.

"""
from __future__ import annotations

import copy
import logging

from requests.exceptions import HTTPError

from accent_provd.app import DeviceNotInProvdTenantError, TenantInvalidForDeviceError
from accent_provd.rest.server import auth
from accent_provd.rest.server.helpers.tenants import Tenant, tenant_helpers
from accent_provd.util import decode_bytes
from twisted.internet import defer
from twisted.web import http, resource, server
from twisted.web.error import UnsupportedMethod
from twisted.web.resource import _computeAllowedMethods

logger = logging.getLogger(__name__)

auth_verifier = auth.get_auth_verifier()


class Request(server.Request):
    # originally taken from twisted.web.server.Request
    prepath: list[bytes]
    postpath: list[bytes]

    def process(self):
        """Process a request."""

        # get site from channel
        self.site = self.channel.site

        corsify_request(self)
        # set various default headers
        self.setHeader(b'server', server.version)
        self.setHeader(b'date', http.datetimeToString())
        self.setHeader(b'content-type', b"text/html")

        # Resource Identification
        self.prepath = []
        self.postpath = list(map(server.unquote, self.path[1:].split(b'/')))

        # We do not really care about the content if the request is a CORS preflight
        if self.method == b'OPTIONS':
            self.finish()
        else:
            d = self.site.getResourceFor(self)
            d.addCallback(self.render)
            d.addErrback(self.processingFailed)


class AuthResource(resource.Resource):
    def render(self, request: Request):
        render_method = self._extract_render_method(request)
        decorated_render_method = auth_verifier.verify_token(
            self, request, render_method
        )
        try:
            self.tenant_uuid = self._build_tenant_list_from_request(
                request, recurse=False
            )[0]
            return decorated_render_method(request)
        except (
            auth.http_exceptions.Unauthorized,
            auth.http_exceptions.InvalidTokenAPIException,
            auth.http_exceptions.MissingPermissionsTokenAPIException,
            tenant_helpers.InvalidTenant,
            tenant_helpers.InvalidUser,
            tenant_helpers.UnauthorizedTenant,
        ):
            request.setResponseCode(http.UNAUTHORIZED)
            return b'Unauthorized'

    def _extract_render_method(self, request: Request):
        # from twisted.web.resource.Resource
        render_method = getattr(self, f'render_{decode_bytes(request.method)}', None)
        if not render_method:
            try:
                allowed_methods = self.allowedMethods
            except AttributeError:
                allowed_methods = _computeAllowedMethods(self)
            raise UnsupportedMethod(allowed_methods)
        return render_method

    def render_OPTIONS(self, request: Request):
        logging.error(f'REQUEST: {request.getAllHeaders()}')
        return b''

    def _extract_tenant_uuid(self, request: Request):
        auth_client = auth.get_auth_client()

        return Tenant.autodetect(request, auth_client).uuid

    def _build_tenant_list(self, tenant_uuid=None, recurse=False):
        auth_client = auth.get_auth_client()

        if not recurse:
            return [tenant_uuid]
        try:
            tenants = auth_client.tenants.list(tenant_uuid=tenant_uuid)['items']
        except HTTPError as e:
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)
            if status_code == 401:
                logger.debug('Tenant listing got a 401, returning %s', [tenant_uuid])
                return [tenant_uuid]
            raise

        return [t['uuid'] for t in tenants]

    def _build_tenant_list_from_request(self, request, recurse=False):
        tenant_uuid = self._extract_tenant_uuid(request)
        return self._build_tenant_list(tenant_uuid=tenant_uuid, recurse=recurse)

    @defer.inlineCallbacks
    def _is_tenant_valid_for_device(self, app, device_id, tenant_uuid):
        device = yield app._dev_get_or_raise(device_id)

        if device['tenant_uuid'] == tenant_uuid:
            defer.returnValue(tenant_uuid)

        tenant_uuids = self._build_tenant_list(tenant_uuid=tenant_uuid, recurse=True)

        if device['tenant_uuid'] in tenant_uuids:
            defer.returnValue(tenant_uuid)

        raise TenantInvalidForDeviceError(tenant_uuid)

    @defer.inlineCallbacks
    def _verify_tenant(self, request: Request):
        tenant_uuid = self._extract_tenant_uuid(request)
        yield defer.returnValue(tenant_uuid)

    @defer.inlineCallbacks
    def _is_device_in_provd_tenant(self, app, device_id, tenant_uuid):
        device = yield app._dev_get_or_raise(device_id)

        if device['is_new']:
            defer.returnValue(tenant_uuid)

        raise DeviceNotInProvdTenantError(tenant_uuid)


class Site(server.Site):
    # originally taken from twisted.web.server.Site
    requestFactory = Request

    def getResourceFor(self, request: Request):
        """
        Get a deferred that will callback with a resource for a request.

        This iterates through the resource hierarchy, calling
        getChildWithDefault on each resource it finds for a path element,
        stopping when it hits an element where isLeaf is true.
        """
        request.site = self
        # Sitepath is used to determine cookie names between distributed
        # servers and disconnected sites.
        request.sitepath = copy.copy(request.prepath)
        return getChildForRequest(self.resource, request)


@defer.inlineCallbacks
def getChildForRequest(resource, request: Request):
    # originally taken from twisted.web.resource
    """
    Traverse resource tree to find who will handle the request.
    """
    while request.postpath and not resource.isLeaf:
        path_element = request.postpath.pop(0)
        request.prepath.append(path_element)
        retval = resource.getChildWithDefault(path_element, request)
        if isinstance(retval, defer.Deferred):
            resource = yield retval
        else:
            resource = retval
    defer.returnValue(resource)


def corsify_request(request: Request):
    # CORS
    request.setHeader(b'Access-Control-Allow-Origin', b'*')
    request.setHeader(
        b'Access-Control-Allow-Methods', b'GET, POST, PUT, DELETE, OPTIONS'
    )
    request.setHeader(
        b'Access-Control-Allow-Headers',
        b'Origin, X-Requested-With, Accept, Content-Type, X-Auth-Token, Accent-Tenant',
    )
    request.setHeader(b'Access-Control-Allow-Credentials', b'false')
    request.setHeader(b'Access-Control-Expose-Headers', b'Location')
