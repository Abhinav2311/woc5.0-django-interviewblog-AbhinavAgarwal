from django.contrib import admin
from .models import Post, Profile, BlogComment
##



# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at','updated_at','slug')
    # prepopulated_fields = {'slug': ('title','author',), }

admin.site.register(Post, PostAdmin)

admin.site.register(Profile)

admin.site.register(BlogComment)

