from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='main_page'),
    path('generate/', generate, name='generate'),
    path('joke/<int:joke_id>/', view_joke, name='view_joke'),
    path('generate/id_g=<int:generator_id>&max_words=<int:max_words>&start=<str:start>/', view_generated, name='view_generated'),
    path('generate/id_g=<int:generator_id>/save=<str:text>/', save_generated, name='save_generated'),
    path('add_generator/', add_generator, name='add_generator'),
]
