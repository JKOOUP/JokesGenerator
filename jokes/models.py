from django.db import models


class Jokes(models.Model):
    text = models.TextField(blank=True, verbose_name='Текст юморески')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата генерации')
    generator = models.ForeignKey('Generators', on_delete=models.SET_NULL, null=True, verbose_name='Генератор')

    def __str__(self):
        cnt = min(3, len(self.text.split()))
        sample_text = ' '.join(self.text.split()[:cnt])
        return sample_text + '...'

    class Meta:
        verbose_name = 'Юмореска'
        verbose_name_plural = 'Юморески'


class Generators(models.Model):
    short_name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=150, verbose_name='Описание модели', default='')
    file = models.FileField(upload_to='./jokes/GeneratorModule/pretrained/', verbose_name='Файл генератора')
    dataset_size = models.IntegerField(verbose_name='Размер датасета')
    num_grams = models.IntegerField(default=2, verbose_name='Размер n-грам')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Генератор'
        verbose_name_plural = 'Генераторы'
