from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_bulk.generics import ListCreateBulkUpdateAPIView
from apps.comun.models import Product, Brand
from apps.comun.serializers import ProductSerializer, BrandSerializer, ProductDetailsSerializer


class ProductsAPIView(ListCreateBulkUpdateAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super(ProductsAPIView, self).get_queryset()
        return queryset.filter(**self.get_filters())

    def get_filters(self):
        fields = Product.fields()
        filters = {}
        for key, value in self.request.query_params.items():
            if key in fields:
                filters[key] = value
        return filters


class ProductDetailsAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer


class BrandsAPIView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
