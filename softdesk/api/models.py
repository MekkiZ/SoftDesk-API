from django.db import models
from django.conf import settings


class Projects(models.Model):

    CHOICES = (
        ('FRONTEND', 'frontend'),
        ('BACKEND', 'backend'),
        ('IOS', 'ios'),
        ('ANDROID', 'android'),
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=CHOICES)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Contributors(models.Model):
    PERMISSION_CHOICES = (
        ('A', 'Author'),
        ('R', 'Responsable'),
        ('C', 'Creator')

    )

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    permission = models.CharField(max_length=1, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=255)


class Issues(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='project_id')
    status = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_user_id')
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignee_user_id')
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):

    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
