from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Test help information for this command.'

    def add_arguments(self, parser):
        parser.add_argument('first', type=int, help="A number less than 100")
        parser.add_argument('second', nargs=3, type=str, help="Three strings arguments")
        parser.add_argument('--option1', default='default value', help="The option1 value")
        parser.add_argument('--option2', action='store_true', help="True if passed")

    
    def handle(self, *args, **options):
        if options['first'] < 100:
            self.stdout.write(self.style.SUCCESS('Great! The number %s is less then 100' %options['first']))
        else:
            raise CommandError('The number %s is greater then 100' % options['first'])

        for value in options['second']:
            self.stdout.write(self.style.SUCCESS(f'Value: {value}'))

        self.stdout.write(f'The value of --option1 is: {options["option1"]}')

        if options['option2']:
            self.stdout.write(self.style.SUCCESS('Option2 is True'))
        else:
            self.stdout.write(self.style.WARNING('Option2 is False'))
