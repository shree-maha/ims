from django.urls import path
from ims_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('shopping_page/', views.shopping_page, name='shopping_page'),
    path('order_page/', views.order_page, name='order_page'),
    path('customer_order_details/', views.customer_order_details, name='customer_order_details'),
    path('ims_product_tracking/', views.ims_product_tracking, name='ims_product_tracking'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



