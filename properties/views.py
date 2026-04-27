import csv
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ViewingRequestForm
from .models import Property, ViewingRequest


def property_list(request):
    """Каталог + простая фильтрация.

    Подсказка для самостоятельной проверки: открой страницу с параметрами
    ?deal_type=rent&price_max=50000 и посмотри, как меняется QuerySet.
    """
    properties = Property.objects.filter(status=Property.STATUS_ACTIVE)
    deal_type = request.GET.get('deal_type')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if deal_type:
        properties = properties.filter(deal_type=deal_type)
    if price_min:
        properties = properties.filter(price__gte=price_min)
    if price_max:
        properties = properties.filter(price__lte=price_max)

    return render(request, 'properties/property_list.html', {
        'properties': properties,
        'deal_type': deal_type,
        'price_min': price_min or '',
        'price_max': price_max or '',
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, status=Property.STATUS_ACTIVE)

    if request.method == 'POST':
        form = ViewingRequestForm(request.POST)
        if form.is_valid():
            viewing_request = form.save(commit=False)
            viewing_request.property = property_obj
            viewing_request.save()
            messages.success(request, 'Спасибо, мы свяжемся с вами.')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = ViewingRequestForm()

    return render(request, 'properties/property_detail.html', {
        'property': property_obj,
        'form': form,
    })


@staff_member_required
def export_requests_csv(request):
    """Экспорт заявок в CSV для Excel.

    Мини-задание: добавь фильтр по периоду через GET-параметры date_from/date_to.
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="viewing_requests.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Дата заявки', 'Имя клиента', 'Телефон', 'Объект', 'Комментарий'])

    for item in ViewingRequest.objects.select_related('property').all():
        writer.writerow([
            item.created_at.strftime('%d.%m.%Y %H:%M'),
            item.client_name,
            item.phone,
            item.property.title,
            item.comment,
        ])

    return response
