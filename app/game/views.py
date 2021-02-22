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

    def post(self, request, pk):
        game = self.get_object(pk)
        row = request.data.get('row')
        col = request.data.get('col')
        skip_AI = (
            True if 'skip_AI' in request.data and
            request.data['skip_AI'] else False
        )

        if game.status == 'Finished':
            message = {
                'type': 'Finished',
                'detail': 'Game has finished'
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            grid = game.make_move(row, col)
        except ValueError as e:
            message = {
                'type': 'ValueError',
                'detail': str(e)
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except IndexError as e:
            message = {
                'type': 'IndexError',
                'detail': str(e)
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        winner = game.check_winner()

        row_resp, col_resp = -1, -1
        if not skip_AI and winner == 0:
            grid, row_resp, col_resp = game.make_AI_move()
            winner = game.check_winner()
        game_status = 'Playing' if winner == 0 else 'Finished'

        serializer = GameSerializer(
            game,
            data={
                'resp_row': row_resp,
                'resp_col': col_resp,
                'grid': grid,
                'status': game_status,
                'winner': winner
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
