import csv

from django.core.management.base import BaseCommand

from food.models import Ingridient


class Command(BaseCommand):
    help = 'Load ingredients'

    def handle(self, *args, **options):
        with open('ingredients.csv') as file:
            reader = csv.reader(file)
            ingridients_cnt = 0
            for row in reader:
                ingridients_cnt += 1
                ingridient, _ = Ingridient.objects.get_or_create(
                    name=row[0], unit=row[1]
                )
                print(ingridient.id, row)

        print('TOTAL:', ingridients_cnt)
