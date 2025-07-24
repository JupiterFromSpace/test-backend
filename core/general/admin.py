from django.contrib import admin
from .models import Stone, StoneComment, StoneFAQ 

@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'stone_type', 'main_color')
    search_fields = ('name', 'stone_type', 'main_color')
    list_filter = ('stone_type',)

@admin.register(StoneComment)
class StoneCommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'stone', 'created_at')
    search_fields = ('author_name', 'text')
    list_filter = ('created_at',)

@admin.register(StoneFAQ)
class StoneFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'stone')
    search_fields = ('question', 'answer')
