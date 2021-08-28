from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from ..models import Card, CardsCollection
from rest_framework import generics, permissions, mixins
from .serializers import CollectionsSerializer, CardsListSerializer, CardsListEditSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cards': reverse('brainup_api:cards_list', request=request, format=format),
        'collections': reverse('brainup_api:collections_list', request=request, format=format)
    })


class CollectionsList(generics.ListCreateAPIView):
    queryset = CardsCollection.objects.all()
    serializer_class = CollectionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CardsCollection.objects.all()
    serializer_class = CollectionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class CardsList(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardsListSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardsListEdit(APIView):

    def get_queryset(self):
        return Card.objects.filter()

    def get(self, request):
        available_collections = CardsCollection.objects.filter(author=request.user).values('id')
        return Response(self.get_queryset()
                            .filter(collection__in=available_collections)
                            .values('id', 'front_side', 'back_side', 'creation_date', 'entry_date', 'knowledge'))

    def put(self, request):
        data = request.data
        colls_ids = CardsCollection.objects.filter(author=request.user).values('id')
        cards = self.get_queryset().filter(collection__in=colls_ids)
        prepared_cards = QuerySet()
        try:
            for card in data:
                try:
                    current_card = cards.get(id=card['id'])
                except:
                    raise Exception('Some card with given id not found')
                for field in card:
                    if field != 'id':
                        setattr(current_card, field, card[field])
                current_card.save()
        except:
            raise Exception('Something went wrong with saving given cards')
        return Response('Cards saved!')


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardsListSerializer
    permission_classes = [permissions.IsAuthenticated]
