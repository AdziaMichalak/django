from django import forms
from posts.models import Author


class PostForm(forms.Form):
    title = forms.CharField(label='Tytuł', required=False)
    content = forms.CharField(label='Treść', widget=forms.Textarea, required=False)
    author_id = forms.ModelChoiceField(label='Wybierz autora', queryset=Author.objects.all(), initial=1, required=False)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        author = cleaned_data.get('author_id')

        if not all([title, content, author]):
            raise forms.ValidationError("Uzupełnij wszystkie wartości!")


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        nick = cleaned_data.get('nick')
        email = cleaned_data.get('email')

        if not (nick and email):
            raise forms.ValidationError("Uzupełnij nick oraz email!")