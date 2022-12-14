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

    def __str__(self):
        return f'{self.title} {self.type}'


class Contributors(models.Model):
    PERMISSION_CHOICES = (
        ('A', 'Author'),
        ('R', 'Responsable'),
        ('C', 'Creator')

    )

    ROLE_CHOICES = (
        ('DEV', 'DEV'),
        ('Designer', 'Designer'),
        ('Chef de project', 'Chef de project'),
        ('Lead', 'Lead')

    )

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    permission = models.CharField(max_length=1, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)


class Issues(models.Model):
    PRIORITY_CHOICES = (
        ('L', 'FAIBLE'),
        ('M', 'MOYENNE'),
        ('H', 'ÉLEVÉE')

    )

    TAG_CHOICES = (
        ('BUG', 'BUG'),
        ('AMÉLIORATION', 'AMÉLIORATION'),
        ('TÂCHE', 'TÂCHE')

    )
    STATUS_CHOICES = (
        ('DO', 'À faire'),
        ('IN PROGRESS', 'En cours'),
        ('FINISH', 'Terminé')

    )
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, choices=TAG_CHOICES)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='project_id')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_user_id')
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignee_user_id')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.id}) '


class Comments(models.Model):
    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_time} {self.id}'
