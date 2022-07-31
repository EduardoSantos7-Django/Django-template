from collections import OrderedDict
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from . import models


class User(serializers.ModelSerializer):
    "Serializer account profile model basic fields."

    name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = models.User
        fields = [
            'name',
            'email',
        ]

    def get_name(self, instance) -> str:
        return str(instance)


class UserUp(serializers.ModelSerializer):
    """Serialize user sing up credentials."""

    password2 = serializers.CharField(required=True)
    agreement = serializers.BooleanField(default=False)

    class Meta:
        """Config metadata."""

        model = models.User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
            'agreement',
        ]

    def validate_password(self, attrs):
        validate_password(attrs)
        return attrs

    def validate_password2(self, attrs):
        if self.initial_data['password'] != self.initial_data['password2']:
            raise serializers.ValidationError("Password doesn't match.")
        return attrs

    def validate_agreement(self, attrs: bool):
        if attrs is not True:
            raise serializers.ValidationError("This field is required.")
        return attrs

    def create(self, validated_data: OrderedDict):
        validated_data.pop('password2')
        validated_data.pop('agreement')

        return models.User.objects.create_user(**validated_data)


class UserIn(serializers.ModelSerializer):
    """Serialize user sing in credentials."""

    email = serializers.EmailField(required=True)
    remember_me = serializers.BooleanField(default=False)

    class Meta:
        """Config metadata."""

        model = models.User
        fields = ['email', 'password', 'remember_me']


class Validated(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'email_verified']


class RequestSendResetEmail(serializers.ModelSerializer):
    """Serialize email."""

    class Meta:
        model = models.User
        fields = [
            'email',
        ]


class ChangePassord(serializers.ModelSerializer):
    """Serialize user password."""

    password2 = serializers.CharField(required=True)

    class Meta:
        model = models.User
        fields = [
            'password',
            'password2',
        ]

    def validate_password(self, attrs):
        validate_password(attrs)
        return attrs

    def validate_password2(self, attrs):
        if self.initial_data['password'] != self.initial_data['password2']:
            raise serializers.ValidationError("Password doesn't match.")
        return attrs

    def update(self, instance: models.User, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
