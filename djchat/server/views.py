from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


# Create your views here.
class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get('by_user') == 'true'
        by_server_id = request.query_params.get('by_server_id')
        with_num_members = request.query_params.get('with_num_members') == 'true'

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed(detail='You need to be signed in')

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))

        if qty:
            self.queryset = self.queryset[:int(qty)]

        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=int(by_server_id))
                if not self.queryset.exists():
                    raise ValidationError(detail=f'Server with id {by_server_id} not found')
            except ValueError:
                raise ValidationError(detail='Incorrect server_id input type')

        serializer = ServerSerializer(self.queryset, many=True, context={'num_members': with_num_members})
        return Response(serializer.data)
