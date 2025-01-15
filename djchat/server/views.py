from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Category, Server
from .schema import server_list_docs
from .serializer import CategorySerializer, ServerSerializer


# Create your views here.
class ServerMembershipViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, server_id):
        server = get_object_or_404(Server, id=server_id)
        user = request.user

        if server.member.filter(id=user.id).exists():
            return Response({'error': 'User is already a member'}, status=status.HTTP_409_CONFLICT)

        server.member.add(user)

        return Response({'message': 'User joined server successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['DELETE'])
    def remove_member(self, request, server_id):
        server = get_object_or_404(Server, id=server_id)
        user = request.user

        if not server.member.filter(id=user.id).exists():
            return Response({'error': 'User in not a member'}, status=status.HTTP_404_NOT_FOUND)

        if server.owner == user:
            return Response({'error': 'Owners cannot be removed as a member'}, status=status.HTTP_409_CONFLICT)

        server.member.remove(user)

        return Response({'message': 'User removed from server'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def is_member(self, request, server_id=None):
        server = get_object_or_404(Server, id=server_id)
        user = request.user
        is_member = server.member.filter(id=user.id).exists()

        return Response({'is_member': is_member})

class CategoryListViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    # permission_classes = [IsAuthenticated]

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
    # permission_classes = [IsAuthenticated]

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

        if by_server_id:
            # if not request.user.is_authenticated:
                #     raise AuthenticationFailed()

            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(detail=f'Server with id {by_server_id} not found')
            except ValueError:
                raise ValidationError(detail='Incorrect server_id input type')

        if qty:
            self.queryset = self.queryset[:int(qty)]

        serializer = ServerSerializer(self.queryset, many=True, context={'num_members': with_num_members})
        return Response(serializer.data)
