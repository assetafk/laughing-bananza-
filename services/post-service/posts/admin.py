from django.contrib import admin
from .models import Post, Comment, Mention


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author_id', 'moderation_status', 'created_at', 'likes_count']
    list_filter = ['moderation_status', 'created_at']
    search_fields = ['caption']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author_id', 'post', 'moderation_status', 'created_at']
    list_filter = ['moderation_status', 'created_at']
    search_fields = ['text']


@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ['id', 'mentioned_user_id', 'post', 'comment', 'email_sent', 'created_at']
    list_filter = ['email_sent', 'created_at']

