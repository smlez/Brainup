from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

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


def learning(request, collection_id):
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
