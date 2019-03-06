from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) # This type of field is rendered as an <input type="text"> HTML element
# Each field type has a default widget that
#determines how the field is rendered in HTML. The default widget
#can be overridden with the widget attribute
 #In the comments field, we
#use a Textarea widget to display it as a <textarea> HTML element
#instead of the default <input> element.   
    
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment              # which model to use to build the form (Comment)
        fields = ('name', 'email', 'body') # By default, Django builds a form field for each field
#contained in the model. However, you can explicitly tell the
#framework which fields you want to include in your form using a
#fields list or define which fields you want to exclude using an exclude
#list of fields
        
# =============================================================================
#  Search view       
# =============================================================================
class SearchForm(forms.Form):
    query = forms.CharField()