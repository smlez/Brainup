import datetime

from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    front_side = models.TextField()
    back_side = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    entry_date = models.DateField(default=datetime.date.today())
    KNOWLEDGE_GRADE = [
        ('1', 'Hard'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ]
    knowledge = models.CharField(
        max_length=1,
        choices=KNOWLEDGE_GRADE,
        default='1'
    )
    collection = models.ForeignKey('CardsCollection', on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return f'front: {self.front_side}\nback:{self.back_side}'


class CardsCollection(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'title: {self.title}'
