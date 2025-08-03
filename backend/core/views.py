from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone

from .models import ChatMessage, OAuthCredential
from .integration_registry import searchIntegrationFunction, callIntegrationFunction
from .oauth import get_flow, get_credentials_from_code, get_user_info

import openai, json, datetime

openai.api_key = settings.OPENAI_API_KEY


# ----------------------------
# Authentication Views
# ----------------------------

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect('login')
        return JsonResponse({'error': 'User already exists'})
    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('chat_page')
        return JsonResponse({'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------------
# Chat Views
# ----------------------------

@login_required
def chat_page(request):
    has_google = OAuthCredential.objects.filter(user=request.user).exists()
    return render(request, 'chat.html', {'has_google': has_google})

import openai
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_API_BASE")
)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def chat_api(request):
    try:
        data = json.loads(request.body)
        user_input = data.get('message')

        tools = searchIntegrationFunction(user_input)

        response = client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL", "gpt-3.5-turbo"),
            messages=[
                {"role": "system", "content": "You are an AI assistant with access to Google integrations."},
                {"role": "user", "content": user_input}
            ],
            tools=tools,
            tool_choice="auto"
        )

        answer = response.choices[0].message.content or "[No reply]"
        ChatMessage.objects.create(user=request.user, message=user_input, response=answer)

        return JsonResponse({'response': answer})

    except Exception as e:
        return JsonResponse({'error': f'Exception: {str(e)}'}, status=500)




# ----------------------------
# Google OAuth Views (Unified)
# ----------------------------

# @login_required
def google_auth_start(request):
    flow = get_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    request.session['oauth_state'] = state
    return redirect(auth_url)


# @login_required
from django.contrib.auth import login

def google_auth_callback(request):
    state = request.session.get('oauth_state')
    flow = get_flow(state=state)
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    user_info = get_user_info(credentials)

    # Get or create the user
    user, _ = User.objects.get_or_create(username=user_info["email"])

    # ✅ Log the user in
    login(request, user)

    # Save credentials in DB
    OAuthCredential.objects.update_or_create(
    user=user,
    provider='google',
    defaults={
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_expiry': credentials.expiry,  # ✅ Fix: use directly
    }
)

    return redirect('chat_page')

from django.core.exceptions import ObjectDoesNotExist
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


@login_required
def get_calendar_events(request):
    try:
        creds = OAuthCredential.objects.get(user=request.user)
    except ObjectDoesNotExist:
        print("[OAuth Error] No credentials found for user:", request.user)
        return JsonResponse({'error': 'Google account not linked. Please log in via Google OAuth.'}, status=400)

    try:
        service = build('calendar', 'v3', credentials=creds.to_credentials())

        events_result = service.events().list(
            calendarId='primary',
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return JsonResponse({"events": events})

    except HttpError as e:
        print("[Google API Error]", e)
        return JsonResponse({'error': f'Google API error: {e}'}, status=500)

    except Exception as e:
        print("[Unexpected Error]", e)
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)