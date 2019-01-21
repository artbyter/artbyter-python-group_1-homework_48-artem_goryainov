from django.urls import path
from webapp.views import FoodDetailView, OrderDetailView, OrderCreateView, FoodCreateView, OrderUpdateView, \
    OrderFoodCreateView, FoodUpdateView, FoodDeleteView, OrderFoodDeleteView, OrdersListView, FoodListView, \
    OrderCourierUpdateView, OrdersCourierListView, InitialView, OrderFoodAjaxCreateView,OrderFoodAjaxUpdateView

app_name = 'webapp'

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders_list'),
    path('login/', InitialView.as_view(), name='initial_view'),
    path('courier/orders/', OrdersCourierListView.as_view(), name='orders_courier_list'),
    path('food/', FoodListView.as_view(), name='food_list'),
    path('food/<int:pk>', FoodDetailView.as_view(), name='food_detail'),
    path('food/create', FoodCreateView.as_view(), name='food_create'),
    path('food/<int:pk>/edit', FoodUpdateView.as_view(), name='food_edit'),
    path('food/<int:pk>/delete', FoodDeleteView.as_view(), name='food_delete'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order/create', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/courier_update', OrderCourierUpdateView.as_view(), name='order_courier_update'),
    path('order/<int:pk>/food/create', OrderFoodAjaxCreateView.as_view(), name='order_food_create'),
    path('order/<int:pk>/food/delete', OrderFoodDeleteView.as_view(), name='order_food_delete'),
    path('order/food/<int:pk>/update', OrderFoodAjaxUpdateView.as_view(), name='order_food_update'),
]
