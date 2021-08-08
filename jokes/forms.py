from django import forms
from .models import Jokes, Generators


class JokeForm(forms.Form):
    generator = forms.ModelChoiceField(
        queryset=Generators.objects.all(),
        label='Генератор',
        empty_label='Выберите генератор',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    max_words = forms.IntegerField(
        min_value=1,
        max_value=1500,
        label='Количество слов',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    start_text = forms.CharField(
        required='',
        max_length=500,
        label='Начать с',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class GeneratorsForm(forms.Form):
    short_name = forms.CharField(
        max_length=50,
        label='Название генератора',
        empty_value='Generator',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        max_length=150,
        label='Описание генератора',
        empty_value='',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    train_file = forms.FileField(
        allow_empty_file=False,
        label='Загрузите файл для обучения',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    num_grams = forms.IntegerField(
        min_value=1,
        max_value=50,
        label='Количество n-грам',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )