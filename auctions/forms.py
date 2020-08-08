from django import forms 
from .models import Category, Listing, Bid, UserComment
  
class ListingForm(forms.ModelForm): 
    class Meta: 
        model = Listing 
        fields = ['title', 'listing_desc', 'cat_id', 'starting_price', 'listing_img']
        labels = {
            'listing_desc': 'Description',
            'cat_id' : 'Category',
            'starting_price' : 'Starting Price',
            'listing_img' : 'Listing Image',   
        }

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'listing_desc' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Description', 'rows':5}),
            'cat_id' : forms.Select(attrs={'class' : 'form-control'}),
            'starting_price' : forms.TextInput(attrs={'class': 'form-control'}),
            # 'listing_img' : forms.ImageField() 
        }


class BidForm(forms.ModelForm): 
    class Meta: 
        model = Bid 
        fields = ['user_bid']

        labels = {'user_bid': ''}

        widgets = {
            'user_bid' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter your Bid Amount', 'default': ''})
            }

class CommentForm(forms.ModelForm):     
    class Meta: 
        model = UserComment 
        fields = ['user_comment']

        labels = {'user_comment': ''}

        widgets = {
            'user_comment' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Enter your comment'}),
            }