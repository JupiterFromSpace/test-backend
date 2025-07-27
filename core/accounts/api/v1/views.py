from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, ResetPasswordSerializer, ProfileUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from core.utils.responses import success_response, error_response


def get_tokens_for_user(user):
    '''
    This function generates a JWT access and refresh token for a given user.
    '''
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    '''
    This class is an APIView for registering new users.
    It checks the information through RegisterSerializer and returns success message after creating the user.
    No token is returned on registration.
    '''
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="ثبت‌نام با موفقیت انجام شد.",
                status_code=status.HTTP_201_CREATED
            )
        return error_response("خطا در ثبت‌نام", serializer.errors)


class LoginView(APIView):
    '''
    This API class is available for user login.
    It takes email and password information, authenticates, and returns a JWT token if successful.
    '''
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return success_response(
                message="ورود با موفقیت انجام شد.",
                data={"tokens": tokens}
            )
        return error_response("خطا در ورود", serializer.errors)




class ResetPasswordView(APIView):
    '''
    This endpoint allows you to reset your password by entering your email and new password.
    '''

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="رمز عبور با موفقیت تغییر کرد.",
                status_code=status.HTTP_200_OK
            )
        return error_response(
            message="خطا در تغییر رمز عبور",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )



class ProfileUpdateView(APIView):
    '''
    This view allows the user to edit their profile information.
    Only logged in users are allowed to use this endpoint.
    '''
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        profile = request.user.profile

        missing_fields = []
        for field in ['first_name', 'last_name']:
            if field not in request.data or not request.data.get(field):
                missing_fields.append(field)

        if missing_fields:
            return error_response(
                message="برخی فیلدهای ضروری ارسال نشده‌اند.",
                errors={field: "این فیلد ضروری است." for field in missing_fields}
            )

        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="پروفایل با موفقیت به‌روزرسانی شد.",
                data=serializer.data
            )
        return error_response("خطا در به‌روزرسانی پروفایل", serializer.errors)
    