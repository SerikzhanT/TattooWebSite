from django.contrib import admin
from django.http.request import HttpRequest

from .models import Style, Tattoo


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}  # slug


@admin.register(Tattoo)
class TattooAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    ordering = ('title', 'created_at')

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}
