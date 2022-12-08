from django.core.management.base import BaseCommand, CommandError
from users.models import CustomUser
from django.db.models import Q
from django.utils import timezone


class Command(BaseCommand):
    help = 'Make user as active e.g. \
            python manage.py update_status False --all; \
            python manage.py update_status False --ids 1 2 3'

    def add_arguments(self, parser):
        # Positional argument
        parser.add_argument('is_active', choices=['True', 'False'], help="Given status")

        # Optional argument
        parser.add_argument('--ids', nargs='+', type=int, help="Update specific users as given ids")
        parser.add_argument('--all', action='store_true', help="Update all users")
        

    def handle(self, *args, **options):
        is_active = options['is_active']
        try:
            if options['all']:
                query = CustomUser.objects.filter(~Q(is_active=is_active), is_superuser=False)
                self.stdout.write(self.style.SUCCESS('Successfully updated user'))
            elif options['ids']:
                query = CustomUser.objects.filter(~Q(is_active=is_active), is_superuser=False, id__in=options['ids'])
            else:
                return self.stdout.write(self.style.WARNING('Specify ids[1,3,..] or --all to update users'))
        except Exception as e:
            raise CommandError(e)

        query.update(is_active=is_active)

        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        self.stdout.write(self.style.SUCCESS('Updated usres successfully.'))


"""
---------DEMO COMMAND----------
python manage.py update_status False --all
python manage.py update_status False --ids 1 2 3
"""
