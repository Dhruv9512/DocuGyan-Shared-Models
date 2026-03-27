from django.db import models
import uuid


class DocuProcess(models.Model):
    # ==========================================
    # Choices Definitions
    # ==========================================
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'

    class IngestionStrategyChoices(models.TextChoices):
        VECTOR = 'VECTOR', 'Vector DB'
        GRAPH = 'GRAPH', 'Knowledge Graph'
        VECTORLESS = 'VECTORLESS', 'Vectorless / Raw Text'
        UNKNOWN = 'UNKNOWN', 'Unknown'

    # ==========================================
    # Core Identifiers
    # ==========================================
    project_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    
    user_uuid = models.UUIDField(
        db_index=True,
        blank=True,
        null=True,
        help_text="The unique ID of the user from the authentication service"
    )

    task_id = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.PENDING,
        db_index=True
    )

    # ==========================================
    # Inputs
    # ==========================================
    reference_urls = models.JSONField(
        default=list, 
        help_text="List of Vercel Blob URLs for reference docs"
    )
    question_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text="List of Vercel Blob URLs for question docs"
    )

    # ==========================================
    # Intermediate Pipeline Artifacts
    # ==========================================
    extracted_doc_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text="Vercel Blob URLs of the markdown-extracted reference documents"
    )
    refined_question_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text="Vercel Blob URLs of the LLM-refined questions"
    )
    ingestion_strategy = models.CharField(
        max_length=20,
        choices=IngestionStrategyChoices.choices,
        default=IngestionStrategyChoices.UNKNOWN,
        help_text="How this document was indexed (determines future retrieval options)"
    )
    collection_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of the vector DB collection or graph DB namespace where this document is stored"
    )

    # ==========================================
    # Final Outputs & Errors
    # ==========================================
    results_url = models.URLField(
        max_length=500,
        blank=True, 
        null=True, 
        help_text="Vercel Blob URL where the LLM final Q&A results are stored"
    )
    error_message = models.TextField(blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ==========================================
    # Model Methods & Meta
    # ==========================================
    def __str__(self):
        return f"{self.project_id} - {self.status}"

    class Meta:
        ordering = ['-created_at'] 
        verbose_name = "Document Process"
        verbose_name_plural = "Document Processes"
        indexes = [
            models.Index(fields=['user_uuid', '-created_at']),
            models.Index(fields=['user_uuid', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]