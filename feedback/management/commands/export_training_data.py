import json
from django.core.management.base import BaseCommand
from feedback.models import Feedback, UserInteraction
from datetime import datetime


class Command(BaseCommand):
    help = 'Export feedback and interactions for GPT model training'

    def handle(self, *args, **kwargs):
        def serialize_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime to ISO 8601 string
            raise TypeError("Type not serializable")

        # Fetch data
        feedback_data = list(Feedback.objects.values())
        interaction_data = list(UserInteraction.objects.values())

        # Combine the data
        export_data = {
            "feedback": feedback_data,
            "interactions": interaction_data,
        }

        # Write to file
        with open('training_data.json', 'w') as f:
            json.dump(export_data, f, indent=4, default=serialize_datetime)

        self.stdout.write(self.style.SUCCESS('Exported data to training_data.json'))
