from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from app.models import Tag
from recipe.serializers import TagSerializer


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags from database"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)
