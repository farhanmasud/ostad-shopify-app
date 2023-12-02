from django.contrib import messages
from django.shortcuts import redirect


def show_error_message_and_redirect(request, error_message, redirect_uri):
    messages.error(request, error_message)
    return redirect(redirect_uri)
