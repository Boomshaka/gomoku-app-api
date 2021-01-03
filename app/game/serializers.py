from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        # fields = ['id', 'title', 'author', 'email']
        fields = '__all__'
