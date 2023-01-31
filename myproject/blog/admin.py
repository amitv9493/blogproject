from django.contrib import admin
from .models import Post, Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display= ['title', 'slug', 'author', 'publish', 'status']

    list_filter = ['status', 'created', 'publish', 'author']
    prepopulated_fields= {'slug': ('title',)}
    row_id_fields = ['author']
    date_hierarchy= 'publish'
    ordering= ['status', 'publish']
    search_fields = ['title', 'body']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
