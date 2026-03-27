from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, DocuProcess


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin panel for CustomUser.
    Overrides the default UserAdmin to remove 'username' and use 'email' instead.
    """
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'user_uuid')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'user_uuid')
    readonly_fields = ('user_uuid', 'last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_uuid')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name'),
        }),
    )


@admin.register(DocuProcess)
class DocuProcessAdmin(admin.ModelAdmin):
    """
    Admin panel for the DocuProcess model.
    Organizes pipeline steps into clean, collapsible sections.
    """
    # Added collection_name to the list display so you can easily see where data is stored
    list_display = ('project_id', 'status', 'ingestion_strategy', 'collection_name', 'user_uuid', 'created_at', 'updated_at')
    
    list_filter = ('status', 'ingestion_strategy', 'created_at')
    
    # Added collection_name to search fields so you can search by Vector DB namespace
    search_fields = ('project_id', 'user_uuid', 'task_id', 'collection_name', 'error_message')
    
    # Core identifiers and timestamps shouldn't be manually edited
    readonly_fields = ('project_id', 'created_at', 'updated_at')

    # Groups fields into collapsible sections for a cleaner UI
    fieldsets = (
        ('Core Identifiers', {
            'fields': ('project_id', 'user_uuid', 'task_id', 'status')
        }),
        ('Inputs', {
            'fields': ('reference_urls', 'question_urls'),
            'classes': ('collapse',), 
        }),
        ('Intermediate Pipeline Artifacts', {
            # Included collection_name next to ingestion_strategy
            'fields': ('ingestion_strategy', 'collection_name', 'extracted_doc_urls', 'refined_question_urls'),
            'classes': ('collapse',),
        }),
        ('Final Outputs & Errors', {
            'fields': ('results_url', 'error_message'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )