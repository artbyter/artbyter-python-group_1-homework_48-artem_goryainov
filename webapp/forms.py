from django import forms
from webapp.models import Food, Order, OrderFood


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = []


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [Order.STATUS_CHOICES[Order.STATUS_NEW],
                                         Order.STATUS_CHOICES[Order.STATUS_PREPARING],
                                         Order.STATUS_CHOICES[Order.STATUS_CANCELED], ]

    class Meta:
        model = Order
        exclude = ['courier', 'operator']


class OrderCourierForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [Order.STATUS_CHOICES[Order.STATUS_DELIVERED],
                                         Order.STATUS_CHOICES[Order.STATUS_ON_WAY] ]

    class Meta:
        model = Order
        fields = ['status', 'courier']


class OrderFoodForm(forms.ModelForm):
    class Meta:
        model = OrderFood
        exclude = ['order']
