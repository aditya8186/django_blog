from django.contrib import admin
from .models import Blogger, BlogPost, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    fields = ['user', 'bio']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('title', 'description')
    inlines = [CommentInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'description')
        }),
        ('Dates', {
            'fields': ('post_date',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('description', 'post_date', 'author', 'blog_post')
    list_filter = ('post_date', 'author')
    search_fields = ('description',)
