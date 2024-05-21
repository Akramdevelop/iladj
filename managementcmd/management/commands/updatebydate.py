from django.core.management.base import BaseCommand
from datetime import date
from accounts.models import NessaCard


class Command(BaseCommand):
    help = 'Check dates and perform actions if they match the current date'

    def handle(self, *args, **options):
        current_date = date.today()

        # Retrieve objects with a date field matching the current date
        nessacards = NessaCard.objects.filter(datebirth=current_date)

        # Perform actions or changes to the matching objects
        for nessacard in nessacards:
            # Perform your actions here, e.g., obj.some_field = new_value
            #
            #
            #
            nessacard.childrennumber = int(nessacard.childrennumber) + 1
            if nessacard.childsex == 'male':
                nessacard.childrensex = nessacard.childrensex + ' + 1 ذكر'
            if nessacard.childsex == 'female':
                nessacard.childrensex = nessacard.childrensex + ' + 1 أنثى'
            if nessacard.childsex == 'twin':
                nessacard.childrensex = nessacard.childrensex + ' + 1 توأم'
            nessacard.lastbirth = nessacard.datebirth
            nessacard.datebirth = None
            nessacard.prevbirth = nessacard.typeofbirth
            nessacard.childsex = None
            nessacard.typeofbirth = None
            nessacard.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully processed {len(nessacards)} objects.'))
