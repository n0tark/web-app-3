from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import delete_contacts


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        send_mail('Successful registration', f'You signed up with your name {name} and email {email}', '', [email])
        return render(request, 'contactForm/success.html', {'name': name, 'email': email})
    # else:
    #     return render(request, 'contactForm/failed.html')

    return render(request, 'contactForm/index.html')


def get_results_data():
    return []

def delete_selected_contacts(request):
    if request.method == 'POST':
        contact_ids = request.POST.getlist('contact_ids[]')  # assuming contact_ids is a list of contact IDs
        delete_contacts.delay(contact_ids)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

def results_table(request):
    results_data = get_results_data()
    context = {
        'results_data': results_data,
    }

    return render(request, 'results_table.html', context)


