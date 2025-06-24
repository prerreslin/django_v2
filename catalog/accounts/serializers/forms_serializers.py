from django.contrib.auth.models import User
from rest_framework import serializers


class CaptchaFieldSerializer(serializers.Serializer):
    captcha_0 = serializers.CharField(required=True)
    captcha_1 = serializers.CharField(required=True)

    def validate(self, attrs):
        from captcha.models import CaptchaStore

        try:
            captcha = CaptchaStore.objects.get(hashkey=attrs.get("captcha_0"))

        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError("Incorrect captcha")

        if captcha.response != attrs.get("captcha_1", "").lower():
            raise serializers.ValidationError("Incorrect captcha")

        captcha.delete()
        return attrs


class RegisterFormSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    captcha = CaptchaFieldSerializer(required=True)
