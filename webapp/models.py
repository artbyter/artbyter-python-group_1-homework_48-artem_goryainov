from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='employee', verbose_name='Пользователь')
    phone = models.CharField(max_length=50, verbose_name='Телефон')

    def __str__(self):
        return self.user.get_full_name()
    class Meta:
        permissions = [
            ('is_courier', 'Разрешения курьера'),
            ('is_operator', 'Разрешения оператора')
        ]


class Food(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(verbose_name='Фотография')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_NEW = 0
    STATUS_PREPARING = 1
    STATUS_ON_WAY = 2
    STATUS_DELIVERED = 3
    STATUS_CANCELED = 4

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый'),
        (STATUS_PREPARING, 'Готовится'),
        (STATUS_ON_WAY, 'В пути'),
        (STATUS_DELIVERED, 'Доставлен'),
        (STATUS_CANCELED, 'Отменён')
    )

    contact_phone = models.CharField(max_length=50, verbose_name='Контактный телефон')
    contact_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    delivery_address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Адрес доставки')
    status = models.IntegerField(default=STATUS_NEW, verbose_name='Статус', choices=STATUS_CHOICES)
    operator = models.ForeignKey(User, null=True, blank=True, related_name='orders', verbose_name='Оператор',
                                 on_delete=models.PROTECT)
    courier = models.ForeignKey(User, null=True, blank=True, related_name='delivered', verbose_name='Курьер',
                                on_delete=models.PROTECT)

    def __str__(self):
        return self.contact_phone


class OrderFood(models.Model):
    order = models.ForeignKey(Order, related_name='foods', verbose_name='Заказ', on_delete=models.PROTECT)
    food = models.ForeignKey(Food, related_name='+', verbose_name='Блюдо', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return str(self.food)
