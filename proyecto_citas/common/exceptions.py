import requests

from rest_framework import status
from rest_framework.exceptions import APIException


class AuthenticationException(Exception):
    def __init__(
            self, message='AuthenticationException',
            response=None, errors=None,
    ):
        super().__init__(self, message)
        self.errors = errors
        self.response = response


class BadRequestFormatException(Exception):
    """Exception launched when the request body could not be parsed according
    to the content type"""
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

'''This custom exception contains a list of exceptions that
refer only to exceptions when trying to connect to a host,
at this point only the connection to the host has been attempted,
an http request has not been sent, so when a listed exception is
thrown here it is safe to retry it in the future.
'''
ConnectionErrorException = (
    requests.exceptions.ConnectionError,
    requests.exceptions.ConnectTimeout,
    requests.packages.urllib3.exceptions.ConnectTimeoutError,
)

'''This custom exception contains a list of exceptions that refer
only to exceptions when sending an http request to a host and we
are waiting for the response of said host, at this point it connected
to the host and sent an http request, so that throwing an exception
listed here is NOT safe to retry in the future.
'''
TimeoutErrorException = (
    requests.exceptions.Timeout,
    requests.exceptions.ReadTimeout,
    requests.packages.urllib3.exceptions.ReadTimeoutError,
    requests.exceptions.RequestException,
)


class FailLoadHttpClientConfigException(Exception):
    """Raised when a http client cannot be created"""

    def __init__(
        self,
        user_email,
        msg,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_email = user_email
        self.msg = msg


class RequestFailureException(Exception):
    """Raised when the request did *not* succeed, and we know nothing happened
    in the remote side. From a businness-logic point of view, the operation the
    client was supposed to perform did NOT happen"""
    def __init__(self, *args, url='', response=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response
        self.url = url


class UnknownResultException(Exception):
    """Raised when we don't know if the request was completed or not. From a
    businness-logic point of view, it is not known if the operation succeded,
    or failed"""
    def __init__(self, *args, url='', response=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response
        self.url = url
