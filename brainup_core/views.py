import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, Q, FilteredRelation

from .API.serializers import CollectionsSerializer
from .models import Card, CardsCollection
from .forms import CardCreationForm, CollectionCreationForm
from rest_framework.renderers import JSONRenderer


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


def learning(request, collection_id, *args):
    if request.user.is_authenticated:
        if request.method == 'GET':
            collection = CardsCollection.objects.get(id=collection_id)
            serialized_collection = CollectionsSerializer(collection).data
            json = JSONRenderer().render(serialized_collection)
            if not collection:
                return redirect('index')
            return render(request, 'cards/learning.html', {'collection_json': json.__str__()[2:][:-1],
                                                           'collection_obj': collection})
    else:
        return redirect('index')


def learn_expired(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            #TODO рефакторинг запроса к базе без пересбора в новый словарь
            raw_collections = CardsCollection.objects.filter(author=request.user)\
                                                     .filter(Q(cards__entry_date__lte=datetime.date.today()-datetime.timedelta(days=0)) | Q(cards__id=None))\
                                                     .values('id', 'title', 'cards')
            expired_cards = {}
            collections = raw_collections.distinct().values('id', 'title')
            number_of_expired = 0
            for collection in raw_collections:
                if collection['id'] in expired_cards:
                    expired_cards[collection['id']].append(collection['cards'])
                else:
                    expired_cards[collection['id']] = [collection['cards']] if collection['cards'] is not None else []
                if collection['cards']: number_of_expired+=1
            print(expired_cards)
            context = {
                'collections': collections,
                'cards': expired_cards,
                'amount_expired': number_of_expired
            }
            return render(request, 'learn_expired.html', context)


#TODO remove if useless
def filter(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            collections = CardsCollection.objects.filter(author=request.user).values('id', 'title')
            context = {
                'collections': collections
            }
            return render(request, 'filter.html', context)
