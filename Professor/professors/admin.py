from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'email', 'h_index', 'created_at']
    list_filter = ['university', 'created_at']
    search_fields = ['name', 'university', 'email', 'research_interests']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('profile_picture', 'name', 'university', 'email')
        }),
        ('Academic Information', {
            'fields': ('h_index', 'research_interests', 'famous_articles')
        }),
        ('Online Profiles', {
            'fields': ('google_scholar_url', 'researchgate_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
