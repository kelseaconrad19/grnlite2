from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from my_app.models import AuthorProfile, BetaReaderProfile
import random

class Command(BaseCommand):
    help = 'Seed users with a mix of authors and beta readers'

    def handle(self, *args, **kwargs):
        # Define user roles
        user_roles = ['author', 'beta_reader']

        # Define sample data
        first_names = ["Alex", "Jamie", "Taylor", "Jordan", "Casey", "Morgan", "Riley", "Drew"]
        last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis"]
        emails = ["example.com", "test.com", "sample.com"]

        # Seed users
        for _ in range(20):  # Adjust the number of users as needed
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
            email = f"{username}@{random.choice(emails)}"
            password = "password123"  # Use a secure password in a real application

            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Assign a role and create the corresponding profile
            role = random.choice(user_roles)
            if role == 'author':
                AuthorProfile.objects.create(user=user, bio="Author bio example", published_books=random.randint(0, 5))
            elif role == 'beta_reader':
                BetaReaderProfile.objects.create(
                    user=user,
                    bio="Beta reader bio example",
                    experience_years=random.randint(1, 10),
                    preferred_genres=random.sample(
                        ["Fantasy", "Romance", "Thriller", "Science Fiction", "Mystery", "Young Adult"], 3
                    )
                )

        self.stdout.write(self.style.SUCCESS('Users seeded successfully!'))