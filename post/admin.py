from django.contrib import admin
from post.models import Post

class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'status']
    list_display = ['title', 'posted_by', 'added_time']
    date_hierarchy = 'added_time'
    search_fields = ['title', 'user']

    def save_model(self, request, post, *args, **kwargs):
        post.user_id = request.user.id
        post.save()

admin.site.register(Post, PostAdmin)