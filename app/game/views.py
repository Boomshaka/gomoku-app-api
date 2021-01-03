from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404

from game.models import Game
from game.serializers import GameSerializer


class GameAPIView(APIView):

    def get(self, request):
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        # print("REQUESTED DATA IS:\n\n\n\n", request.data, '\n\n\n\n\n')
        if serializer.is_valid():
            serializer.save()
            # print("Data to BE Returned", serializer.data, '\n\n\n')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameDetails(APIView):

    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        game = self.get_object(pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)
