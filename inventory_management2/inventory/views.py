from rest_framework import viewsets, permissions
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        cache_key = 'products'
        cached_products = cache.get(cache_key)
        if cached_products:
            return cached_products

        products = Product.objects.all()
        cache.set(cache_key, products, timeout=60 * 15)  # Cache for 15 minutes
        return products

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    logger.error(f"Error occurred: {response.data}")
    return response

from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
