from django.shortcuts import render
from phonebook.models import Contact
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# View to render the 'phones.html' template with all contacts
def phones(request):
    contacts = Contact.objects.all()
    return render(request, "phones.html", {"contacts": contacts})

# View to render the 'contactList.html' template with all contacts
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contactList.html', {'contacts': contacts})

# Add a user to the 'online_users' group
def user_online(user_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_add)('online_users', str(user_id))

# Remove a user from the 'online_users' group
def user_offline(user_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_discard)('online_users', str(user_id))

# View to get the count of online users (only accessible to superuser)
def online_users(request):
    if request.user.is_superuser:
        channel_layer = get_channel_layer()
        online_users = async_to_sync(channel_layer.group_channels)('online_users')
        return JsonResponse({'online_users_count': len(online_users)})
    else:
        return JsonResponse({'error': 'Only superuser can access this endpoint'}, status=403)

# API view to get authentication token for a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_auth_token(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


def delete_selected_contacts(request):
    if request.method == 'POST':
        contact_ids = request.POST.getlist('contact_ids[]')  # Assuming contact_ids is a list of contact IDs
        # Delete contacts with the given IDs
        # Example: Contact.objects.filter(id__in=contact_ids).delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})