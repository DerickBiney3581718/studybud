from django.shortcuts import render, redirect   
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, User, Message
from .forms import RoomForm, MessageForm
# Create your views here.


# rooms = [
#     {'id': 1, 'name': "Let's learn python!"},
#     {'id': 2, 'name': "Design with me!"},
#     {'id': 3, 'name': "for frontend devs!"}

# ]
def home(request):
    q = request.GET.get('q')
    if q:
        rooms_by_topic = Q(topic__name__icontains= q)
        rooms_by_name = Q(name__icontains= q)
        rooms_by_host = Q(host__username__icontains= q)
        rooms_by_description = Q(description__icontains = q)
        query = rooms_by_host | rooms_by_name | rooms_by_topic | rooms_by_description
        rooms = Room.objects.filter(query)
        
    else:
    #     if q:
        rooms = Room.objects.all()


    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics}
    return render(request, "base/home.html", context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user =   User.objects.get(username= username)
        except:
            messages.error(request, "No user found")
        user = authenticate(request, username= username, password = password)
        if user:
            login(request, user)
            return redirect('home')
    context = {'login': True}
    return render(request, 'base/login_register.html', context)
    
def logout_page(request):
    logout(request)
    return redirect('login')

def register_page(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save(commit=False)
            user.username = user.username.lower()
            f.save()
            login(request, user)
            return redirect('home')
    context = {'page': page}
    return redirect(request, 'base/login_register.html', context)


def room(request, pk):
    room = Room.objects.get(pk=pk)
    participants = room.participants.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            o = form.save(commit=False)
            o.user = request.user
            o.room = room
            o.body = request.POST.get('body')
            o.save()
            return redirect('room', pk = room.id)
    messages = room.message_set.all().order_by('created')
    context = {"room": room, 'room_messages':messages, 'participants':participants}    
    return render(request, "base/room.html", context)

@login_required(login_url='login')
def create_room(request):
    if request.method == 'POST':
        new_form = RoomForm(request.POST)
        if new_form.is_valid():
            # host = request.user.id
            # new_form.host = host
            new_form.save()
            return redirect('home')
    new_form = RoomForm()
    return render(request, "base/room_form.html", {'form': new_form})

def update_room(request, pk):
    room = Room.objects.get(pk = pk)
    if request.method == "POST":
        f = RoomForm(instance=room, data= request.POST)
        if f.is_valid():
            f.save()
        return redirect('home')
    f = RoomForm(instance=room)
    return render(request, "base/room_form.html", {'form': f})

def delete_room(request, pk):
    room = Room.objects.get(pk = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_form.html', {'obj': room})