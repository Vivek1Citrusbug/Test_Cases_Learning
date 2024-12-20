from django.contrib import admin
from .domain.models import Like
# Register your models here.

class LikeAdmin(admin.ModelAdmin):
    list_display = ['post','user','created_at']

admin.site.register(Like,LikeAdmin)

