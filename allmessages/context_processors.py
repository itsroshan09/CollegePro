# context_processors.py
from .models import allmessages

def unread_messages_count(request):
    unread_count = allmessages.objects.filter(read=False).count()
    return {'unread_count': unread_count}
