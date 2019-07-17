from django.contrib import admin

# Register your models here.
from app.models import Post, Category, Author, Comment, PostView

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)