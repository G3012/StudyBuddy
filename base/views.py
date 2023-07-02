from django.shortcuts import render, redirect #Importing redirect
from .models import Room,Topic, Message, User #Importing Room,Topic and Message from models to display info regarding rooms.
from .forms import RoomForm,UserForm,MyUserCreationForm #Importing Roomform from forms.py
from django.db.models import Q #This helps to make search engine dynamic i.e, a user can search either by room name or by topic name or by description.
# from django.contrib.auth.models import User #Importing User to check wether the requested user is present in the User database table or not.
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required #importing login_required to restrict some pages to not related users.
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm #importing UserCreationForm for user registration 
#This is a python list of rooms which is to be displayed in home page.
# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend Developers'},
# ]

def loginPage(request):
    #we do this just to differentiate wether request is for login or signup.
    page = 'login'
    #Restricting Login Page from already logged in user.
    if request.user.is_authenticated:
        return redirect('home')
    #When login is requested by any user
    if request.method == 'POST':
        #First stores the entered values
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        #checks with User database table, if present checks wether they are equal or not if equal sets the username to username.If it is not present, throws a Error flash message.
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        #If it is present in User database and is equal, authenticates it. 
        user = authenticate(request, email=email, password=password)
        #If authenticated user gets login and redirects to home page, else throws a Error flash message.
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username/Password does not exists')


    context = {'page': page}
    return render(request, 'base/login_register.html',context);

def logoutUser(request):
    #When logout requested, just logsout and directs it to home page.
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    #When a sign up is requested, checks wether the filled details are valid or not, if valid, user is saved in lowercase and logged in, else throw a error message.
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An Error occured during registration')

    return render(request,'base/login_register.html',{'form': form})

#defined a function by name home on calling which it returns HttpResponse.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' #q is what a user searched and if it is blank q sets to blank string.
    #Accessing filtered objects(rooms) from the Room database table. Filtering happens based on topicname,roomname,roomdesc.__icontains means that it is not necessary to search full name as it automatically takes its best match. 
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ) 
    #Accessing all the objects(topics) from the Topic database table.
    topics = Topic.objects.all()[0:5]
    #Finds the number of rooms
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #Storing the messages filtered by room and topic name searched by the user using the Q function to display these messages in Activity feed.
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context) #We pass context which holds rooms using which we could display them in home page.

def room(request,pk):
    room = Room.objects.get(id=pk) #Here we are getting a single object(room) from any database table by its id which is equal to pk.
    room_messages = room.message_set.all().order_by('-created') #Storing all the existing messages and ordered like recent message at the top.
    participants = room.participants.all() #Storing all the participants.
    #If a new mmessage is posted, we are gonna add the user of message,which room and the message in database table, and then redirect to room page.
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user) #If a user who is not a participant of that room posts a message, make him a participant of that room.
        return redirect('room',pk=room.id)
    #looping over all the rooms and passing the room with id which is same as requested pk.
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room =i;
    context = {'room':room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk) #Storing a paritcular user from User database using pk.
    rooms = user.room_set.all() #Storing all the rooms of which that particular user is a part of.
    room_messages = user.message_set.all() #Storing all the messages which is posted by that particular user. 
    topics = Topic.objects.all() #Storign all the topics.
    context={'user': user,'rooms':rooms, 'topics': topics,'room_messages': room_messages}
    return render(request,'base/profile.html',context)

@login_required(login_url='login') #If not logged in user tries to create room, it just directs to login page.
def createRoom(request):
    form = RoomForm() #It just sets the variable form to the Modelform.
    topics = Topic.objects.all()
    #When creating a room is requested, the inbuilt functions in forms just checks wether the filled details are valid and if valid, saves in the form and redirects to home page.
    if request.method == 'POST':
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            Room.objects.create(
                host = request.user,
                topic = topic,
                name = request.POST.get('name'),
                description = request.POST.get('description'),
            )
            return redirect('home')

    context={'form' : form, 'topics': topics}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #Acessing the already filled form.
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')

    #when update room is requested, checks wether the updated form is valid and if valid,save updated form in forms and redirects to home page.
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context = {'form' : form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    #If delete request is done by a user who is not the host of that room, then throw this kind of response.
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')
    
    #when delete room is requested, it just deletes the room from the database and redirects to home page.
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    #If delete request is done by a user who is not the owner of that message, then throw this kind of response.
    if request.user != message.user:
        return HttpResponse('Your are not allowed here!')
    
    #when delete message is requested, it just deletes the message from the database and redirects to home page.
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request,'base/update-user.html',{'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html',{'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages': room_messages})