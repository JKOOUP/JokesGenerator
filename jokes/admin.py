from django.contrib import admin
from .models import Jokes, Generators


class JokesAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_short_text', 'date', 'generator')
    list_display_links = ('id', 'get_short_text')

    @admin.display(description='Сокращенный текст')
    def get_short_text(self, obj):
        cnt = min(3, len(obj.text.split()))
        sample_text = ' '.join(obj.text.split()[:cnt])
        return sample_text + '...'


class GeneratorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_generator_name', 'dataset_size', 'num_grams', 'date')
    list_display_links = ('id', 'get_generator_name')

    @admin.display(description='Генератор')
    def get_generator_name(self, obj):
        return f'Generator_{obj.dataset_size}_{obj.num_grams}'


admin.site.register(Jokes, JokesAdmin)
admin.site.register(Generators, GeneratorsAdmin)