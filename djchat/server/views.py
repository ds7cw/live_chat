from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response

from .models import Server
from .serializer import ServerSerializer


# Create your views here.
class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        by_server_id = request.query_params.get('by_server_id') == 'true'

        if by_user and not request.user.is_authenticated:
            raise AuthenticationFailed(detail='You need to be signed in')

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if qty:
            self.queryset = self.queryset[:int(qty)]

        if by_server_id:
            try:
                server_id = int(request.query_params.get('server_id'))
                self.queryset = self.queryset.filter(id=server_id)
                if not self.queryset:
                    raise ValidationError(detail=f'Server with id {server_id} not found')
            except ValueError:
                raise ValidationError(detail='Incorrect server_id input type')

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
