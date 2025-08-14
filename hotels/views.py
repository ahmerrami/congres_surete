from django.shortcuts import render, get_object_or_404
from .models import Hotel

def hotel_list(request):
    hotels = Hotel.objects.filter(active=True).order_by("name")
    return render(request, "hotels/list.html", {"hotels": hotels})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk, active=True)
    return render(request, "hotels/detail.html", {"hotel": hotel})
