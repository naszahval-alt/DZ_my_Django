import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from datetime import datetime

class Command(BaseCommand):
    help = 'Import phones from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='phones.csv',
            help='Path to CSV file',
        )

    def handle(self, *args, **options):
        file_path = options['file']

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                phone, created = Phone.objects.update_or_create(
                    slug=row['slug'],
            defaults={
                'name': row['name'],
                'price': row['price'],
                'image': row['image'],
                'release_date': datetime.strptime(row['release_date'], '%Y-%m-%d').date(),
                'lte_exists': row['lte_exists'].lower() in ['true', '1', 'yes'],
            }
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {row["name"]}')
        )
