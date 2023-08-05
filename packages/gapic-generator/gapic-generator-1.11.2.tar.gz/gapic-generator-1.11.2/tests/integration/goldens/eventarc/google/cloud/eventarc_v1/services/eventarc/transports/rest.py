# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.api_core import operations_v1
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.cloud.location import locations_pb2 # type: ignore
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.eventarc_v1.types import eventarc
from google.cloud.eventarc_v1.types import trigger
from google.longrunning import operations_pb2  # type: ignore

from .base import EventarcTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class EventarcRestInterceptor:
    """Interceptor for Eventarc.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the EventarcRestTransport.

    .. code-block:: python
        class MyCustomEventarcInterceptor(EventarcRestInterceptor):
            def pre_create_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_triggers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_triggers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = EventarcRestTransport(interceptor=MyCustomEventarcInterceptor())
        client = EventarcClient(transport=transport)


    """
    def pre_create_trigger(self, request: eventarc.CreateTriggerRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[eventarc.CreateTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_create_trigger(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_trigger

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response
    def pre_delete_trigger(self, request: eventarc.DeleteTriggerRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[eventarc.DeleteTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_delete_trigger(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_trigger

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response
    def pre_get_trigger(self, request: eventarc.GetTriggerRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[eventarc.GetTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_trigger(self, response: trigger.Trigger) -> trigger.Trigger:
        """Post-rpc interceptor for get_trigger

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response
    def pre_list_triggers(self, request: eventarc.ListTriggersRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[eventarc.ListTriggersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_triggers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_list_triggers(self, response: eventarc.ListTriggersResponse) -> eventarc.ListTriggersResponse:
        """Post-rpc interceptor for list_triggers

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response
    def pre_update_trigger(self, request: eventarc.UpdateTriggerRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[eventarc.UpdateTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_update_trigger(self, response: operations_pb2.Operation) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_trigger

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class EventarcRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: EventarcRestInterceptor


class EventarcRestTransport(EventarcTransport):
    """REST backend transport for Eventarc.

    Eventarc allows users to subscribe to various events that are
    provided by Google Cloud services and forward them to supported
    destinations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
    """

    def __init__(self, *,
            host: str = 'eventarc.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            client_cert_source_for_mtls: Optional[Callable[[
                ], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            url_scheme: str = 'https',
            interceptor: Optional[EventarcRestInterceptor] = None,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

       NOTE: This REST transport functionality is currently in a beta
       state (preview). We welcome your feedback via a GitHub issue in
       this library's repository. Thank you!

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(f"Unexpected hostname structure: {host}")  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST)
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or EventarcRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
            }

            rest_transport = operations_v1.OperationsRestTransport(
                    host=self._host,
                    # use the credentials which are saved
                    credentials=self._credentials,
                    scopes=self._scopes,
                    http_options=http_options,
                    path_prefix="v1")

            self._operations_client = operations_v1.AbstractOperationsClient(transport=rest_transport)

        # Return the client from cache.
        return self._operations_client

    class _CreateTrigger(EventarcRestStub):
        def __hash__(self):
            return hash("CreateTrigger")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "triggerId" : "",            "validateOnly" : False,        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: eventarc.CreateTriggerRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the create trigger method over HTTP.

            Args:
                request (~.eventarc.CreateTriggerRequest):
                    The request object. The request message for the
                CreateTrigger method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1/{parent=projects/*/locations/*}/triggers',
                'body': 'trigger',
            },
            ]
            request, metadata = self._interceptor.pre_create_trigger(request, metadata)
            pb_request = eventarc.CreateTriggerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_trigger(resp)
            return resp

    class _DeleteTrigger(EventarcRestStub):
        def __hash__(self):
            return hash("DeleteTrigger")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "validateOnly" : False,        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: eventarc.DeleteTriggerRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the delete trigger method over HTTP.

            Args:
                request (~.eventarc.DeleteTriggerRequest):
                    The request object. The request message for the
                DeleteTrigger method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'delete',
                'uri': '/v1/{name=projects/*/locations/*/triggers/*}',
            },
            ]
            request, metadata = self._interceptor.pre_delete_trigger(request, metadata)
            pb_request = eventarc.DeleteTriggerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_trigger(resp)
            return resp

    class _GetTrigger(EventarcRestStub):
        def __hash__(self):
            return hash("GetTrigger")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: eventarc.GetTriggerRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> trigger.Trigger:
            r"""Call the get trigger method over HTTP.

            Args:
                request (~.eventarc.GetTriggerRequest):
                    The request object. The request message for the
                GetTrigger method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.trigger.Trigger:
                    A representation of the trigger
                resource.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1/{name=projects/*/locations/*/triggers/*}',
            },
            ]
            request, metadata = self._interceptor.pre_get_trigger(request, metadata)
            pb_request = eventarc.GetTriggerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = trigger.Trigger()
            pb_resp = trigger.Trigger.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_trigger(resp)
            return resp

    class _ListTriggers(EventarcRestStub):
        def __hash__(self):
            return hash("ListTriggers")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: eventarc.ListTriggersRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> eventarc.ListTriggersResponse:
            r"""Call the list triggers method over HTTP.

            Args:
                request (~.eventarc.ListTriggersRequest):
                    The request object. The request message for the
                ListTriggers method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.eventarc.ListTriggersResponse:
                    The response message for the
                ListTriggers method.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1/{parent=projects/*/locations/*}/triggers',
            },
            ]
            request, metadata = self._interceptor.pre_list_triggers(request, metadata)
            pb_request = eventarc.ListTriggersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = eventarc.ListTriggersResponse()
            pb_resp = eventarc.ListTriggersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_triggers(resp)
            return resp

    class _UpdateTrigger(EventarcRestStub):
        def __hash__(self):
            return hash("UpdateTrigger")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
            "validateOnly" : False,        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: eventarc.UpdateTriggerRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> operations_pb2.Operation:
            r"""Call the update trigger method over HTTP.

            Args:
                request (~.eventarc.UpdateTriggerRequest):
                    The request object. The request message for the
                UpdateTrigger method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'patch',
                'uri': '/v1/{trigger.name=projects/*/locations/*/triggers/*}',
                'body': 'trigger',
            },
            ]
            request, metadata = self._interceptor.pre_update_trigger(request, metadata)
            pb_request = eventarc.UpdateTriggerRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                including_default_value_fields=False,
                use_integers_for_enums=False
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_trigger(resp)
            return resp

    @property
    def create_trigger(self) -> Callable[
            [eventarc.CreateTriggerRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTrigger(self._session, self._host, self._interceptor) # type: ignore

    @property
    def delete_trigger(self) -> Callable[
            [eventarc.DeleteTriggerRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTrigger(self._session, self._host, self._interceptor) # type: ignore

    @property
    def get_trigger(self) -> Callable[
            [eventarc.GetTriggerRequest],
            trigger.Trigger]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTrigger(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_triggers(self) -> Callable[
            [eventarc.ListTriggersRequest],
            eventarc.ListTriggersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTriggers(self._session, self._host, self._interceptor) # type: ignore

    @property
    def update_trigger(self) -> Callable[
            [eventarc.UpdateTriggerRequest],
            operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTrigger(self._session, self._host, self._interceptor) # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__=(
    'EventarcRestTransport',
)
