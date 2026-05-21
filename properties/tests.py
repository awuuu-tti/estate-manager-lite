from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import ViewingRequestForm
from .models import Property, ViewingRequest


class PropertyModelTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            title='Квартира на Московской',
            address='г. Пенза, ул. Московская, 12',
            deal_type=Property.DEAL_RENT,
            price=45000,
            area=42.5,
            floor=5,
            description='Светлая квартира рядом с центром',
            status=Property.STATUS_ACTIVE,
        )

    def test_property_string_representation(self):
        self.assertEqual(str(self.property), 'Квартира на Московской — Аренда')


class ViewingRequestFormTest(TestCase):
    def test_valid_form(self):
        form = ViewingRequestForm(data={
            'client_name': 'Иван',
            'phone': '+79990000000',
            'comment': 'Хочу посмотреть объект',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_phone(self):
        form = ViewingRequestForm(data={
            'client_name': 'Иван',
            'phone': 'телефон',
            'comment': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)


class PropertyViewsTest(TestCase):
    def setUp(self):
        self.rent_property = Property.objects.create(
            title='Квартира в аренду',
            address='г. Пенза, ул. Московская, 12',
            deal_type=Property.DEAL_RENT,
            price=45000,
            area=42,
            floor=5,
            description='Квартира для аренды',
            status=Property.STATUS_ACTIVE,
        )
        self.sale_property = Property.objects.create(
            title='Дом на продажу',
            address='Пензенская область, с. Засечное',
            deal_type=Property.DEAL_SALE,
            price=5200000,
            area=120,
            floor=2,
            description='Дом для продажи',
            status=Property.STATUS_ACTIVE,
        )
        self.inactive_property = Property.objects.create(
            title='Проданный объект',
            address='г. Пенза',
            deal_type=Property.DEAL_SALE,
            price=3000000,
            area=60,
            description='Не должен отображаться',
            status=Property.STATUS_SOLD,
        )

    def test_property_list_shows_only_active_properties(self):
        response = self.client.get(reverse('property_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Квартира в аренду')
        self.assertContains(response, 'Дом на продажу')
        self.assertNotContains(response, 'Проданный объект')

    def test_filter_by_deal_type(self):
        response = self.client.get(reverse('property_list'), {'deal_type': Property.DEAL_RENT})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Квартира в аренду')
        self.assertNotContains(response, 'Дом на продажу')

    def test_filter_by_price_max(self):
        response = self.client.get(reverse('property_list'), {'price_max': '50000'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Квартира в аренду')
        self.assertNotContains(response, 'Дом на продажу')

    def test_property_detail_page(self):
        response = self.client.get(reverse('property_detail', args=[self.rent_property.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Квартира в аренду')
        self.assertContains(response, 'Записаться на просмотр')

    def test_create_viewing_request(self):
        response = self.client.post(reverse('property_detail', args=[self.rent_property.pk]), {
            'client_name': 'Анна',
            'phone': '+79991234567',
            'comment': 'Удобно посмотреть завтра',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ViewingRequest.objects.count(), 1)
        request_obj = ViewingRequest.objects.first()
        self.assertEqual(request_obj.client_name, 'Анна')
        self.assertEqual(request_obj.property, self.rent_property)


class ExportCsvTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            title='Квартира на Московской',
            address='г. Пенза, ул. Московская, 12',
            deal_type=Property.DEAL_RENT,
            price=45000,
            area=42,
            description='Описание объекта',
            status=Property.STATUS_ACTIVE,
        )
        ViewingRequest.objects.create(
            property=self.property,
            client_name='Иван',
            phone='+79990000000',
            comment='Хочу посмотреть объект',
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='Admin12345',
        )

    def test_export_requires_login(self):
        response = self.client.get(reverse('export_requests_csv'))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_export_csv(self):
        self.client.login(username='admin', password='Admin12345')
        response = self.client.get(reverse('export_requests_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8-sig')
        self.assertIn('attachment; filename="viewing_requests.csv"', response['Content-Disposition'])
        content = response.content.decode('utf-8-sig')
        self.assertIn('Дата заявки;Имя клиента;Телефон;Объект;Комментарий', content)
        self.assertIn('Иван', content)
        self.assertIn('Квартира на Московской', content)
