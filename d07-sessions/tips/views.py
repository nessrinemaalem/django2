import random
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Tip
from .forms import TipForm

def homepage(request):
    now = time.time()
    assigned_at = request.session.get('username_assigned_at', 0)
    duration = getattr(settings, 'SESSION_USERNAME_DURATION', 42)

    if not request.session.get('username') or (now - assigned_at) >= duration:
        request.session['username'] = random.choice(settings.ANONYMOUS_USERNAMES)
        request.session['username_assigned_at'] = now

    time_left = max(0, duration - (time.time() - request.session['username_assigned_at']))

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('homepage')
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect('homepage')
    else:
        form = TipForm()

    return render(request, 'tips/homepage.html', {
        'username': request.session['username'],
        'refresh_in': int(time_left) + 1,
        'tips': Tip.objects.all(),
        'form': form,
    })

def upvote(request, tip_id):
    if not request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        tip = get_object_or_404(Tip, id=tip_id)
        user = request.user
        if tip.upvotes.filter(pk=user.pk).exists():
            tip.upvotes.remove(user)
        else:
            tip.downvotes.remove(user)
            tip.upvotes.add(user)
    return redirect('homepage')

def downvote(request, tip_id):
    if not request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        tip = get_object_or_404(Tip, id=tip_id)
        user = request.user
        if tip.downvotes.filter(pk=user.pk).exists():
            tip.downvotes.remove(user)
        else:
            tip.upvotes.remove(user)
            tip.downvotes.add(user)
    return redirect('homepage')

def delete_tip(request, tip_id):
    if not request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        tip = get_object_or_404(Tip, id=tip_id)
        tip.delete()
    return redirect('homepage')

def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'tips/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'tips/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')
