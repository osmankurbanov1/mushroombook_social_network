from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    """
    Posts
    """
    list_display = ("post_author", "post_is_published", "count_of_post_views")


class CommentAdmin(MPTTModelAdmin, admin.ModelAdmin):
    """
    Comments to the posts
    """
    list_display = ("comment_author", "post", "created_date", "update_date", "is_published")
    mptt_level_indent = 10


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
