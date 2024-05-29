from api.chat.models import Chat, Message

# * -------------------------- CONVERSATIONS -----------------------------


def get_receiver(current_profile, chat):
    receiver = chat.user_set.exclude(id=current_profile.id)
    return receiver[0]


def get_conversation_between(p1, p2):
    chat = Chat.objects.filter(user_set=p1).filter(user_set=p2)
    if chat.exists():
        return chat.first()
    else:
        return None


def get_last_message(chat):
    messages = Message.objects.filter(chat=chat).order_by("-created")
    if messages.exists():
        return messages.first()
    else:
        return None
