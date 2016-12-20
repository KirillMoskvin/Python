from django.contrib import admin
from post.models import Post, Comments


# Register your models here.

class PostInline(admin.StackedInline):
	model = Comments
	extra = 2



class PostAdmin(admin.ModelAdmin):
	fields = ["post_title", "post_text", "post_date"]
	inlines = [PostInline]
	list_filter = ['post_date']
#	post_display = ['article_title', 'article_date']

admin.site.register(Post, PostAdmin)