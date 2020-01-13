import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from remindmoi_bot.models import Reminder


@csrf_exempt
@require_POST
def add_reminder(request):
    # TODO: make it safer.
    # Add CSRF validation
    # Sanitize/validate post data
    reminder_obj = json.loads(request.body)
    reminder = Reminder(**reminder_obj)
    reminder.save()
    return JsonResponse({'success': True})
