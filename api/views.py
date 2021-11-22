from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Invoice, Customer, Item, Sku, Brand, Category
from rest_framework import viewsets, status
from rest_framework import permissions
from api.serializers import InvoiceSerializer, CustomerSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('createtime')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, validated_data):
        items_data = validated_data.data.pop('items')
        customer_data = validated_data.data.pop('customer', None)
        if customer_data:
            customer = Customer.objects.create(**customer_data)
            validated_data.data['customer'] = customer

        invoice = Invoice.objects.create(**validated_data.data)
        for item_data in items_data:
            sku_data = item_data.pop('sku')
            brand_data = sku_data.pop('brand')
            brand = Brand.objects.create(**brand_data)
            category_data = sku_data.pop('category')
            category = Category.objects.create(**category_data)
            sku = Sku.objects.create(brand=brand, category=category, **sku_data)
            item = Item.objects.create(invoice=invoice, **item_data, sku=sku)
            # item = Item.objects.create(**item_data, sku=sku)
            invoice.items.add(item)

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, validated_data, pk=None):
        # def update(self, instance, validated_data, pk=None):
        items_data = validated_data.data.pop('items')
        # instance = super().update(instance, validated_data)  # if you want to update other fields

        if pk is not None:
            invoice = Invoice.objects.get(id=pk)
            invoice.createtime = validated_data.data['createtime']
            invoice.document_number = validated_data.data['document_number']
            invoice.save()
            for item_data in items_data:
                sku_data = item_data.pop('sku')
                # Brand Model
                brand_data = sku_data.pop('brand')
                brand = Brand.objects.get(id=brand_data['id'])
                brand.name = brand_data['name']
                brand.save()
                # Category Model
                category_data = sku_data.pop('category')
                category = Category.objects.get(id=category_data['id'])
                category.name = category_data['name']
                category.save()
                sku = Sku.objects.update(brand=brand, category=category, **sku_data)
                item = Item.objects.update(invoice=invoice, **item_data, sku=sku)
                invoice.items.add(item)


            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_404_NOT_FOUND)
