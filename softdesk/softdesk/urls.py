"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from api import views as v
from rest_framework.authtoken import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register('users', v.UserViewSet, basename='users')
router.register('projects', v.ProjectViewSet, basename='projects')
router.register('issues', v.IssueViewSet, basename='issues')
router.register('comments', v.CommentViewSet, basename='comments')
router.register('contributors', v.ContributorViewAll, basename='contributors')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path("get-details/", v.UserDetailAPI.as_view()),
    path('signup/', v.RegisterUserAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('api-token-auth', views.obtain_auth_token),
    path('signup/', v.RegisterUserAPIView.as_view()),
    path('projects/<int:project_id>/users/', v.ContributorViewSet.as_view({'get': 'list'})),
    path('projects/<int:project_id>/users/<int:user_id_id>', v.DeleteContributeur.as_view({'get': 'list'})),
    path('projects/<int:project_id>/issues/', v.IssueDetailsForProjectViewSet.as_view({'get': 'list'})),
    path('projects/<int:project_id>/issues/<int:issues_id>', v.IssuesModifyView.as_view()),
]
