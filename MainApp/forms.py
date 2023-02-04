from django import forms
from django.forms import ModelForm
from .models import Post, Profile
##
from django.contrib.auth.models import User


class BlogCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','company','year','offer_type','job_profile','content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'blog_input',
                'name': 'title',
                'placeholder': 'Title (Should be unique)'}),
            
            'company': forms.TextInput(attrs={
                'class': 'blog_input',
                'name': 'company',
                'placeholder': 'Company Name'}),

            'year': forms.NumberInput(attrs={
                'class': 'blog_input',
                'name': 'year',
                'placeholder': 'Year'}),

            'offer_type': forms.Select(attrs={
                'id':'offer_id',
                'class': 'blog_input',
                'name': 'offer_type',
                'placeholder': 'Select Offer Type'}),

            'job_profile': forms.TextInput(attrs={
                'id' : 'job_pro',
                'class': 'blog_input',
                'name': 'job_profile',
                'placeholder': 'Job Profile'}),

            # 'content': forms.TextInput(attrs={
            #     'class': 'blog_input',
            #     'name': 'content',
            #     'placeholder': 'Job Profile'}),
                }

    # To remove the field labels 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
                'bio': forms.Textarea(attrs={
                'rows':4, 'cols':52}),
                'degree': forms.TextInput(attrs={
                    'size':52,
                }),
                'program': forms.TextInput(attrs={
                    'size':52,
                }),
                'graduation': forms.NumberInput(attrs={
                    'size':52,
                }),
                }
