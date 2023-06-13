from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

# Create your views here.


class TestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return Response({"message": "Test"}, status=status.HTTP_200_OK)
