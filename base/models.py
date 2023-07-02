from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User #Django has a inbuilt usermodel, so we are importing it.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

#Creating a database table by name "Topic" which contains only name of the topic and returns the name.
class Topic(models.Model):
    
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#Creating a database table by name "Room", returns name of the room.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) #A host can host many rooms but a room can have only one host, which is of the type User model, ans on deleting the host the room wont gets deleted.
    topic =  models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #A topic can have many rooms but a room can have only one topic,which is one of Topic database table, and on deleting any topic, the room wont gets deleted.
    name = models.CharField(max_length = 200)#Name of a room.
    description = models.TextField(null=True, blank=True)#Description of a room, to keep it optional, we set null and blank as true.
    participants = models.ManyToManyField(User, related_name='participants', blank=True) #This is a many to many relationship database which means one user can message in many rooms and one room can have many users messages.
    updated = models.DateTimeField(auto_now=True)#To show the updated time every time we update something in the room.
    created = models.DateTimeField(auto_now_add=True)#To show the created date and time of the room, it gets updated only once it is created.

    class Meta:
        ordering = ['-updated', 'created'] #ordering the rooms like showing the recent created room at the top.

    def __str__(self):
        return self.name

#Creating a database table by name "Message", returns the body of the message of max 50 length. 
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)#A user can send many messages but a message can be sent by only one user, which is of the type User model, and on deleting any user, the messages of that user gets deleted.
    room =  models.ForeignKey(Room, on_delete=models.CASCADE)#A room can have many messages but a message can be of only one room, which is one of Room database table, and on deleting any room, the messages of that room gets deleted.
    body = models.TextField()#Content od message.
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']
        
    def __str__(self):
        return self.body[0:50]