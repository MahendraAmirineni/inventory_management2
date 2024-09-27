from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.models import Category, Product


class ProductAPITests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(name="Test Product", category=self.category, quantity=10)

    def test_create_product(self):
        url = reverse('product-list')
        data = {'name': 'New Product', 'category': self.category.id, 'quantity': 20}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
