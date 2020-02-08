from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from app.models import Tag
from recipe.serializers import TagSerializer


class TagViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    """Manage tags from database"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create new tag"""
        serializer.save(user=self.request.user)
