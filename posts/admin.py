from django.contrib import admin
from .models import Post, Comment, Mention


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'caption_preview', 'moderation_status', 'created_at', 'likes_count']
    list_filter = ['moderation_status', 'created_at']
    search_fields = ['caption', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'likes_count']
    raw_id_fields = ['author']

    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Подпись'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'text_preview', 'moderation_status', 'created_at']
    list_filter = ['moderation_status', 'created_at']
    search_fields = ['text', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['author', 'post']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст'


@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ['id', 'mentioned_user', 'post', 'comment', 'email_sent', 'created_at']
    list_filter = ['email_sent', 'created_at']
    search_fields = ['mentioned_user__username']
    readonly_fields = ['created_at']
    raw_id_fields = ['mentioned_user', 'post', 'comment']

