

from rest_framework import serializers
from .models import Hotel, Review, Booking, District

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):

    district_name = serializers.SerializerMethodField()

    def get_district_name(self, obj):
        return obj.district.district_name if obj.district else None

    class Meta:
        model = Hotel
        fields = ['id','name','address','district_name','photo','address','description','price_per_night','available_room']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    hotel = serializers.ReadOnlyField(source='hotel.name')

    class Meta:
        model = Review
        fields = ['id', 'hotel', 'user', 'body', 'created', 'rating']



# class BookingSerializer(serializers.ModelSerializer):
#     hotel_name = serializers.SerializerMethodField()
#     username = serializers.SerializerMethodField()

#     def get_hotel_name(self, obj):
#         return obj.hotel.name if obj.hotel else None
    
#     def get_username(self, obj):
#         return obj.user.username if obj.user else None

#     class Meta:
#         model = Booking
#         fields = ['id', 'start_date', 'end_date', 'number_of_rooms', 'booked_at', 'username', 'hotel_name']


from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'hotel', 'start_date', 'end_date', 'number_of_rooms', 'booked_at']
        read_only_fields = ['id', 'user', 'booked_at']
