from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
	content = models.TextField()
	time = models.DateTimeField(auto_now_add=True)