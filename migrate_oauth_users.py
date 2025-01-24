import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "my_app.settings"
)  # Replace with your project settings
import django

django.setup()

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


def migrate_oauth_users():
    social_accounts = SocialAccount.objects.all()
    for social_account in social_accounts:
        user = social_account.user  # Get the associated user (might be None)
        extra_data = social_account.extra_data

        if not user:
            # Create a new User
            user = User.objects.create_user(
                username=extra_data.get("username")
                or extra_data.get("email"),  # Choose a username
                email=extra_data.get("email"),
                first_name=extra_data.get("first_name"),
                last_name=extra_data.get("last_name"),
            )
            social_account.user = user
            social_account.save()
        else:
            # Update existing User (if needed)
            if not user.email and extra_data.get("email"):
                user.email = extra_data.get("email")
                user.save()


if __name__ == "__main__":
    migrate_oauth_users()
