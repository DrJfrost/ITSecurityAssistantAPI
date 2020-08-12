from rest_framework import serializers
from meetings.models import MeetingClass, MeetingState, MeetingType, Meeting
from django.utils import timezone

class MeetingClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingClass
        fields = ['id', 'name']

class MeetingStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingState
        fields = ['id', 'name']

class MeetingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingType
        fields = ['id', 'name']

class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = ['id', 'price', 'date', 'description', 'customer', 'auditor', 'meeting_type', 'state', 'meeting_class', 'report']
        read_only_fields = ['report']
    
    def update(self, instance, validated_data):

        instance.price = validated_data.get("price", instance.price)
        instance.date = validated_data.get("date", instance.date)
        instance.description = validated_data.get("description", instance.description)
        instance.auditor = validated_data.get("auditor", instance.auditor)
        instance.meeting_type = validated_data.get("meeting_type", instance.meeting_type)
        instance.state = validated_data.get("state", instance.state)
        instance.meeting_class = validated_data.get("meeting_class", instance.meeting_class)

        instance.save()
        return instance

    def validate_customer(self, value):
        
        if value.is_staff or value.is_superuser:
            raise serializers.ValidationError("The user is not a customer")
        return value

    def validate_auditor(self, value):
        
        if value.is_staff and not value.is_superuser and not value.staff_profile.position.name == "Auditor" or not value.is_staff:
            raise serializers.ValidationError("The user is not an auditor")
        return value

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("date must be equal or grater than current time")
        return value


class MeetingInfoSerializer(serializers.ModelSerializer):

    meeting_class = MeetingClassSerializer()
    state = MeetingStateSerializer()
    meeting_type = MeetingTypeSerializer()

    class Meta:
        model=Meeting
        fields = ['id', 'price', 'date', 'description', 'customer', 'auditor', 'meeting_type', 'state', 'meeting_class', 'report']