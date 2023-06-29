import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer, FacebookSocialAuthSerializer
from oauth2_provider.models import (
    AccessToken,
    RefreshToken,
    get_access_token_model,
    get_application_model,
)
from oauth2_provider.views.base import TokenView
from oauth2_provider.signals import app_authorized
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from oauth2_provider.views.mixins import OAuthLibMixin
from django.views.generic import View
from django.views.decorators.debug import sensitive_post_parameters


# class GoogleSocialAuthView(GenericAPIView):
#     serializer_class = GoogleSocialAuthSerializer

#     def post(self, request):
#         """
#         POST with "auth_token"
#         Send an idtoken as from google to get user information
#         """

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = (serializer.validated_data)["auth_token"]
#         return Response(data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class GoogleSocialAuthView(OAuthLibMixin, View):
    serializer_class = GoogleSocialAuthSerializer
    """
    Implements an endpoint to provide access tokens

    The endpoint is used in the following flows:
    * Authorization code
    * Password
    * Client credentials
    """

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        auth_token = request.POST.get("auth_token")
        serializer = self.serializer_class(data={"auth_token": auth_token})
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        username = user.phone
        password = user.password
        hashed_password = make_password(password)
        new_request = request.POST.copy()
        new_request["username"] = username
        new_request["password"] = "DEFAULT_PASSWORD"
        request.POST = new_request
        print("request.POST: ", request.POST)
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        user = serializer.validated_data["user"]

        access_token = AccessToken.objects.create(
            user=user,
            token_type="Bearer",
            expires=None,  # Không có thời gian hết hạn
            scope="read write",  # Phạm vi truy cập của access token
        )

        # Tạo refresh token của Django OAuth Toolkit cho user
        # refresh_token = RefreshToken.objects.create(
        #     user=user,
        #     token=generate_token(),  # Tạo một refresh token duy nhất
        #     access_token=access_token,
        #     revoked=False,
        # )
        return Response(data, status=status.HTTP_200_OK)
