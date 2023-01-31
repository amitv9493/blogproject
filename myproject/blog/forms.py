from django import forms 
from .models import Comment
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=False)
    email = forms.EmailField( required=True)
    to = forms.EmailField( required=True)
    comments = forms.CharField(widget = forms.Textarea ,required=False)
    
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
