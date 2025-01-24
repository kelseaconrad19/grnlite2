from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from my_app.models import Profile


class Command(BaseCommand):
    help = 'Add dummy users (authors and beta readers)'

    def handle(self, *args, **kwargs):
        # Define dummy user data for authors
        authors_data = [
            {"username": "author1", "email": "author1@example.com", "password": "Password123", "role": "author"},
            {"username": "author2", "email": "author2@example.com", "password": "Password123", "role": "author"},
            {"username": "author3", "email": "author3@example.com", "password": "Password123", "role": "author"},
        ]

        # Define dummy user data for beta readers
        beta_readers_data = [
            {"username": "reader1", "email": "reader1@example.com", "password": "Password123", "role": "beta_reader"},
            {"username": "reader2", "email": "reader2@example.com", "password": "Password123", "role": "beta_reader"},
            {"username": "reader3", "email": "reader3@example.com", "password": "Password123", "role": "beta_reader"},
        ]

        # Add author users
        for user_data in authors_data:
            self.create_user_with_profile(user_data)

        # Add beta reader users
        for user_data in beta_readers_data:
            self.create_user_with_profile(user_data)

        self.stdout.write(self.style.SUCCESS("Dummy users (authors and beta readers) added successfully!"))

    def create_user_with_profile(self, user_data):
        # Create User
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={"email": user_data["email"]}
        )

        if created:
            user.set_password(user_data["password"])
            user.save()

            # Create Profile with the specified role
            Profile.objects.get_or_create(
                user=user,
                defaults={"role": user_data["role"]}
            )

            self.stdout.write(self.style.SUCCESS(f"Added user: {user.username}, Role: {user_data['role']}"))
        else:
            self.stdout.write(self.style.WARNING(f"User {user.username} already exists."))