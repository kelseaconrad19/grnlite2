from django.core.management.base import BaseCommand
from my_app.models import Manuscript, User, Keyword, FeedbackTopic


class Command(BaseCommand):
    help = "Add dummy data, including manuscripts, authors, and beta readers."

    def handle(self, *args, **kwargs):
        # Add dummy manuscripts
        self.add_dummy_manuscripts()
        self.stdout.write(self.style.SUCCESS("Dummy manuscripts added successfully!"))

    def add_dummy_manuscripts(self):
        # Fetch existing author users
        authors = User.objects.filter(profile__role="author")

        if not authors.exists():
            self.stdout.write(self.style.WARNING("No authors found. Add authors first."))
            return

        # Fetch or create keywords
        keyword1, _ = Keyword.objects.get_or_create(name="Fantasy", category="genre")
        keyword2, _ = Keyword.objects.get_or_create(name="Adventure", category="genre")

        # Fetch or create feedback topics
        topic1, _ = FeedbackTopic.objects.get_or_create(name="Plot Structure")
        topic2, _ = FeedbackTopic.objects.get_or_create(name="Character Development")

        # Dummy manuscript data
        manuscripts_data = [
            {
                "title": "The Hidden Kingdom",
                "file_path": "static/Front_End/Images/HiddenKingdom.jpeg",
                "status": "draft",
                "budget": 1200.00,
                "beta_readers_needed": 3,
                "plot_summary": "A gripping tale of a hidden kingdom and its secrets.",
            },
            {
                "title": "Journey to the Unknown",
                "file_path": "static/Front_End/Images/JourneyToUnknown.jpg",
                "status": "in_review",
                "budget": 1500.00,
                "beta_readers_needed": 2,
                "plot_summary": "An exciting adventure to uncover the unknown.",
            },
            {
                "title": "Whispers of the Ancients",
                "file_path": "static/Front_End/Images/WhisperOfTheAncients.jpg",
                "status": "submitted",
                "budget": 1000.00,
                "beta_readers_needed": 4,
                "plot_summary": "A story of ancient secrets threatening the modern world.",
            },
            {
                "title": "Tales of the Forgotten",
                "file_path": "static/Front_End/Images/TalesForgotten.jpeg",
                "status": "completed",
                "budget": 900.00,
                "beta_readers_needed": 5,
                "plot_summary": "A forgotten tale that could change everything.",
            },
            {
                "title": "The Eternal Quest",
                "file_path": "/static/Front_End/Images/EternalQuest.jpeg",
                "status": "draft",
                "budget": 800.00,
                "beta_readers_needed": 3,
                "plot_summary": "A quest for eternity and the challenges it brings.",
            },
        ]

        # Assign manuscripts to authors in round-robin fashion
        for idx, manuscript_data in enumerate(manuscripts_data):
            author = authors[idx % authors.count()]  # Rotate through authors

            manuscript = Manuscript.objects.create(
                author=author,
                title=manuscript_data["title"],
                file_path=manuscript_data["file_path"],
                status=manuscript_data["status"],
                budget=manuscript_data["budget"],
                beta_readers_needed=manuscript_data["beta_readers_needed"],
                plot_summary=manuscript_data["plot_summary"],
            )

            # Assign keywords and feedback topics
            manuscript.keywords.add(keyword1, keyword2)
            manuscript.feedback_topics.add(topic1, topic2)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Added manuscript: {manuscript.title} by {author.username}"
                )
            )