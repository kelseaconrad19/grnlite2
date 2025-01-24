from django.core.management.base import BaseCommand
from my_app.models import FeedbackTopic

class Command(BaseCommand):
    help = "Populates predefined feedback topics"

    def handle(self, *args, **kwargs):
        topics = [
            "Plot Structure",
            "Character Development",
            "Setting and Worldbuilding",
            "Pacing",
            "Dialogue",
            "Overall Impressions",
        ]
        for topic in topics:
            FeedbackTopic.objects.get_or_create(name=topic)
        self.stdout.write(self.style.SUCCESS('Successfully added feedback topics!')) 