from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from libapi.models import Book
from libapi.serializers import BookSerializer
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST

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

class BookModelViewSet(ModelViewSet):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer

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
