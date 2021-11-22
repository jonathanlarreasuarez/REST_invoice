# Django REST Framework
from rest_framework import serializers

# Model
from api.models import Invoice, Customer, Item, Sku, Brand, Category


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SkuSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()

    class Meta:
        model = Sku
        fields = ('brand', 'category', 'reference', 'name', 'price')


class ItemSerializer(serializers.ModelSerializer):
    sku = SkuSerializer()

    class Meta:
        model = Item
        fields = ['sku', 'gross', 'discounts', 'subtotal', 'tax', 'total']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('document_type', 'document_number', 'first_name', 'last_name', 'phone', 'address', 'email')


class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False, read_only=False)
    items = ItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['createtime', 'document_number', 'customer', 'items']


