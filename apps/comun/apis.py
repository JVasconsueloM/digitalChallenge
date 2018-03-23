from django.contrib.auth import authenticate
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework_bulk.generics import ListCreateBulkUpdateAPIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from apps.comun.models import Product, Brand, ProductDetails
from apps.comun.serializers import ProductSerializer, BrandSerializer, ProductDetailsSerializer
from apps.comun.utils import paginate, valid_filters, exception_response, model_setattr, ValidationError


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
        queryset = queryset.filter(**self.filter())
        # queryset.count () - esto realizará  un SELECT COUNT(*) some_table
        # len(queryset) - esto realizará un SELECT * FROM some_table
        queryset_count = queryset.count()

        data = paginate(self.request, queryset, queryset_count)
        return data

    def filter(self):
        # esta funcion valida solo la busqueda por los atributos disponibles en el modelo
        vf = valid_filters(Product)
        pdf = valid_filters(ProductDetails)
        f = {}
        for key, value in self.request.query_params.items():
            if key in vf:
                f[key] = value

            if key in pdf:
                f['details__%s' % (key)] = value

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


class APIAuthentication(APIView):
    authentication_classes = ()
    permission_classes = ()

    @exception_response
    def post(self, *args, **kwargs):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        email = self.request.data.get('email')
        sing_up = self.request.data.get('sign_up')

        if not username or not password:
            raise ValidationError('username or password not provided.')

        if sing_up:
            user = User.objects.create_user(
                username=username,
                password=password,
                is_active=True,
                email=email
            )
        else:
            user = authenticate(username=username, password=password)

        if not user:
            return Response({"details": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)
