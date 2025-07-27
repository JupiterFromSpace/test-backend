from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from accounts.models.users import User
from accounts.models.profiles import Profile


class RegisterSerializer(serializers.ModelSerializer):
    '''
    New user registration with initial profile creation (first_name, last_name, description)
    '''

    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    description = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'description']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("ایمیل قبلاً ثبت شده است.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        # جداسازی اطلاعات پروفایل
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        description = validated_data.pop('description', '')

        user = User.objects.create_user(**validated_data)

        # به‌روزرسانی پروفایل مرتبط
        profile = user.profile
        profile.first_name = first_name
        profile.last_name = last_name
        profile.description = description
        profile.save()

        return user



class LoginSerializer(serializers.Serializer):
    '''
        This class is responsible for performing the login operation.
        A simple Serializer is used because there is no need to store or modify it in the database.
        It only checks the information and authenticates it.
    '''

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("ایمیل یا رمز عبور اشتباه است.")
        if not user.is_active:
            raise serializers.ValidationError("حساب کاربری فعال نیست.")

        attrs["user"] = user
        return attrs



class ResetPasswordSerializer(serializers.Serializer):
    '''
    Receive email and new password to reset password.
    Password is validated with Django's validate_password.
    '''

    email = serializers.EmailField()
    new_password = serializers.CharField(
        write_only=True, 
        min_length=8, 
        style={'input_type': 'password'}
    )

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("کاربری با این ایمیل ثبت نشده است.")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self):
        '''
        پسورد کاربر با ایمیل داده شده را به پسورد جدید تغییر می‌دهد.
        '''
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user
    
    
    
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    '''
    This class is used to edit user profile information.
    Only fields that are allowed to be edited are specified.
    '''
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    description = serializers.CharField(write_only=True, required=False, allow_blank=True)    
    image = serializers.CharField(write_only=True, required=False, min_length=8)
    
    class Meta:
        model = Profile
        
        fields = ['first_name', 'last_name', 'description', 'image']
        
