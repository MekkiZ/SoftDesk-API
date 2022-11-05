from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions, generics
from api.serializers import UserSerializer, ContributorSerializer, ProjectDetailSerializer, ProjectListSerializer, \
    CommentSerializer, IssueSerializer
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


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_class = ProjectDetailSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        queryset = Projects.objects.filter(author_user_id=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_class
        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContributorViewAll(viewsets.ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):

        project = get_object_or_404(Projects, id=project_id)

        if request.user.id == project.author_user_id_id:
            try:
                contributor = Contributors()
                contributor.project_id_id = project
                contributor.user_id_id = get_object_or_404(User, id=request.data['user_id'])
                contributor.role = request.data['role']
                contributor.permissions = request.data['permissions']
                data = {'user_id': contributor.user_id.id, 'project_id': contributor.project_id.id,
                        'permission': contributor.permission, 'role': contributor.role}
                print(data)
                print('je suis dans le try')
                contributor.save()
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:

                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        else:
            print('je susi dasn le else')
            return Response(status.HTTP_403_FORBIDDEN)


class DeleteContributeur(viewsets.ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['DELETE', 'POST'])
    def delete(self, request, user_id_id, *args, **kwargs):
        user_id_id = Contributors.objects.get(id=user_id_id)
        user_id_id.delete()
        return Response(status.HTTP_204_NO_CONTENT)
