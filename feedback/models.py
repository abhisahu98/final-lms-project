from django.db import models

class Feedback(models.Model):
    course_id = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    rating = models.IntegerField()
    feedback_text = models.TextField()
    processed_feedback = models.TextField(blank=True, null=True)  # Store GPT-4 processed feedback
    processed = models.BooleanField(default=False)  # Flag to indicate processing status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_id} - {self.instructor} - Processed: {self.processed}"
