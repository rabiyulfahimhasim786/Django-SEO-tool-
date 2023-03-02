from django import forms
from .models import textarticle, Keyword, Genre, Film

class articleForm(forms.ModelForm):
    class Meta:
        model = textarticle
        fields = ('url',)

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('Keywords', )

class Genreform(forms.ModelForm):
    class Meta:
        model=Genre
        fields="__all__"

class Filmform(forms.ModelForm):
    class Meta:
        model=Film
        fields="__all__"

