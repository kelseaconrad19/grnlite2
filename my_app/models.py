from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="customuser_set", blank=True
    )


class CustomUserGroup(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class CustomUserPermission(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


class Profile(models.Model):
    ROLE_CHOICES = [
        ("author", "Author"),
        ("beta_reader", "Beta Reader"),
        ("admin", "Admin"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text="Role of the user",
    )
    user = models.OneToOneField(
        User,  # Reference the default User model
        on_delete=models.CASCADE,
        help_text="User who owns the profile",
    )
    def is_author(self):
        return self.role == 'author'

    def is_reader(self):
        return self.role == 'beta_reader'
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class MyModel(models.Model):
    field1 = models.CharField(max_length=100)

    class Meta:
        db_table = "my_table_name"


class Keyword(models.Model):
    name = models.CharField(
        max_length=100, null=False, help_text="Keyword for tagging manuscripts"
    )
    CATEGORY_CHOICES = [
        ("genre", "Genre"),
        ("theme", "Theme"),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        null=False,
        help_text="Category of the keyword",
    )

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
class BetaReader(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="beta_reader_profile",
        help_text="The profile associated with this beta reader",
    )
    experience = models.TextField(
        null=True, blank=True, help_text="Summary of the beta reader's experience"
    )
    keywords = models.ManyToManyField(
        "Keyword",
        related_name="beta_readers",
        blank=True,
        help_text="Keywords the beta reader is interested in",
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Average rating for this beta reader"
    )
    total_reviews = models.PositiveIntegerField(
        default=0, help_text="Total number of reviews completed by the beta reader"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the beta reader profile was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When the beta reader profile was last updated"
    )

    def __str__(self):
        return f"{self.profile.user.username} - Beta Reader"

    def update_rating(self, new_rating):
        """
        Updates the average rating based on a new rating.
        """
        total_ratings = self.total_reviews * (self.rating or 0)
        self.total_reviews += 1
        self.rating = (total_ratings + new_rating) / self.total_reviews
        self.save()


# class FeedbackCategory(models.Model):
#     name = models.CharField(max_length=100, unique=True, help_text="Feedback category name")
#     description = models.TextField(null=True, blank=True, help_text="Description of the category")
#     is_active = models.BooleanField(default=True, help_text="Is this category active and selectable?")


#     def __str__(self):
#         return self.name


class Feedback(models.Model):
    manuscript = models.ForeignKey(
        "Manuscript", on_delete=models.CASCADE, related_name="feedbacks"
    )
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    plot = models.TextField(null=True, blank=True)
    characters = models.TextField(null=True, blank=True)
    pacing = models.TextField(null=True, blank=True)
    worldbuilding = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    
class FeedbackTopic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FeedbackQuestion(models.Model):
    question_text = models.TextField(help_text="The text of the feedback question")
    is_active = models.BooleanField(
        default=True, help_text="Is this question active and selectable?"
    )
    topic = models.ForeignKey(FeedbackTopic, on_delete=models.CASCADE, related_name="questions", null=True, blank=True)

    def __str__(self):
        return f"{self.question_text}"

    class Meta:
        abstract = False


    

class Manuscript(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("in_review", "In Review"),
        ("completed", "Completed"),
    ]
    title = models.CharField(max_length=255)
    file_path = models.FileField(upload_to="manuscripts/")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="draft", null=False, blank=True, help_text="Status of the manuscript")
    keywords = models.ManyToManyField("Keyword", blank=True, through="Manuscript_keywords")
    feedback_topics = models.ManyToManyField("FeedbackTopic", blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    beta_readers_needed = models.PositiveIntegerField(null=True, blank=True)
    cover_art = models.ImageField(upload_to="cover_art/", null=True, blank=True)
    nda_required = models.BooleanField(default=False)
    nda_file = models.FileField(upload_to="nda_files/", null=True, blank=True)
    plot_summary = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manuscripts")
    
    class Meta:
        permissions = [
            ("can_view_reader_dashboard", "Can view reader dashboard"),
            ("can_view_author_dashboard", "Can view author dashboard"),
        ]

    def __str__(self):
        return self.title
    

    # New fields for feedback categories and questions
    # feedback_categories = models.ManyToManyField(
    #     FeedbackCategory,
    #     related_name="manuscripts",
    #     blank=True,
    #     help_text="Selected feedback categories for this manuscript",
    # )
    # feedback_questions = models.ManyToManyField(
    #     FeedbackQuestion,
    #     related_name="manuscripts",
    #     blank=True,
    #     help_text="Selected feedback questions for this manuscript",
    # )
    @classmethod
    def count_drafts(cls, user):
        """Count the number of manuscripts with 'draft' status for a specific user."""
        return cls.objects.filter(author=user, status="draft").count()
    
    def __str__(self):
        return self.title
    
class ReaderManuscript(models.Model):
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reader_manuscripts",
        help_text="The reader associated with the manuscript"
    )
    manuscript = models.ForeignKey(
        Manuscript,
        on_delete=models.CASCADE,
        related_name="readers",
        help_text="The manuscript chosen by the reader"
    )
    status = models.CharField(
        max_length=50,
        choices=[('in_progress', 'In Progress'), ('completed', 'Completed')],
        default='in_progress'
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reader.username} - {self.manuscript.title}"


class ManuscriptFeedbackPreference(models.Model):
    manuscript = models.ForeignKey(
        Manuscript, on_delete=models.CASCADE, related_name="feedback_preferences"
    )
    question = models.ForeignKey(
        FeedbackQuestion,
        on_delete=models.CASCADE,
        related_name="manuscript_preferences",
    )

    def __str__(self):
        return f"{self.manuscript.title} - {self.question.question_text}"
    
class Manuscript_keywords(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE)
    keyword = models.ForeignKey('Keyword', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "my_app_manuscript_keywords"
    def __str__(self):
        return f"{self.manuscript.title} - {self.keyword.name}"


class FeedbackResponse(models.Model):
    manuscript = models.ForeignKey(
        Manuscript,
        on_delete=models.CASCADE,
        related_name="feedback_responses",
        help_text="The manuscript this feedback is for",
    )
    reader = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        limit_choices_to={
            "groups__name": "beta_reader"
        },  # Adjust group or role logic if necessary
        related_name="feedback_given",
        help_text="The beta reader providing the feedback",
    )
    question = models.ForeignKey(
        FeedbackQuestion,
        on_delete=models.CASCADE,
        help_text="The specific feedback question being answered",
    )
    answer_text = models.TextField(
        null=True, blank=True, help_text="The beta reader's answer to the question"
    )
    review_date = models.DateTimeField(
        auto_now_add=True, help_text="When the feedback was submitted"
    )

    def __str__(self):
        return f"Feedback by {self.reader.username} for {self.manuscript.title} - Question: {self.question.id}"


class AuthorSettings(models.Model):
    author = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="settings",
        help_text="The author this settings configuration belongs to",
    )
    feedback_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Customizable preferences for the type of feedback the author wants",
    )
    notification_preferences = models.JSONField(
        default=dict, blank=True, help_text="Notification settings for the author"
    )
    profile_visibility = models.BooleanField(
        default=True, help_text="Whether the author's profile is public or private"
    )
    auto_submit_feedback = models.BooleanField(
        default=False,
        help_text="Automatically submit feedback requests when manuscripts are uploaded",
    )
    created_at = models.DateTimeField(
        default=now, help_text="Timestamp of when the settings were created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp of when the settings were last updated"
    )

    def __str__(self):
        return f"Settings for {self.author.username}"


class Resource(models.Model):
    title = models.CharField(
        max_length=150, null=False, help_text="Title of the resource"
    )
    description = models.TextField(
        null=True, blank=True, help_text="Description of the resource"
    )
    file_path = models.FileField(
        upload_to="resources/",
        null=False,
        help_text="Path to the uploaded resource file",
    )
    category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Category of the resource (e.g., 'Templates', 'Guides')",
    )
    tags = models.TextField(
        null=True,
        blank=True,
        help_text="Comma-separated tags for search and categorization",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the resource was uploaded"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the resource was last updated"
    )

    def __str__(self):
        return self.title


class ResourceInteraction(models.Model):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="interactions"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="resource_interactions",
        help_text="The user interacting with the resource",
    )
    interaction_type = models.CharField(
        max_length=50,
        choices=[("download", "Download"), ("favorite", "Favorite")],
        help_text="Type of user interaction",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp of the interaction"
    )

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.resource.title}"


class Notification(models.Model):
    STATUS_CHOICES = [
        ("read", "Read"),
        ("not_read", "Not Read"),
    ]
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="The user receiving the notification",
    )
    message = models.TextField(null=False, help_text="Message of the notification")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=False,
        help_text="Read status of the notification",
        default="not_read",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the notification was sent"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the notification was read"
    )


class BetaReaderApplication(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ("applied", "Applied"),  # Application submitted but not yet reviewed
        ("approved", "Approved"),  # Beta reader accepted by the author
        ("rejected", "Rejected"),  # Beta reader declined
    ]

    manuscript = models.ForeignKey(
        "Manuscript",
        on_delete=models.CASCADE,
        related_name="applications",
        help_text="The manuscript this application is for",
    )
    beta_reader = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        limit_choices_to={
            "groups__name": "beta_reader"
        },  # Or another method of filtering beta readers
        related_name="applications",
        help_text="The beta reader submitting the application",
    )
    reader_rating = models.IntegerField(
        null=True,
        blank=True,
        help_text="Optional rating given to the beta reader for their application",
    )
    attachment = models.FileField(
        upload_to="beta_reader_applications/",
        null=True,
        blank=True,
        help_text="Optional attachment for the beta reader's application",
    )
    status = models.CharField(
        max_length=10,
        choices=APPLICATION_STATUS_CHOICES,
        default="applied",
        help_text="Status of the application",
    )
    application_date = models.DateTimeField(
        auto_now_add=True, help_text="When the application was submitted"
    )
    review_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the application was reviewed by the author",
    )
    cover_letter = models.TextField(
        null=True,
        blank=True,
        help_text="Optional message from the beta reader to the author",
    )


class ManuscriptKeywords(models.Model):
    manuscript = models.ForeignKey("Manuscript", on_delete=models.CASCADE)
    keyword = models.ForeignKey("Keyword", on_delete=models.CASCADE)
    
@receiver(post_save, sender=User)  # Replace `User` with `CustomUser` if you're using a custom user model
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
@receiver(post_save, sender=Profile)
def create_beta_reader(sender, instance, created, **kwargs):
    if created and instance.role == "beta_reader":
        BetaReader.objects.create(profile=instance)
