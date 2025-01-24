from django.core.management.base import BaseCommand
from my_app.models import FeedbackQuestion, FeedbackTopic


class Command(BaseCommand):
    help = 'Add feedback questions to the database'

    def handle(self, *args, **kwargs):
        # Define your feedback topics and associated questions
        data = {
    "Overall Impressions": [
        "What was your overall reaction to the manuscript?",
        "Did the story resonate with you emotionally? Why or why not?",
        "What aspects of the manuscript stood out to you the most?",
        "Were there any areas where the manuscript fell short of your expectations?",
        "Would you recommend this manuscript to others? Why or why not?",
    ],
    "Dialogue": [
        "Did the dialogue reflect the characters' personalities and relationships effectively?",
        "Were there moments where the dialogue felt especially authentic or impactful?",
        "Did any of the dialogue seem out of place or inconsistent with the setting or characters?",
        "Were the conversations engaging and easy to follow?",
        "Did the dialogue advance the plot or reveal character traits effectively?",
    ],
    "Pacing": [
        "Were there any parts of the story that felt too rushed or too slow?",
        "Did the pacing of key events keep you engaged?",
        "Were there any scenes you felt could have been expanded or condensed?",
        "Did the transitions between scenes feel smooth and natural?",
        "Was the balance of action and exposition effective throughout the manuscript?",
    ],
    "Setting and World-Building": [
        "Were the settings described vividly enough to immerse you in the story?",
        "Did the world-building feel cohesive and believable?",
        "Were there any places where you wanted more detail about the setting or world?",
        "Did the setting enhance the mood or themes of the story effectively?",
        "Were the rules or logic of the story's world clearly established?",
    ],
    "Character Development": [
        "Were the characters' motivations and arcs believable and compelling?",
        "Did you find the protagonist relatable or engaging? Why or why not?",
        "Were there any secondary characters that you wanted to know more about?",
        "Did the relationships between characters evolve in a satisfying way?",
        "Were there any inconsistencies in character behavior or development?",
    ],
    "Plot Structure": [
        "Did the story have a strong beginning, middle, and end?",
        "Were the plot twists or major developments surprising and well-executed?",
        "Did the story flow logically from one event to the next?",
        "Were there any plot holes or unresolved questions that detracted from the story?",
        "Was the climax and resolution satisfying?",
    ],
}

        # Add feedback topics and questions
        for topic_name, questions in data.items():
            # Create or get the feedback topic
            topic, created = FeedbackTopic.objects.get_or_create(name=topic_name)

            for question_text in questions:
                FeedbackQuestion.objects.get_or_create(
                    topic=topic,
                    question_text=question_text,
                    is_active=True,  # Mark questions as active by default
                )

        self.stdout.write(self.style.SUCCESS('New feedback questions added successfully!'))