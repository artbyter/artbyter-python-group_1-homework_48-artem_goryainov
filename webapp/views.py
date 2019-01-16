from django.views.generic import DetailView, CreateView, UpdateView, View, DeleteView, ListView, FormView
from django.urls import reverse
from django.http import HttpResponseRedirect
from webapp.models import Food, Order, OrderFood
from webapp.forms import FoodForm, OrderForm, OrderFoodForm, OrderCourierForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q


class InitialView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'couriers' in request.user.groups.values_list('name', flat=True):
            return HttpResponseRedirect(reverse('webapp:orders_courier_list'))
        else:
            return HttpResponseRedirect(reverse('webapp:orders_list'))


class FoodListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Food
    template_name = 'food_list.html'
    permission_required = 'webapp.view_food'


class FoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Food
    template_name = 'food_create.html'
    form_class = FoodForm
    permission_required = 'webapp.add_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})


class FoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Food
    template_name = 'food_edit.html'
    form_class = FoodForm
    permission_required = 'webapp.change_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})


class FoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Food
    template_name = 'food_delete.html'
    permission_required = 'webapp.delete_food'

    def get_success_url(self):
        return reverse('webapp:food_list', kwargs={})


class FoodDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Food
    template_name = 'food_detail.html'
    permission_required = 'webapp.view_food'


class OrdersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'index.html'
    permission_required = 'webapp.is_operator'


class OrdersCourierListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'index.html'
    permission_required = 'webapp.is_courier'

    def get_queryset(self):
        queryset = Order.objects.filter(Q(status=Order.STATUS_PREPARING) | Q(status=Order.STATUS_ON_WAY))
        return queryset


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView,FormView):
    model = Order
    template_name = 'order_detail.html'
    permission_required = 'webapp.view_order'
    form_class = OrderFoodForm


class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    template_name = 'order_update.html'
    form_class = OrderForm
    permission_required = 'webapp.change_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})


class OrderCourierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    template_name = 'order_update.html'
    fields = []
    permission_required = 'webapp.is_courier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = 'Взять заказ' if self.object.status == Order.STATUS_PREPARING else 'Завершить заказ'
        context['if_own_order'] = self.object.courier == self.request.user
        return context

    def form_valid(self, form):
        self.object.courier = self.request.user

        if self.object.status == Order.STATUS_PREPARING:
            self.object.status = Order.STATUS_ON_WAY
        elif self.object.status == Order.STATUS_ON_WAY:
            self.object.status = Order.STATUS_DELIVERED
        else:
            return super().form_invalid(self.form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})


# Представления для создания заказа
class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm
    permission_required = 'webapp.add_order'

    def form_valid(self, form):
        form.instance.operator = self.request.user
        if form.instance.status != Order.STATUS_NEW:
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})


# ... и для добавления блюд в заказ
class OrderFoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_create.html'
    permission_required = 'webapp.add_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_pk'] = self.kwargs.get('pk')
        return context

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class OrderFoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = OrderFood
    template_name = 'order_food_delete.html'
    permission_required = 'webapp.delete_food'

    def post(self, request, *args, **kwargs):
        if request.POST.get('delete')=='no':
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(OrderFoodDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})
