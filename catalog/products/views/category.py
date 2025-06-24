from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from ..models import Category
from ..serializers import CategorySerializer

class CaregoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer