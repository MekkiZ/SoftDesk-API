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


class IssueDetailsForProjectViewSet(viewsets.ModelViewSet):
    serializer_class = IssueAddForProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_issue_id = self.kwargs['project_id']
        return Issues.objects.filter(project_id=project_issue_id)

    def post(self, request, project_id, *args, **kwargs):

        project = get_object_or_404(Projects, id=project_id)
        if request.user.id == project.author_user_id_id:
            try:
                issues = Issues()
                issues.project_id = project
                issues.title = request.data['title']
                issues.desc = request.data['desc']
                issues.tag = request.data['tag']
                issues.priority = request.data['priority']
                issues.status = request.data['status']
                issues.author_user_id = get_object_or_404(User, id=project.author_user_id.id)
                issues.assignee_user_id = get_object_or_404(User, id=request.data['assignee_user_id'])
                data = {'title': issues.title,
                        'project_id': issues.project_id.id,
                        'desc': issues.desc,
                        'tag': issues.tag,
                        'priority': issues.priority,
                        'status': issues.status,
                        'assignee_user_id': issues.author_user_id.id
                        }
                issues.save()
                return Response(data, status=status.HTTP_201_CREATED)
            except IndexError as exc:
                return Response(str(exc), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(None, status=status.HTTP_403_FORBIDDEN)


class IssuesModifyView(APIView):
    serializer_class = IssueAddForProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id, issues_id):
        issue_to_get = Issues.objects.filter(Q(project_id=project_id) & Q(id=issues_id))
        serializer = IssueSerializer(issue_to_get, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Issues.objects.filter(project_id_id=project_id)

    def put(self, request, issues_id, *args, **kwargs):
        issues = Issues.objects.get(id=issues_id)
        serializer = IssueAddForProjectSerializer(issues, data=request.data)
        data = request.data
        if serializer.is_valid():
            issues.title = data['title']
            issues.desc = data['desc']
            issues.tag = data['tag']
            issues.priority = data['priority']
            issues.status = data['status']
            issues.author_user_id = User.objects.get(id=data['author_user_id'])
            issues.assignee_user_id = User.objects.get(id=data['assignee_user_id'])
            issues.save()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, issues_id, project_id, *args, **kwargs):
        f = Issues.objects.filter(Q(id=issues_id) & Q(project_id_id=project_id))
        f.delete()
        return Response(status.HTTP_200_OK)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContributorViewAll(viewsets.ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # https://www.django-rest-framework.org/api-guide/filtering/
        project_id = self.kwargs['project_id']
        return Contributors.objects.filter(project_id=project_id)

    def post(self, request, project_id):

        project = get_object_or_404(Projects, id=project_id)

        if request.user.id == project.author_user_id_id:
            try:
                contributor = Contributors()
                contributor.project_id = project
                contributor.user_id = get_object_or_404(User, id=request.data['user_id'])
                contributor.role = request.data['role']
                contributor.permission = request.data['permission']
                data = {'user_id': contributor.user_id.id, 'project_id': contributor.project_id.id,
                        'permission': contributor.permission, 'role': contributor.role}
                f = Contributors.objects.filter(project_id=contributor.project_id)
                if f.count() >= 1:
                    f.delete()
                contributor.save()
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:

                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status.HTTP_403_FORBIDDEN)


class DeleteContributeur(viewsets.ModelViewSet):
    serializer_class = ContributorDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # https://www.django-rest-framework.org/api-guide/filtering/
        user = self.kwargs['user_id_id']
        return Contributors.objects.filter(Q(user_id=user) & Q(project_id=self.kwargs['project_id'])
                                           )

    @action(detail=False, methods=['DELETE'])
    def delete(self, request, user_id_id, *args, **kwargs):
        user = self.kwargs['user_id_id']
        f = Contributors.objects.filter(project_id=self.kwargs['project_id'])
        f.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class CommentsAddApiView(APIView):
    serializer_class = CommentAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comments.objects.filter(issue_id_id=self.kwargs['issues_id'])

    def get(self, request, project_id, issues_id):
        Comments.objects.filter(issue_id_id=issues_id)
        Issues.objects.filter(project_id_id=project_id)
        comments = Comments.objects.filter(issue_id_id=issues_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id, issues_id):

        issues = get_object_or_404(Issues, id=issues_id)
        Issues.objects.filter(project_id_id=project_id)
        if request.user.id == request.user.id:
            try:
                comment = Comments()
                comment.issue_id_id = issues.id
                comment.description = request.data['description']
                comment.author_user_id = User.objects.get(id=request.data['author_user_id'])
                print(comment.author_user_id_id)
                comment.save()
                data = {
                    'issue_id': comment.issue_id_id,
                    'description': comment.description,
                    'author': comment.author_user_id.id,
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except comment.DoesNotExist as exc:
                return Response(str(exc), status=status.HTTP_403_FORBIDDEN)
        else:

            return Response(None, status=status.HTTP_403_FORBIDDEN)
