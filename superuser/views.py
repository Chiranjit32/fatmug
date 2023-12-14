from django.shortcuts import render
import environ
from fatmug.decorators import login_required
from django.urls import reverse
from decimal import Decimal
from api import models
# Create your views here.

env = environ.Env()
environ.Env.read_env()
context = {}
context['project_name'] = env("PROJECT_NAME")


@login_required
def dashboard(request):
    context.update({
        'page_title': "Dashboard",
        'breadcrumbs': [{'name': "Dashboard", 'url': reverse('superuser:dashboard')}]
    })
    return render(request, 'portal/dashboard.html', context)



@login_required
def vendorList(request):
    context.update({
        'page_title': "Vendor List",
        'breadcrumbs': [{'name': "Dashboard", 'url': reverse('superuser:dashboard')}, {'name': "Vendor", 'url': reverse('superuser:vendorList')}, {'name': "List"}]
    })
    return render(request, 'portal/Vendor/list.html', context)



@login_required
def vendorAdd(request):
    context.update({
        'page_title': "Vendor Add",
        'breadcrumbs': [{'name': "Dashboard", 'url': reverse('superuser:dashboard')}, {'name': "Vendor", 'url': reverse('superuser:vendorList')}, {'name': "Add"}]
    })
    return render(request, 'portal/Vendor/add.html', context)


@login_required
def vendorEdit(request, id):
    vendor = models.Vendor.objects.get(pk=id)
    context.update({
        'vendor': vendor,
        'page_title': "Vendor Edit",
        'breadcrumbs': [{'name': "Dashboard", 'url': reverse('superuser:dashboard')}, {'name': "Vendor", 'url': reverse('superuser:vendorList')}, {'name': "Edit"}]
    })
    return render(request, 'portal/Vendor/edit.html', context)


@login_required
def purchaseOrderList(request):
    context.update({
        'page_title': "Purchase Order List",
        'breadcrumbs': [{'name': "Dashboard", 'url': reverse('superuser:dashboard')}, {'name': "Purchase Order", 'url': reverse('superuser:purchaseOrderList')}, {'name': "List"}]
    })
    return render(request, 'portal/Purchase Order/list.html', context)


@login_required
def purchaseOrderAdd(request):
    context.update({
        'page_title': "Purchase Order Add",
        'breadcrumbs': [{'name': "Dashboard", 'url': reverse('superuser:dashboard')}, {'name': "Purchase Order", 'url': reverse('superuser:purchaseOrderList')}, {'name': "Add"}]
    })
    return render(request, 'portal/Purchase Order/add.html', context)


@login_required
def purchaseOrderEdit(request, id):
    purchaseOrder = models.Purchase_Order.objects.get(pk=id)
    context.update({
        'purchaseOrder': purchaseOrder,
        'page_title': "Purchase Order Edit",
        'breadcrumbs': [{'name': "Dashboard", 'url': reverse('superuser:dashboard')}, {'name': "Purchase Order", 'url': reverse('superuser:purchaseOrderList')}, {'name': "Edit"}]
    })
    return render(request, 'portal/Purchase Order/edit.html', context)


@login_required
def purchaseOrderView(request, id):
    purchaseOrder = models.Purchase_Order.objects.get(pk=id)
    total_amount = 0
    for item in purchaseOrder.items:
        total_amount += Decimal(item['price'])
    context.update({
        'purchaseOrder': purchaseOrder,
        'total_amount': total_amount,
        'page_title': "Purchase Order View",
        'breadcrumbs': [{'name': "Dashboard", 'url': reverse('superuser:dashboard')}, {'name': "Purchase Order", 'url': reverse('superuser:purchaseOrderList')}, {'name': "View"}]
    })
    return render(request, 'portal/Purchase Order/view.html', context)
