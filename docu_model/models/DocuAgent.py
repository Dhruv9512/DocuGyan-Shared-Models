from django.db import models

class DocuProcess(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    project_id = models.CharField(max_length=50, unique=True, primary_key=True) 
    
    user_uuid = models.CharField(
        max_length=255, 
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

    reference_urls = models.JSONField(default=list, help_text="List of Vercel Blob URLs for reference docs")
    question_urls = models.JSONField(default=list, blank=True, help_text="List of Vercel Blob URLs for question docs")
    text_questions = models.JSONField(default=list, blank=True, help_text="List of text questions")

    results_url = models.URLField(
        max_length=500,
        blank=True, 
        null=True, 
        help_text="Vercel Blob URL where the LLM final Q&A results are stored"
    )
    error_message = models.TextField(blank=True, null=True)

    metadata = models.JSONField(default=dict, blank=True, help_text="Execution metadata, token usage, time taken")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

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