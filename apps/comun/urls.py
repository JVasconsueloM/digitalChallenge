from django.urls import path

from apps.comun.apis import ProductsAPIView, BrandsAPIView, ProductDetailsAPIView

app_name = 'common'
urlpatterns = [
    path('products/', ProductsAPIView.as_view(), name='products'),
    path('products/<int:id>/', ProductDetailsAPIView.as_view(), name='products'),
    path('brands/', BrandsAPIView.as_view(), name='brands'),
]
