from rest_framework.response import Response
from rest_framework import status


def success_response(message="Operation successful", data=None, status_code=status.HTTP_200_OK):
    return Response({
        "status": "success",
        "message": message,
        "data": data or {},
    }, status=status_code)


def error_response(message="Something went wrong", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "status": "error",
        "message": message,
        "errors": errors or {},
    }, status=status_code)


def internal_server_error_response(message="Internal Server Error", exception=None):
    return Response({
        "status": "fail",
        "message": message,
        "errors": {"detail": str(exception) if exception else "Unexpected error"},
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
