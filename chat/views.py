from django.shortcuts import render, redirect
from .models import ChatMessage

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("account_login")
    
    if request.method == 'POST':
        message = request.POST.get('message', '')  # Assuming the message is sent as POST data
        sender = request.user  # Assuming the sender is the authenticated user
        if message:
            # Save the message to the database
            ChatMessage.objects.create(sender=sender, message=message)
    
    # Retrieve all chat messages from the database
    chat_messages = ChatMessage.objects.all()

    context = {'chat_messages': chat_messages}
    return render(request, "chat/chatPage.html", context)
