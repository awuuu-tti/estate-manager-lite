from django.db import models
from django.core.validators import RegexValidator


class Property(models.Model):
    """Карточка объекта недвижимости.

    Учебное задание: проверь, какие поля прямо указаны в ТЗ,
    и добавь недостающие характеристики самостоятельно.
    """
    DEAL_SALE = 'sale'
    DEAL_RENT = 'rent'
    DEAL_CHOICES = [
        (DEAL_SALE, 'Продажа'),
        (DEAL_RENT, 'Аренда'),
    ]

    STATUS_ACTIVE = 'active'
    STATUS_SOLD = 'sold'
    STATUS_RENTED = 'rented'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Активен'),
        (STATUS_SOLD, 'Продан'),
        (STATUS_RENTED, 'Сдан'),
    ]

    title = models.CharField('Название', max_length=150)
    address = models.CharField('Адрес', max_length=255)
    deal_type = models.CharField('Тип сделки', max_length=10, choices=DEAL_CHOICES)
    price = models.PositiveIntegerField('Цена')
    area = models.DecimalField('Площадь, м²', max_digits=8, decimal_places=2)
    floor = models.IntegerField('Этаж', blank=True, null=True)
    description = models.TextField('Описание')
    main_photo = models.ImageField('Главное фото', upload_to='properties/', blank=True, null=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объект недвижимости'
        verbose_name_plural = 'Объекты недвижимости'

    def __str__(self):
        return f'{self.title} — {self.get_deal_type_display()}'


class ViewingRequest(models.Model):
    """Заявка клиента на просмотр объекта."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='requests', verbose_name='Объект')
    client_name = models.CharField('Имя клиента', max_length=100)
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[RegexValidator(r'^\+?[0-9\-\s()]{7,20}$', 'Введите корректный телефон.')],
    )
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка на просмотр'
        verbose_name_plural = 'Заявки на просмотр'

    def __str__(self):
        return f'{self.client_name}: {self.property.title}'
