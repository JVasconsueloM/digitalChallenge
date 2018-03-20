from rest_framework import serializers

from apps.comun.models import Product, Brand, ProductDetails


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializerList(serializers.ListSerializer):
    def update(self, instance, validated_data):
        product_map = {p.id: p for p in instance}
        data_map = {item['id']: item for item in validated_data}

        ret = []
        for product_id, data in data_map.items():
            product = product_map.get(product_id, None)
            if product:
                ret.append(self.child.update(product, data))

        return ret


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = '__all__'
        list_serializer_class = ProductSerializerList


class _ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = '__all__'


class ProductDetailsSerializer(serializers.ModelSerializer):
    details = _ProductDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
