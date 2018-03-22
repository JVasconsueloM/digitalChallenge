from django.urls import path

from apps.comun.apis import ProductsAPIView, BrandsAPIView, ProductDetailsAPIView, APIProducts, APIProductDetails
from apps.comun.views import FileUploadView

app_name = 'common'
urlpatterns = [
    # old paths
    path('products/', ProductsAPIView.as_view(), name='products'),
    path('products/<int:id>/', ProductDetailsAPIView.as_view(), name='products'),
    path('brands/', BrandsAPIView.as_view(), name='brands'),

    # new paths
    path('api/products/', APIProducts.as_view(), name='api_products'),
    path('api/products/<int:pk>/', APIProductDetails.as_view(), name='api_product_details'),
    path('api/file/', FileUploadView.as_view(), name='api_file'),

]
