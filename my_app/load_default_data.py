from django.core.management.base import BaseCommand
from my_app.models import Profile, Manuscript, AuthorSettings, YourModel
import pytest
from django.core.management import call_command


class Command(BaseCommand):
    help = "Load default data into the database"

    def handle(self, *args, **kwargs):
        Profile.objects.create(name="Default Profile", genre="Fiction")
        Manuscript.objects.create(
            title="Default Manuscript", content="This is a default manuscript."
        )
        AuthorSettings.objects.create(
            author_name="Default Author", bio="This is a default bio."
        )
        YourModel.objects.create(field1="value1", field2="value2")
        self.stdout.write(self.style.SUCCESS("Successfully loaded default data"))


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("load_default_data")
