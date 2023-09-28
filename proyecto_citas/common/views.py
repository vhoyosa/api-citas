import logging

from django.http import HttpResponse

from rest_framework import views
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from common.exceptions import BadRequestFormatException


logger = logging.getLogger(__name__)


class APIView(views.APIView):
    pass


class ServiceView(APIView):
    """
    Custom `APIView` that helps to validate input data and return
    a response with validation errors.

    In order to use the view, you must define `process_request`
    method. It could return `rest_framework.response.Response`
    object or a pair of an object for `response_serializer` and
    a status code (for example, `rest_framework.status.HTTP_201_CREATED`).
    When request or response serializers are not needed, make use of
    common.serializers.NoDataSerializer

    Attributes:
        http_method (str): Allowed HTTP method.
        request_serializer (rest_framework.serializers.Serializer):
            Required attribute that defines a serializer that will
            be used to validate the data received by the view.
        response_serializer (rest_framework.serializers.Serializer):
            Serializer for response object (if exists).
    """

    request_serializer = None
    response_serializer = None
    http_method = None

    # pylint: disable=unused-argument,no-self-use

    def _allowed_methods(self):
        return [
            self.http_method
        ]

    def get_extra_context(self, **kwargs):
        return kwargs

    def request_regular_handling(self, request, data, *args, **kwargs):
        # pylint: disable=not-callable
        context = self.get_extra_context(view=self, request=request)

        rqs = self.request_serializer(data=data, context=context)
        rqs.is_valid(raise_exception=True)

        request_result = self.process_request(rqs, request)
        if isinstance(request_result, (Response, HttpResponse)):
            return request_result

        response_data, status_code = request_result
        rps = self.response_serializer(response_data)

        return Response(
            rps.data,
            status=status_code,
        )

    def process_request(self, request_serializer_obj, request):
        raise Exception('process_request method not implemented')

    def run_valid_request(self, valid_method, request, *args, **kwargs):
        if self.http_method != valid_method:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return self.request_regular_handling(
            request, request.GET, *args, **kwargs
        )

    def get(self, request, *args, **kwargs):
        return self.run_valid_request('GET', request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.run_valid_request('DELETE', request, *args, **kwargs)

    def validate_request_body(self, request):
        try:
            request.data
        except ParseError as exc:
            logger.warning(
                'Received invalid data in request body',
                extra=dict(
                    request_body=request.body[:1000],
                    request_meta=request.META,
                ),
            )
            raise BadRequestFormatException(request, exc)

    def post(self, request, *args, **kwargs):
        if self.http_method != 'POST':
            return self.http_method_not_allowed(request, *args, **kwargs)

        self.validate_request_body(request)

        return self.request_regular_handling(
            request, request.data, *args, **kwargs
        )

    def patch(self, request, *args, **kwargs):
        if self.http_method != 'PATCH':
            return self.http_method_not_allowed(request, *args, **kwargs)

        self.validate_request_body(request)

        return self.request_regular_handling(
            request, request.data, *args, **kwargs
        )

    def put(self, request, *args, **kwargs):
        if self.http_method != 'PUT':
            return self.http_method_not_allowed(request, *args, **kwargs)

        self.validate_request_body(request)

        return self.request_regular_handling(
            request, request.data, *args, **kwargs
        )
