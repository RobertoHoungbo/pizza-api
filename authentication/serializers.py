from .models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class UserCreationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username already exists!')
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email already exists!')
        return email

    def validate_phone_number(self, phonenumber):
        if User.objects.filter(phone_number=phonenumber).exists():
            raise serializers.ValidationError('This phone number already exists!')
        return phonenumber

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )

        return user


class UserListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=80)

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
