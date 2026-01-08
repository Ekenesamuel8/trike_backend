# apps/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("phone", "email", "pin")

    def create(self, validated_data):
        validated_data["pin"] = make_password(validated_data["pin"])
        return User.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    pin = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        pin = data.get("pin")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not check_password(pin, user.pin):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("Account disabled")

        data["user"] = user
        return data