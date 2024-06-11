from celery import shared_task
from phonebook.models import Contact

@shared_task
def delete_contacts(contact_ids):
    Contact.objects.filter(id__in=contact_ids).delete()
