from django.contrib import admin

from.models import Room, Topic, Message, User #Importing all the database tables from models.
#Registering the models created in the admin-panel.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)