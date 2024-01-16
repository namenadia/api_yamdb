from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets

from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    '''permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )'''

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )
