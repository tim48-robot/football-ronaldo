from django.urls import path
from main.views import show_main, show_json, show_xml, show_xml_by_id, show_json_by_id, show_product, create_product, register, login_user, logout_user, edit_product, delete_product, proxy_image, create_product_flutter

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name="login"),
    path('register/',register, name='register'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', delete_product, name='delete_product'),
    path("json/", show_json, name="show_json"),
    path('product/<str:id>/', show_product, name="show_product"),
    path('create-product/', create_product, name="create_product"),
    path("json/<str:product_id>/", show_json_by_id, name="show_json_by_id"),
    path("xml/", show_xml, name="show_xml"),
    path("xml/<str:product_id>/", show_xml_by_id, name="show_xml_by_id"),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
]