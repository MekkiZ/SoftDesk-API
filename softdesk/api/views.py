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
    """
    Function get details to all users in API
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    """
    This function have to purpose to display the register part
    """
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
    """
    The first EndPoint of this project, with purpose to show projects of its contributors
    """
    serializer_class = ProjectListSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        get project of contributor
        :return: return querySet
        """
        user = self.request.user.id
        queryset = Projects.objects.filter(author_user_id=user)
        queryset_user_con = Contributors.objects.filter(user_id_id=user)

        if queryset:
            print('premuier if')
            return queryset
        elif queryset_user_con:
            print('deuxieme if')
            project_con = Contributors.objects.get(user_id_id=user)
            print(queryset_user_con)
            print(project_con.project_id_id)
            return Projects.objects.filter(id=project_con.project_id_id)
        else:
            return Projects.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        Function to delete Project, only the author can
        :param request: get request for statement and handle the query
        :param args: take url param
        :param kwargs: take url param
        :return: queryset and response 200
        """
        project = Projects.objects.get(id=kwargs.get('pk'))
        print(project)
        if Projects.objects.filter(author_user_id_id=request.user.id):
            project.delete()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_403_FORBIDDEN)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Class ViewSet for Comment to issue
    """
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueDetailsForProjectViewSet(APIView):
    """
    class viewSet issue detaisl for Project
    """
    serializer_class = IssueAddForProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id, *args, **kwargs):
        """
        Function to get all issues for project
        :param request: handle and use for statement
        :param project_id: ID project for query
        :return: querySet
        """
        # IssueSerializer
        project_issue_id = self.kwargs['project_id']
        issue_project = Issues.objects.filter(project_id=project_issue_id)
        project_get = Projects.objects.get(id=project_issue_id)

        serializer = IssueSerializer(issue_project, many=True)
        contributor = Contributors.objects.filter(Q(project_id_id=project_issue_id)
                                                  & Q(user_id_id=request.user.id)
                                                  )
        if contributor.exists():
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_404_NOT_FOUND)

    def post(self, request, project_id, *args, **kwargs):
        """
        Function to createIssue
        :param request: id user
        :param project_id: Porject id
        :param args:
        :param kwargs:
        :return: queryset
        """

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
        if request.user.id == issues.author_user_id_id:
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
        else:
            return Response(status.HTTP_403_FORBIDDEN)

    def delete(self, request, issues_id, project_id, *args, **kwargs):
        issues = Issues.objects.get(id=issues_id)
        if request.user.id == issues.author_user_id_id:
            f = Issues.objects.filter(Q(id=issues_id) & Q(project_id_id=project_id))
            f.delete()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_403_FORBIDDEN)


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
                f = Contributors.objects.filter(Q(permission=contributor.permission) &
                                                Q(role=contributor.role) &
                                                Q(project_id_id=contributor.project_id) &
                                                Q(user_id_id=contributor.user_id_id))
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
    def delete(self, request, project_id, user_id_id, *args, **kwargs):
        project = get_object_or_404(Projects, id=project_id)
        if request.user.id == project.author_user_id_id:
            user = self.kwargs['user_id_id']
            f = Contributors.objects.filter(user_id_id=user_id_id)
            f.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        else:
            return Response(status.HTTP_403_FORBIDDEN)


class CommentsAddApiView(APIView):
    serializer_class = CommentAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comments.objects.filter(issue_id_id=self.kwargs['issues_id'])

    def get(self, request, project_id, issues_id):
        user_contributor = Contributors.objects.filter(Q(user_id_id=request.user.id)
                                                       & Q(project_id_id=project_id))

        if user_contributor:
            Issues.objects.filter(project_id_id=project_id)
            comments = Comments.objects.filter(issue_id_id=issues_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'you are not contributor of this project contact your CTO'}
            return Response(data, status.HTTP_403_FORBIDDEN)

    def post(self, request, project_id, issues_id):

        issues = get_object_or_404(Issues, id=issues_id)
        Issues.objects.filter(project_id_id=project_id)

        if request.user.id == issues.author_user_id_id:

            try:
                comment = Comments()
                comment.issue_id_id = issues.id
                comment.description = request.data['description']
                comment.author_user_id = User.objects.get(id=request.data['author_user_id'])
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


class CommentModifyView(APIView):
    serializer_class = CommentAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id, issues_id, comment_id):

        Issues.objects.filter(project_id_id=project_id)
        comment_to_get = Comments.objects.filter(Q(issue_id_id=issues_id) & Q(id=comment_id))
        serializer = CommentAddSerializer(comment_to_get, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Issues.objects.filter(project_id_id=project_id)

    def put(self, request, issues_id, comment_id, *args, **kwargs):

        issues = Issues.objects.get(id=issues_id)
        comment = Comments.objects.get(id=comment_id)
        serializer = CommentAddSerializer(comment, data=request.data)
        data = request.data
        if request.user.id == issues.assignee_user_id_id or issues.author_user_id:
            if serializer.is_valid():
                comment.description = data['description']
                comment.author_user_id = User.objects.get(id=data['author_user_id'])
                comment.save()

                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status.HTTP_403_FORBIDDEN)

    def delete(self, request, issues_id, project_id, comment_id, *args, **kwargs):
        issues = Issues.objects.get(id=issues_id)
        if request.user.id == issues.author_user_id_id:
            Issues.objects.filter(project_id_id=project_id)
            f = Comments.objects.filter(Q(id=comment_id) & Q(issue_id_id=issues_id))
            f.delete()
            return Response(status.HTTP_200_OK)
        else:

            return Response(status.HTTP_403_FORBIDDEN)
