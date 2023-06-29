from django.contrib.auth import authenticate
from user.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed

# from constant.choice import DEFAULT_PASSWORD


def register_social_google_user(email, name):
    try:
        # check user has email is exist
        user = User.objects.get(email=email)
        if user.auth_google == False:
            user.is_active = True
            user.auth_google = True
            user.save()

        return user, {
            "access_token": user.access_token,
            "refresh_token": user.refresh_token,
        }

    except:
        new_user = User.objects.create_user(
            username=name,
            email=email,
            phone=email.split("@")[0],
            # role=role
        )
        new_user.set_password("DEFAULT_PASSWORD")
        new_user.is_active = True
        new_user.auth_google = True
        new_user.save()
        return new_user, {
            "access_token": new_user.access_token,
            "refresh_token": new_user.refresh_token,
        }


def register_social_facebook_user(email, name):
    try:
        # check user has email is exist
        user = User.objects.get(email=email)
        if user.auth_facebook == False:
            user.is_verified = True
            user.is_active = True
            user.auth_facebook = True
            user.save()

        return user, {
            "access_token": user.access_token,
            "refresh_token": user.refresh_token,
        }

    except:
        # check user has email is not exist
        new_user = User.objects.create_user(
            username=name, email=email, password="DEFAULT_PASSWORD"
        )
        new_user.is_verified = True
        new_user.is_active = True
        new_user.auth_facebook = True
        new_user.save()
        return new_user, {
            "access_token": new_user.access_token,
            "refresh_token": new_user.refresh_token,
        }
