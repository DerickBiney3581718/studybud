from .models import Room, Message
from django import forms

class RoomForm(forms.ModelForm):
    
    class Meta:
        model = Room
        fields = ("__all__")
class MessageForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ['body']