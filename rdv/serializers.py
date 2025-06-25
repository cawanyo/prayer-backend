from rest_framework import serializers
from .models import RDV, RDVAvailability
from accounts.serializers import CustomUserSerializer
class RDVAvailabilitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = RDVAvailability
        fields = ['id', 'date', 'start_time', 'end_time']


class RDVSerializer(serializers.ModelSerializer):
    rdv_availabilities = RDVAvailabilitySerializer(many=True)
    selected_availability = RDVAvailabilitySerializer(read_only=True)
    created_by = CustomUserSerializer()

    class Meta:
        model = RDV
        fields = ['id',  'rdv_availabilities', 'selected_availability', 'date', 'time', 'informations', 'state', 'created_by', 'validated_by', 'created_at']
        read_only_fields = ['created_by', 'validated_by', 'created_at']

    def create(self, validated_data):
        avail_data = validated_data.pop('rdv_availabilities')
        rdv = RDV.objects.create(**validated_data)
        for avail in avail_data:
            availability = RDVAvailability.objects.create( **avail)
            rdv.rdv_availabilities.add(availability)
        return rdv

    def update(self, instance, validated_data):
        availabilities_data = validated_data.pop('rdv_availabilities', [])
        # update RDV fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # handle availabilities
        for availability_data in availabilities_data:
            availability_id = availability_data.get('id', None)
            if availability_id:
                # Update existing availability
                try:
                    availability_instance = RDVAvailability.objects.get(id=availability_id, rdvs=instance)
                    for attr, value in availability_data.items():
                        setattr(availability_instance, attr, value)
                    availability_instance.save()
                except RDVAvailability.DoesNotExist:
                    continue
            else:
                # Create new availability
                availability_instance = RDVAvailability.objects.create(**availability_data)
                availability_instance.rdvs.add(instance)

        return instance