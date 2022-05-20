from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from wall.models import Post, Comment, PostLike


class PostLikeAdmin(admin.ModelAdmin):
    """
    Likes
    """
    # list_display = ("post", "user_liked")


class PostAdmin(admin.ModelAdmin):
    """
    Posts
    """
    list_display = ("post_author", "post_is_published", "list_of_mushrooms", "post_description")


class CommentAdmin(MPTTModelAdmin, admin.ModelAdmin):
    """
    Comments to the posts
    """
    list_display = ("comment_author", "post", "created_date", "update_date", "is_published")
    mptt_level_indent = 10


admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
