from django.core.management.base import BaseCommand

from food.models import Tag

ALL_TAGS = (
    ('Завтрак', 'breakfast', 'orange'),
    ('Обед', 'lunch', 'green'),
    ('Ужин', 'dinner', 'purple'),
)


class Command(BaseCommand):
    help = 'Load tags'

    def handle(self, *args, **options):
        for item in ALL_TAGS:
            tag, _ = Tag.objects.get_or_create(
                name=item[0],
                slug=item[1],
                color=item[2]
            )
            if tag:
                print(f'Add {item[1]} tag.')
