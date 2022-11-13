from django.db.models import Count, Q
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions, generics
from api.serializers import UserSerializer, ContributorSerializer, ProjectDetailSerializer, ProjectListSerializer, \
    CommentSerializer, IssueSerializer, ContributorDetailsSerializer, IssueAddForProjectSerializer, CommentAddSerializer
from api.models import Projects, Comments, Issues, Contributors
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet


class ProjectReadOnly(ReadOnlyModelViewSet):
    serializer_class = ProjectListSerializer
    detail_class = ProjectDetailSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        queryset = Projects.objects.filter(author_user_id=user)
        return queryset



