from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework_bulk.generics import ListCreateBulkUpdateAPIView

from apps.comun.models import Product, Brand
from apps.comun.serializers import ProductSerializer, BrandSerializer, ProductDetailsSerializer
from apps.comun.utils import paginate, valid_filters, exception_response, model_setattr


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


class APIProducts(APIView):
    @exception_response
    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        return Response(data, status=status.HTTP_200_OK)

    @exception_response
    def post(self, request, *args, **kwargs):
        data = self.request.data
        product = Product.objects.create(**data)
        return Response(product.to_dict(False), status=status.HTTP_201_CREATED)

    @exception_response
    def put(self, request, *args, **kwargs):
        data = self.bulk_update()
        return Response(data, status=status.HTTP_200_OK)

    def get_queryset(self):
        # se obtienen todos los objetos
        queryset = Product.objects.filter()
        # queryset.count () - esto realizará  un SELECT COUNT(*) some_table
        # len(queryset) - esto realizará un SELECT * FROM some_table
        queryset_count = queryset.count()

        queryset = queryset.filter(**self.filter())

        data = paginate(self.request, queryset, queryset_count)
        return data

    def filter(self):
        # esta funcion valida solo la busqueda por los atributos disponibles en el modelo
        vf = valid_filters(Product)
        f = {}
        for key, value in self.request.query_params.items():
            if key in vf:
                f[key] = value
        return f

    @atomic
    def bulk_update(self):
        data = self.request.data
        # comprobamos si es una lista
        if not isinstance(data, list):
            raise TypeError('Se esperaba una lista de elementos.')

        # creamos un diccionario con la data enviada en caso de no existir el campo id saldra un error
        # obtenemos solo los productos en base a los ids registrados
        data_map = {item['id']: item for item in data}
        queryset = Product.objects.filter(id__in=data_map.keys())
        queryset_map = {item.id: item for item in queryset}

        # aca podemos validarlos ids de dos formas o realizamos como se ah puesto actualmente o evaluamos la condicion
        # queryset.values_list('id', flat=True) y recorrer esa lista verificando con data_map.keys() cuales son los ids
        # no existentes

        for id, data in data_map.items():
            product = queryset_map.get(id, None)
            if not product:
                raise Product.DoesNotExist('no se encontro el producto(id=%s)' % id)

            model_setattr(product, data)
            product.save()

        return queryset.values()


class APIProductDetails(APIView):
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        return super(APIProductDetails, self).dispatch(request, *args, **kwargs)

    @exception_response
    def get(self, *args, **kwargs):
        self.get_object()
        data = self.object.to_dict()
        return Response(data, status=status.HTTP_200_OK)

    @exception_response
    def put(self, *args, **kwargs):
        return self.put_or_patch(*args, **kwargs)

    @exception_response
    def patch(self, *args, **kwargs):
        return self.put_or_patch(*args, **kwargs)

    @exception_response
    def delete(self, *args, **kwargs):
        self.get_object()
        self.object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        self.object = get_object_or_404(Product, id=self.pk)

    def put_or_patch(self, *args, **kwargs):
        # update function, first getting object
        self.get_object()
        # podriamos realizar la actualización con un
        # Product.object.filter(id=self.pk).update(**self.request.data)
        # pero reutilizaremos la funcion get_object para generar un error 404 en caso de no encontrar el objeto
        # y para no generar otro queryset  realizamos lo siguiente
        model_setattr(self.object, self.request.data)
        self.object.save()
        return Response(self.object.to_dict(), status=status.HTTP_200_OK)
