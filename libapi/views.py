from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from libapi.models import Book, PublicationHouse
from libapi.serializers import BookSerializer, PublicationHouseSerializer
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid username or password"}, status=HTTP_400_BAD_REQUEST)

class PublicationHousesList(ListAPIView):
    # queryset = PublicationHouse.objects.all()
    serializer_class = PublicationHouseSerializer

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, request):
        print('Get called')
        house = PublicationHouse.objects.get(pk=1)
        ser_house = PublicationHouseSerializer(house)
        return Response(ser_house.data)

class BookModelViewSet(ModelViewSet):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        price = self.request.query_params.get('price')
        pages = self.request.query_params.get('pages')
        print(price)
        print(pages)

        q1, q2 = None, None
        if price:
            q1 = Q(price=price)
        if pages:
            q2 = Q(pages=pages)

        if q1 and q2:
            finalq = q1 & q2
        elif q1:
            finalq = q1
        elif q2:
            finalq = q2
        else:
            finalq = None

        if finalq:
            return Book.objects.filter(finalq)
        return Book.objects.all()

class BookListView(ListCreateAPIView):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        price = self.request.query_params.get('price')
        pages = self.request.query_params.get('pages')

        q1, q2 = None, None
        if price:
            q1 = Q(price=price)
        if pages:
            q2 = Q(pages=pages)

        if q1 and q2:
            finalq = q1 & q2
        elif q1:
            finalq = q1
        elif q2:
            finalq = q2
        else:
            finalq = None

        if finalq:
            return Book.objects.filter(finalq)
        return Book.objects.all()

class GetBookView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
