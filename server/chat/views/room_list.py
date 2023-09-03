import uuid

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render
from chat.models import Conversation


@login_required
def chatroom_delete(request, chatroom_uuid):
    if request.method == "POST":
        try:
            chatroom = Conversation.objects.get(uuid=chatroom_uuid, user=request.user)
            chatroom.delete()
        except Conversation.DoesNotExist:
            pass  # Optionally, you can handle this case as needed.
        # Trigger a reload of the current page
        return redirect(
            request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
        )


@login_required
def chatroom_create(request):
    if request.method == "POST":
        Conversation.objects.create(user=request.user, collection=uuid.uuid4())
        return redirect(
            request.META.get("HTTP_REFERER", "redirect_if_referer_not_found")
        )


@login_required
def chatroom_list(request):
    user = request.user
    sort_by = request.GET.get("sort_by", "-updated_at")

    conversations = (
        Conversation.objects.filter(user=user)
        .annotate(message_count=Count("messages"))
        .order_by(sort_by)
    )

    is_sorted_by_newest = True if sort_by == "-updated_at" else False

    return render(
        request,
        "chat/chatroom_list.html",
        {
            "conversations": conversations,
            "sort_by": sort_by,
            "is_sorted_by_newest": is_sorted_by_newest,
        },
    )
