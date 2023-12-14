from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.views import View
from . import models
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q, F
import math
import environ

env = environ.Env()
environ.Env.read_env()


class CustomPaginator:
    def __init__(self, items, per_page):
        self.items = items
        self.per_page = per_page

    def get_page(self, page_number):
        page_number = int(page_number)  # Convert to integer
        start = (page_number - 1) * self.per_page
        end = start + self.per_page
        page_items = self.items[start:end]
        return page_items

    def get_total_pages(self):
        return math.ceil(len(self.items) / self.per_page)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def loginUser(request):
    context = {}
    user = models.User.objects.get(pk=request.user.id)
    if user is not None:
        login(request, user)
        context.update({'status': 200, 'message': ""})
    else:
        context.update({'status': 501, 'message': "User Not Found."})
    return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    context = {}
    logout(request)
    try:
        del request.session
    except:
        pass
    try:
        storage = get_messages(request)
        for message in storage:
            message = ''
        storage.used = False
    except:
        pass
    context.update({'status': 200, 'message': "Logged Out Successfully."})
    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserDetails(request):
    context = {}
    context.update({'status': 200, 'message': "User Details Fetched Successfully.",
                   'userDetails': serializers.serialize('json', [request.user])})
    return JsonResponse(context, safe=False)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vendorListCreate(request):
    context = {}
    if request.method == 'GET':
        pk = request.GET.get('pk', None)
        find_all = request.GET.get('find_all', None)
        keyword = request.GET.get('keyword', None)
        if pk is not None and pk != "":
            vendor = list(models.Vendor.objects.filter(pk=pk)[:1].values('pk', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate'))
            context.update({
                'status': 200,
                'message': "Vendor Fetched Successfully.",
                'page_items': vendor,
            })
        else:
            if keyword is not None and keyword != "":
                vendors = list(models.Vendor.objects.filter(Q(name__icontains=keyword) | Q(vendor_code__icontains=keyword) | Q(contact_details__icontains=keyword)).values('pk', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate'))
            else:
                vendors = list(models.Vendor.objects.values('pk', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate'))
            if find_all is not None and int(find_all) == 1:
                context.update({
                    'status': 200,
                    'message': "Vendors Fetched Successfully.",
                    'page_items': vendors,
                })
                return JsonResponse(context)
            per_page = int(env("PER_PAGE_DATA"))
            button_to_show = int(env("PER_PAGE_PAGINATION_BUTTON"))
            current_page = request.GET.get('current_page', 1)

            paginator = CustomPaginator(vendors, per_page)
            page_items = paginator.get_page(current_page)
            total_pages = paginator.get_total_pages()

            context.update({
                'status': 200,
                'message': "Vendors Fetched Successfully.",
                'page_items': page_items,
                'total_pages': total_pages,
                'current_page': int(current_page),
                'button_to_show': int(button_to_show),
            })
        return JsonResponse(context)
    elif request.method == 'POST':
        if not request.POST['name'] or not request.POST['vendor_code'] or not request.POST['contact_details'] or not request.POST['address']:
            context.update({
                'status': 501,
                'message': "Vendor Name/Vendor Code/Contact Details/Address has not been provided."
            })
        exist_data = models.Vendor.objects.filter(vendor_code__iexact=request.POST['vendor_code'])
        if len(exist_data) > 0:
            context.update({
                'status': 502,
                'message': "Vendor with this code already exists."
            })
            return JsonResponse(context)
        try:
            with transaction.atomic():
                vendor = models.Vendor()
                vendor.name = request.POST['name']
                vendor.vendor_code = request.POST['vendor_code']
                vendor.contact_details = request.POST['contact_details']
                vendor.address = request.POST['address']
                vendor.save()
            transaction.commit()
            context.update({
                'status': 200,
                'message': "Vendor Created Successfully."
            })
        except Exception:
            context.update({
                'status': 503,
                'message': "Something Went Wrong. Please Try Again."
            })
            transaction.rollback()
        return JsonResponse(context)
    return JsonResponse(context)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def vendorRetrieveUpdateDelete(request, pk):
    context = {}
    if request.method == 'GET':
        vendor = list(models.Vendor.objects.filter(pk=pk)[:1].values('pk', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate'))
        context.update({
            'status': 200,
            'message': "Vendor Fetched Successfully.",
            'page_items': vendor,
        })
        return JsonResponse(context)
    elif request.method == 'PUT':
        if not request.POST['name'] or not request.POST['vendor_code'] or not request.POST['contact_details'] or not request.POST['address']:
            context.update({
                'status': 504,
                'message': "Vendor Name/Vendor Code/Contact Details/Address has not been provided."
            })
        exist_data = models.Vendor.objects.filter(vendor_code__iexact=request.POST['vendor_code']).exclude(pk=pk)
        if len(exist_data) > 0:
            context.update({
                'status': 505,
                'message': "Vendor with this code already exists."
            })
            return JsonResponse(context)
        try:
            with transaction.atomic():
                vendor = models.Vendor.objects.get(pk=pk)
                vendor.name = request.POST['name']
                vendor.vendor_code = request.POST['vendor_code']
                vendor.contact_details = request.POST['contact_details']
                vendor.address = request.POST['address']
                vendor.save()
            transaction.commit()
            context.update({
                'status': 200,
                'message': "Vendor Updated Successfully."
            })
        except Exception:
            context.update({
                'status': 506,
                'message': "Something Went Wrong. Please Try Again."
            })
            transaction.rollback()
        return JsonResponse(context)
    elif request.method == 'DELETE':
        vendor = models.Vendor.objects.get(pk=pk)
        try:
            with transaction.atomic():
                vendor.delete()
            transaction.commit()
            context.update({
                'status': 200,
                'message': "Vendor Deleted Successfully."
            })
        except Exception:
            context.update({
                'status': 507,
                'message': "Something Went Wrong. Please Try Again."
            })
            transaction.rollback()
        return JsonResponse(context)
    return JsonResponse(context)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def purchaseOrderListCreate(request):
    context = {}
    if request.method == 'GET':
        pk = request.GET.get('pk', None)
        find_all = request.GET.get('find_all', None)
        keyword = request.GET.get('keyword', None)
        vendor_id = request.GET.get('vendor_id', None)
        if pk is not None and pk != "":
            purchaseOrder = list(models.Purchase_Order.objects.filter(pk=pk)[:1].values('pk', 'vendor__name', 'vendor', 'po_number', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date'))
            context.update({
                'status': 200,
                'message': "Purchase Order Fetched Successfully.",
                'page_items': purchaseOrder,
            })
        else:
            if vendor_id is not None and vendor_id != "":
                purchaseOrders = models.Purchase_Order.objects.filter(vendor_id=vendor_id)
            else:
                purchaseOrders = models.Purchase_Order.objects.all()
            if keyword is not None and keyword != "":
                purchaseOrders = purchaseOrders.filter(Q(vendor__name__icontains=keyword) | Q(po_number__icontains=keyword) | Q(order_date__icontains=keyword) | Q(delivery_date__icontains=keyword) | Q(status__icontains=keyword))
            purchaseOrders = list(purchaseOrders.values('pk', 'vendor__name', 'vendor', 'po_number', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date'))
            if find_all is not None and int(find_all) == 1:
                context.update({
                    'status': 200,
                    'message': "Purchase Orders Fetched Successfully.",
                    'page_items': purchaseOrders,
                })
                return JsonResponse(context)

            per_page = int(env("PER_PAGE_DATA"))
            button_to_show = int(env("PER_PAGE_PAGINATION_BUTTON"))
            current_page = request.GET.get('current_page', 1)

            paginator = CustomPaginator(purchaseOrders, per_page)
            page_items = paginator.get_page(current_page)
            total_pages = paginator.get_total_pages()

            context.update({
                'status': 200,
                'message': "Purchase Orders Fetched Successfully.",
                'page_items': page_items,
                'total_pages': total_pages,
                'current_page': int(current_page),
                'button_to_show': int(button_to_show),
            })
        return JsonResponse(context)
    elif request.method == 'POST':
        print(request.POST)
        if not request.POST['po_number'] or not request.POST['vendor'] or not request.POST['order_date'] or not request.POST['delivery_date'] or not request.POST['status'] or not request.POST['quantity'] or not request.POST['quality_rating'] or not request.POST['issue_date'] or not request.POST['acknowledgment_date']:
            context.update({
                'status': 508,
                'message': "PO Number/Vendor/Order Date/Delivery Date/Status/Quantity/Quality Rating/Issue Date/Acknowledgment Date has not been provided."
            })
        exist_data = models.Purchase_Order.objects.filter(po_number__iexact=request.POST['po_number'])
        if len(exist_data) > 0:
            context.update({
                'status': 509,
                'message': "Purchase Order with this PO Number already exists."
            })
            return JsonResponse(context)
        # Parse the items data
        items = []
        for key, value in request.POST.items():
            if key.startswith('items['):
                item_index = int(key.split('[')[1].split(']')[0])
                item_field = key.split('[')[2].split(']')[0]
                if len(items) <= item_index:
                    items.append({})
                items[item_index][item_field] = value
        # Convert string values to the appropriate types
        for item in items:
            item['rate'] = int(item['rate'])
            item['quantity'] = int(item['quantity'])
            item['price'] = float(item['price'])
        try:
            with transaction.atomic():
                purchaseOrder = models.Purchase_Order()
                purchaseOrder.po_number = request.POST['po_number']
                purchaseOrder.vendor_id = request.POST['vendor']
                purchaseOrder.order_date = request.POST['order_date']
                purchaseOrder.delivery_date = request.POST['delivery_date']
                purchaseOrder.status = request.POST['status']
                purchaseOrder.quantity = request.POST['quantity']
                purchaseOrder.quality_rating = request.POST['quality_rating']
                purchaseOrder.issue_date = request.POST['issue_date']
                purchaseOrder.acknowledgment_date = request.POST['acknowledgment_date']
                purchaseOrder.items = items
                purchaseOrder.save()

                completed_orders = purchaseOrder.vendor.purchase_order_set.filter(status='completed')

                # On-Time Delivery Rate
                completed_on_time = completed_orders.filter(delivery_date__lte=F('acknowledgment_date'))
                purchaseOrder.vendor.on_time_delivery_rate = (completed_on_time.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

                # Quality Rating Average
                quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
                purchaseOrder.vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0

                # Average Response Time
                response_times = completed_orders.exclude(acknowledgment_date__isnull=True).values_list('acknowledgment_date', 'issue_date')
                average_response_time = sum((ack_date - issue_date).seconds for ack_date, issue_date in response_times) / len(response_times) if len(response_times) > 0 else 0
                purchaseOrder.vendor.average_response_time = average_response_time / 3600  # Convert seconds to hours

                # Fulfillment Rate
                successful_orders = completed_orders.filter(status='completed', issue_date__lte=F('acknowledgment_date'))
                purchaseOrder.vendor.fulfillment_rate = (successful_orders.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

                purchaseOrder.vendor.save()

                historical_performances = models.Historical_Performance()
                historical_performances.vendor_id = purchaseOrder.vendor.pk
                historical_performances.on_time_delivery_rate = purchaseOrder.vendor.on_time_delivery_rate
                historical_performances.quality_rating_avg = purchaseOrder.vendor.quality_rating_avg
                historical_performances.average_response_time = purchaseOrder.vendor.average_response_time
                historical_performances.fulfillment_rate = purchaseOrder.vendor.fulfillment_rate
                historical_performances.save()
            transaction.commit()
            context.update({
                'status': 200,
                'message': "Purchase Order Created Successfully."
            })
        except Exception:
            context.update({
                'status': 510,
                'message': "Something Went Wrong. Please Try Again."
            })
            transaction.rollback()
        return JsonResponse(context)
    return JsonResponse(context)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def purchaseOrderRetrieveUpdateDelete(request, pk):
    context = {}
    if request.method == 'GET':
        purchaseOrder = list(models.Purchase_Order.objects.filter(pk=pk)[:1].values('pk', 'po_number', 'vendor', 'vendor__name', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date'))
        context.update({
            'status': 200,
            'message': "Purchase Order Fetched Successfully.",
            'page_items': purchaseOrder,
        })
        return JsonResponse(context)
    elif request.method == 'PUT':
        if not request.POST['po_number'] or not request.POST['vendor'] or not request.POST['order_date'] or not request.POST['delivery_date'] or not request.POST['status'] or not request.POST['quantity'] or not request.POST['quality_rating'] or not request.POST['issue_date'] or not request.POST['acknowledgment_date']:
            context.update({
                'status': 511,
                'message': "PO Number/Vendor/Order Date/Delivery Date/Status/Quantity/Quality Rating/Issue Date/Acknowledgment Date has not been provided."
            })
        exist_data = models.Purchase_Order.objects.filter(po_number__iexact=request.POST['po_number']).exclude(pk=pk)
        if len(exist_data) > 0:
            context.update({
                'status': 512,
                'message': "Purchase Order with this PO Number already exists."
            })
            return JsonResponse(context)
        # Parse the items data
        items = []
        for key, value in request.POST.items():
            if key.startswith('items['):
                item_index = int(key.split('[')[1].split(']')[0])
                item_field = key.split('[')[2].split(']')[0]
                if len(items) <= item_index:
                    items.append({})
                items[item_index][item_field] = value
        # Convert string values to the appropriate types
        for item in items:
            item['rate'] = int(item['rate'])
            item['quantity'] = int(item['quantity'])
            item['price'] = float(item['price'])
        
        try:
            with transaction.atomic():
                purchaseOrder = models.Purchase_Order.objects.get(pk=pk)
                purchaseOrder.po_number = request.POST['po_number']
                purchaseOrder.vendor_id = request.POST['vendor']
                purchaseOrder.order_date = request.POST['order_date']
                purchaseOrder.delivery_date = request.POST['delivery_date']
                purchaseOrder.status = request.POST['status']
                purchaseOrder.quantity = request.POST['quantity']
                purchaseOrder.quality_rating = request.POST['quality_rating']
                purchaseOrder.issue_date = request.POST['issue_date']
                purchaseOrder.acknowledgment_date = request.POST['acknowledgment_date']
                purchaseOrder.items = items
                purchaseOrder.save()

                completed_orders = purchaseOrder.vendor.purchase_order_set.filter(status='completed')

                # On-Time Delivery Rate
                completed_on_time = completed_orders.filter(delivery_date__lte=F('acknowledgment_date'))
                purchaseOrder.vendor.on_time_delivery_rate = (completed_on_time.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

                # Quality Rating Average
                quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
                purchaseOrder.vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0

                # Average Response Time
                response_times = completed_orders.exclude(acknowledgment_date__isnull=True).values_list('acknowledgment_date', 'issue_date')
                average_response_time = sum((ack_date - issue_date).seconds for ack_date, issue_date in response_times) / len(response_times) if len(response_times) > 0 else 0
                purchaseOrder.vendor.average_response_time = average_response_time / 3600  # Convert seconds to hours

                # Fulfillment Rate
                successful_orders = completed_orders.filter(status='completed', issue_date__lte=F('acknowledgment_date'))
                purchaseOrder.vendor.fulfillment_rate = (successful_orders.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

                purchaseOrder.vendor.save()

                historical_performances = models.Historical_Performance()
                historical_performances.vendor_id = purchaseOrder.vendor.pk
                historical_performances.on_time_delivery_rate = purchaseOrder.vendor.on_time_delivery_rate
                historical_performances.quality_rating_avg = purchaseOrder.vendor.quality_rating_avg
                historical_performances.average_response_time = purchaseOrder.vendor.average_response_time
                historical_performances.fulfillment_rate = purchaseOrder.vendor.fulfillment_rate
                historical_performances.save()
            transaction.commit()
            context.update({
                'status': 200,
                'message': "Purchase Order Updated Successfully."
            })
        except Exception:
            context.update({
                'status': 513,
                'message': "Something Went Wrong. Please Try Again."
            })
            transaction.rollback()
        return JsonResponse(context)
    elif request.method == 'DELETE':
        purchaseOrder = models.Purchase_Order.objects.get(pk=pk)
        try:
            with transaction.atomic():
                completed_orders = purchaseOrder.vendor.purchase_order_set.filter(status='completed')

                # On-Time Delivery Rate
                completed_on_time = completed_orders.filter(delivery_date__lte=F('acknowledgment_date'))
                purchaseOrder.vendor.on_time_delivery_rate = (completed_on_time.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

                # Quality Rating Average
                quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
                purchaseOrder.vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0

                # Average Response Time
                response_times = completed_orders.exclude(acknowledgment_date__isnull=True).values_list('acknowledgment_date', 'issue_date')
                average_response_time = sum((ack_date - issue_date).seconds for ack_date, issue_date in response_times) / len(response_times) if len(response_times) > 0 else 0
                purchaseOrder.vendor.average_response_time = average_response_time / 3600  # Convert seconds to hours

                # Fulfillment Rate
                successful_orders = completed_orders.filter(status='completed', issue_date__lte=F('acknowledgment_date'))
                purchaseOrder.vendor.fulfillment_rate = (successful_orders.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

                purchaseOrder.vendor.save()

                historical_performances = models.Historical_Performance()
                historical_performances.vendor_id = purchaseOrder.vendor.pk
                historical_performances.on_time_delivery_rate = purchaseOrder.vendor.on_time_delivery_rate
                historical_performances.quality_rating_avg = purchaseOrder.vendor.quality_rating_avg
                historical_performances.average_response_time = purchaseOrder.vendor.average_response_time
                historical_performances.fulfillment_rate = purchaseOrder.vendor.fulfillment_rate
                historical_performances.save()
                purchaseOrder.delete()
            transaction.commit()
            context.update({
                'status': 200,
                'message': "Purchase Order Deleted Successfully."
            })
        except Exception:
            context.update({
                'status': 514,
                'message': "Something Went Wrong. Please Try Again."
            })
            transaction.rollback()
        return JsonResponse(context)
    return JsonResponse(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendorPerformance(request, vendor_id):
    context = {}
    if request.method == 'GET':
        try:
            vendor = models.Vendor.objects.get(pk=vendor_id)
            context.update({
                'status': 200,
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'average_response_time': vendor.average_response_time,
                'fulfillment_rate': vendor.fulfillment_rate,
            })
            return JsonResponse(context)
        except models.Vendor.DoesNotExist:
            context.update({
                'status': 515,
                'message': "Vendor Not Found."
            })
            return JsonResponse(context)