from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from ..models import Card, CardsCollection
from rest_framework import generics, permissions
from .serializers import CollectionsSerializer, CardsSerializer
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


class CardsList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardsSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardsSerializer
    permission_classes = [permissions.IsAuthenticated]
