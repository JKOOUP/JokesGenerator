from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Jokes, Generators
from .GeneratorModule.NgramGenerator import NgramGenerator
from .GeneratorModule.Tokenizer import Tokenizer
from .forms import JokeForm, GeneratorsForm


def index(request: HttpRequest) -> HttpResponse:
    jokes = Jokes.objects.order_by('-date')
    jokes_with_generators = [(joke, joke.generator) for joke in jokes]

    context = {
        'jokes_wg': jokes_with_generators
    }
    return render(request, 'jokes/index.html', context)


def generate(request: HttpRequest) -> HttpResponse:
    joke_text = ''
    if request.method == 'POST':
        form = JokeForm(request.POST)
        if form.is_valid():
            id_g = form.cleaned_data['generator'].id
            max_words = form.cleaned_data['max_words']
            start = form.cleaned_data['start_text']
            if start == '':
                start = 'None'
            return redirect(f'/generate/id_g={id_g}&max_words={max_words}&start={start}')
    else:
        form = JokeForm()

    context = {
        'text': joke_text,
        'form': form,
    }

    return render(request, 'jokes/generate.html', context)


def view_joke(request: HttpRequest, joke_id: int) -> HttpResponse:
    joke_obj = get_object_or_404(Jokes, pk=joke_id)
    context = {
        'joke': joke_obj,
        'generator': Generators.objects.get(id=joke_obj.generator_id),
    }
    return render(request, 'jokes/view_joke.html', context)


def view_generated(request: HttpRequest, generator_id: int, max_words: int, start: str) -> HttpResponse:
    generator_db_obj = Generators.objects.get(id=generator_id)

    tokenizer = Tokenizer(pretrained=True, file_path='./jokes/GeneratorModule/pretrained/tokenizer37k.pkl')
    generator = NgramGenerator(num_grams=generator_db_obj.num_grams, tokenizer=tokenizer)
    generator.load(file_path=str(generator_db_obj.file))

    if start == 'None':
        joke_text = generator.generate(max_words)
    else:
        joke_text = generator.generate(max_words, start)

    context = {
        'text': joke_text,
        'generator_id': generator_id,
        'max_words': max_words,
        'start': start,
    }

    return render(request, 'jokes/view_generated.html', context)


def save_generated(request: HttpRequest, generator_id: int, text: str) -> HttpResponse:
    joke = Jokes(generator_id=generator_id, text=text)
    joke.save()
    return redirect(f'/joke/{joke.id}')


def add_generator(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        generator_form = GeneratorsForm(request.POST, request.FILES)
        if generator_form.is_valid():
            file = request.FILES['train_file']
            num_grams = generator_form.cleaned_data['num_grams']
            short_name = generator_form.cleaned_data['short_name']
            description = generator_form.cleaned_data['description']

            text = file.read().decode('utf-8')
            trainset_size = len(text.split('<eoa>'))

            tokenizer = Tokenizer(pretrained=True, file_path='./jokes/GeneratorModule/pretrained/tokenizer37k_new.pkl')
            generator = NgramGenerator(num_grams, tokenizer)
            generator.train(text=text)

            generator_file_path = f'./jokes/GeneratorModule/pretrained/generator_{trainset_size}_{num_grams}'
            generator.save(generator_file_path)

            generator_db_obj = Generators(
                short_name=short_name,
                description=description,
                file=generator_file_path + '.pkl',
                dataset_size=trainset_size,
                num_grams=num_grams,
            )

            generator_db_obj.save()
            return redirect('/add_generator')
    else:
        generator_form = GeneratorsForm()

    context = {
        'form': generator_form,
    }
    return render(request, 'jokes/add_generator.html', context)
