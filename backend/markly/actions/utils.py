from django.contrib.contenttypes.models import ContentType
from actions.models import Action
from django.utils import timezone


def create_action(user, verb, target=None):
    """Handy shortcut to create action"""
    now = timezone.now()
    last_minute = now - timezone.timedelta(seconds=60)

    similar_action = Action.objects.filter(user__id=user.id,
                                           verb=verb,
                                           created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_action = similar_action.filter(target_ct=target_ct,
                                               target_id=target.id)
    if not similar_action:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
