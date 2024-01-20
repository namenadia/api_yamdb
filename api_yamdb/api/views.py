from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
# from .permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
#   permission_classes = [IsAdminOrReadOnly,]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('categories__slug', 'geners__slug', 'name', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']
#   permission_classes = [IsAdminOrReadOnly,]


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
