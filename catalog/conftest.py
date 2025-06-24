import os

import django
import django.contrib
import django.contrib.auth
import django.contrib.auth.models
import pytest


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catalog.settings")
django.setup()

from rest_framework.test import APIClient


@pytest.fixture
def user():
    return django.contrib.auth.models.User.objects.create_user(
        username="testusertestusertestuser", password="password_test_user"
    )


@pytest.fixture
def api_client():
    apiclient = APIClient()
    return apiclient


@pytest.fixture
def super_user():
    return django.contrib.auth.models.User.objects.create_superuser(
        username="testsuperusernametestsuperusername",password="password_test_super_user"
    )