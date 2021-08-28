from rest_framework import serializers
from ..models import CardsCollection, Card


class CardsListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Card
        fields = '__all__'


class CollectionsSerializer(serializers.ModelSerializer):
    cards = CardsListSerializer(many=True, required=False)

    def create(self, validated_data):
        cards_data = validated_data.pop('cards', [])
        collection = CardsCollection.objects.create(**validated_data)
        for card in cards_data:
            Card.objects.create(collection=collection, **card)
        return collection

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        cards = validated_data.get('cards')
        for card in cards:
            card_id = card.get('id', None)
            if card_id:
                inv_card = Card.objects.get(id=card_id, collection=instance)
                inv_card.front_side = card.get('front_side', inv_card.front_side)
                inv_card.back_side = card.get('back_side', inv_card.back_side)
                inv_card.knowledge = card.get('knowledge', inv_card.knowledge)
                inv_card.entry_date = card.get('entry_date', inv_card.entry_date)
                inv_card.save()
            else:
                Card.objects.create(collection=instance, **card)
        return instance

    class Meta:
        model = CardsCollection
        fields = '__all__'
        read_only_fields = [
            'id',
            'author',
            'creation_date'
        ]


class CardsListEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ['id', 'creation_date']

    def update(self, instance, validated_data):
        pass
