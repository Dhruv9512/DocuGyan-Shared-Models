from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, DocuProcess, ChatSession, ChatMessage


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
    list_display = ('project_id', 'status', 'title', 'description', 'ingestion_strategy', 'collection_name', 'grooming_data','user_uuid', 'created_at', 'updated_at')
    
    list_filter = ('status', 'collection_name', 'created_at')
    
    # Added collection_name to search fields so you can search by Vector DB namespace
    search_fields = ('project_id', 'user_uuid', 'task_id', 'collection_name', 'error_message', 'title', 'description')
    
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


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    # Removed thread_id
    list_display = (
        'session_id', 
        'title', 
        'project', 
        'user', 
        'created_at'
    )
    
    list_filter = ('created_at', 'project')
    
    search_fields = (
        'session_id', 
        'title', 
        'user__email', 
        'project__project_id'
    )
    
    # Removed the duplicate 'session_id'
    readonly_fields = ('session_id', 'created_at')
    
    ordering = ('-created_at',)

    # Removed the "LangGraph Internal" section and merged the concept
    fieldsets = (
        ('Session Details (LangGraph Thread)', {
            'fields': ('session_id', 'title', 'created_at')
        }),
        ('Relationships', {
            'fields': ('project', 'user')
        }),
    )

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    # 1. Update display to show both sides of the conversation
    list_display = ('message_id', 'session', 'user_query_preview', 'assistant_response_preview', 'created_at')
    
    # 2. Remove 'role' filter as it no longer exists
    list_filter = ('created_at',)
    
    # 3. Update search to look through both query and response
    search_fields = ('message_id', 'session__session_id', 'user_query', 'assistant_response')
    
    readonly_fields = ('message_id', 'created_at')
    
    # Optional: Change to '-created_at' to see the newest chats at the top
    ordering = ('-created_at',) 

    fieldsets = (
        ('Conversation Turn', {
            'fields': ('message_id', 'user_query', 'assistant_response', 'created_at')
        }),
        ('Relationships', {
            'fields': ('session',)
        }),
    )

    # Helper methods to keep the list view clean
    def user_query_preview(self, obj):
        return obj.user_query[:50] + "..." if len(obj.user_query) > 50 else obj.user_query
    user_query_preview.short_description = 'User Query'

    def assistant_response_preview(self, obj):
        return obj.assistant_response[:50] + "..." if len(obj.assistant_response) > 50 else obj.assistant_response
    assistant_response_preview.short_description = 'Assistant Response'