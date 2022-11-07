from django.contrib import admin
from .models import Projects, Comments, Contributors, Issues


admin.site.register(Projects)
admin.site.register(Contributors)
admin.site.register(Issues)
admin.site.register(Comments)