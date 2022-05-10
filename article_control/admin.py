from django.contrib import admin
from .models import *

class ArticleCategoryModelAdmin(admin.ModelAdmin):
	list_display = ['category', 'created_at', 'updated_at']


class ArticleModelAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'category', 'created_at', 'updated_at']
	list_filter = ['author', 'category']
	search_fields = ['title', 'content']
	list_per_page = 10
	ordering = ['-created_at']
	filter_horizontal = ['author']
	raw_id_fields = ['author']
	date_hierarchy = 'created_at'
	


admin.site.register(ArticleCategoryModel, ArticleCategoryModelAdmin)
admin.site.register(ArticleModel)
