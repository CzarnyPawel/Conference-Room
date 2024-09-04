from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import ConferenceRoom, Reservation
from django.utils import timezone
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.
class AddRoom(View):
    """
    Class of adding a new conference room.
    """
    def get(self, request):
        return render(request, 'add_room1.html')
    def post(self, request):
        name = request.POST['name']
        capacity = request.POST['capacity']
        projector = request.POST.get('projector')
        if not name:
            return render(request, 'error2.html')
        if ConferenceRoom.objects.filter(name=name).exists():
            return render(request, 'error3.html')
        try:
            capacity = int(capacity)
            if capacity <= 0:
                return render(request, 'error4.html')
        except ValueError:
            return render(request, 'error9.html')
        projector = True if projector else False
        ConferenceRoom.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect('all-rooms') # do zrobienia jako redirect po utworzeniu strony głównej

class ShowAllRooms(View):
    """
    A class that shows all conference rooms.
    """
    def get(self, request):
        rooms = ConferenceRoom.objects.all()
        current_date = date.today()
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]

            room.reserved = date.today() in reservation_dates
        return render(request, 'show_rooms1.html', {'rooms': rooms, 'current_date': current_date})

    def post(self, request):
        room_name = request.POST.get('name', '')
        capacity = request.POST.get('capacity', '')
        projector = request.POST.get('projector', '')

        query = Q()

        if room_name:
            query &= Q(name__icontains=room_name)
        if capacity:
            query &= Q(capacity__gte=(int(capacity)))
        if projector:
            query &= Q(projector=True)
        rooms = ConferenceRoom.objects.filter(query)

        current_date = date.today()
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]

            room.reserved = date.today() in reservation_dates

        return render(request, 'search_room1.html', {'rooms': rooms})

class RoomDetails(View):
    """
    A class that shows all details about conference room.
    """
    def get(self, request, id):
        details = ConferenceRoom.objects.get(id=id)
        reservations = Reservation.objects.filter(room_id=id).order_by('date')
        return render(request, 'room_details1.html', {'details': details, 'reservations': reservations})



class DeleteRoom(View):
    """
    Class to remove conference room.
    """
    def get(self, request, id):
        delete_room = ConferenceRoom.objects.get(id=id)
        delete_room.delete()
        return render(request, 'error1.html')

class ModifyRoom(View):
    """
    Class that modify details in the conference room.
    """
    def get(self, request, id):
        modify_room = ConferenceRoom.objects.get(id=id)
        return render(request, 'modify_room1.html', {'modify_room': modify_room})

    def post(self, request, id):
        modify_room = ConferenceRoom.objects.get(id=id)
        name = request.POST['name']
        capacity = request.POST['capacity']
        projector = request.POST.get('projector')
        if not name:
            return render(request, 'error5.html')
        #if ConferenceRoom.objects.filter(name=name).exists():
            #return HttpResponse('Podana nazwa sali już istnieje!')
        try:
            capacity = int(capacity)
            if capacity <= 0:
                return render(request, 'error6.html')
        except ValueError:
            return render(request, 'error10.html')
        projector = True if projector else False
        modify_room.name = name
        modify_room.capacity = capacity
        modify_room.projector = projector
        modify_room.save()
        return redirect('all-rooms')

class ReserveRoom(View):
    """
    A class for booking conference room.
    """
    def get(self, request, id):
        reserve = ConferenceRoom.objects.get(id=id)
        reservations = Reservation.objects.filter(room_id=id).order_by('date')
        return render(request, 'reserve_room1.html', {'reserve': reserve, 'reservations': reservations})

    def post(self, request, id):
        room_id = ConferenceRoom.objects.get(id=id)
        booking_date = request.POST.get('date', '')
        comment = request.POST.get('comment')
        # konieczność sformatowania daty pobranej z formularza na format ISO, aby móc porównać daty ze sobą
        if not booking_date:
            return render(request, 'error5.html')
        booking_date = date.fromisoformat(booking_date)
        exist_reservation = Reservation.objects.filter(room_id=room_id, date=booking_date).exists()

        if exist_reservation:
            return render(request, 'error7.html')
            #return redirect('error1')

        if booking_date < date.today():
            return render(request, 'error8.html')

        Reservation.objects.create(date=booking_date, room_id=room_id, comment=comment)
        return redirect('all-rooms')


