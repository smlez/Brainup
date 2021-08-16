import datetime

from django.core.cache import cache
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.renderers import JSONRenderer

from .API.serializers import CollectionsSerializer
from .forms import CardCreationForm, CollectionCreationForm
from .models import Card, CardsCollection


def index(request):
    if request.user.is_authenticated:
        collections = CardsCollection.objects.filter(author=request.user)
        context = {
            'collections': collections,
            'user': request.user
        }
        return render(request, 'index.html', context)
    else:
        return redirect('user_manager:sign_in')


def card(request, card_id):
    if request.user.is_authenticated:
        context = {
            'front': Card.front_side,
            'back': Card.back_side
        }
        print("context")
        return render(request, 'card.html', context)
    else:
        return redirect('index')


def collection(request, collection_id):
    if request.user.is_authenticated:
        try:
            collection = CardsCollection.objects.filter(author=request.user).get(id=collection_id)
        except:
            collection = None

        context = {
            'collection': collection
        }
        return render(request, 'cards/collection.html', context)
    else:
        return redirect('index')


def card_creation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CardCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('index'))
        else:
            form = CardCreationForm()
            form.fields['collection'].queryset = CardsCollection.objects.filter(author=request.user)
        return render(request, 'cards/base_creation_form.html', {'form': form})
    else:
        return redirect('index')


def collection_creation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CollectionCreationForm(request.POST)
            if form.is_valid():
                collection = form.save(commit=False)
                collection.author = request.user
                collection.save()
                return redirect('index')
        else:
            form = CollectionCreationForm()
        return render(request, 'cards/base_creation_form.html', {'form': form})
    else:
        return redirect('index')


def learning(request, collection_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            collection = list(CardsCollection.objects\
                              .filter(id=collection_id)\
                              .values('cards__id', 'cards__front_side', 'cards__back_side', 'cards__entry_date', 'cards__knowledge'))
            if not collection:
                return redirect('index')
            test_colls = collection
            for card in test_colls:
                card['cards__entry_date'] = card['cards__entry_date'].isoformat()
            return render(request, 'cards/learning.html', {'collection': collection})
    else:
        return HttpResponse('User is not authenticated!')


def show_expired(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # TODO проверка оптимизированности запроса и их кол-ва
            full_collections = CardsCollection.objects.filter(author=request.user) \
                .filter(
                Q(cards__entry_date__lte=datetime.date.today() - datetime.timedelta(days=0))) \
                .values('id', 'title', 'cards__id', 'cards__front_side', 'cards__back_side', 'cards__entry_date', 'cards__knowledge')
            amount_expired = {}
            expired_collections = list(full_collections.distinct().values('id', 'title').annotate(Count('cards__id')))
            cache.add(str(request.user.id), full_collections, 240)
            context = {
                'collections': expired_collections
            }
            return render(request, 'show_expired.html', context)


def learn_expired(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            id = int(request.GET['id'])
            collections = cache.get(str(request.user.id))
            print('cards: ', collections)
            # for collection in collections:
            context = {

            }
            return render(request, 'learning.html', context)
    else:
        return HttpResponse('User is not authenticated!')
