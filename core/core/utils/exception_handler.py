from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from core.utils.responses import error_response, internal_server_error_response


def custom_exception_handler(exc, context):
    
    response = drf_exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code
        message = str(exc)

        if isinstance(exc, ValidationError):
            return error_response("Validation failed", errors=exc.detail, status_code=status_code)

        if isinstance(exc, (NotFound, ObjectDoesNotExist)):
            return error_response("Not found", status_code=404)

        if isinstance(exc, PermissionDenied):
            return error_response("Permission denied", status_code=403)

        return error_response(message, status_code=status_code)

    # ارورهای غیرقابل هندل (مثلاً کد 500 یا Exceptionهای Python)
    return internal_server_error_response(exception=exc)
