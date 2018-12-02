from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, HyperlinkedRelatedField
from libapi.models import Book, PublicationHouse

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'pages')

class PublicationHouseSerializer(ModelSerializer):
    # books = PrimaryKeyRelatedField(many=True, read_only=True)
    # books = HyperlinkedRelatedField(many=True, read_only=True,view_name='book-detail')
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = PublicationHouse
        fields = ('id','name','ratings','books')
