from rest_framework import serializers
from meetings.models import MeetingClass, MeetingState, MeetingType, Meeting

class MeetingClassSerializer(serializers.ModelSerializer):

    class Meta:
        model=MeetingClass
        fields = ['id', 'name']

class MeetingStateSerializer(serializers.ModelSerializer):

    class Meta:
        model=MeetingState
        fields = ['id', 'name']

class MeetingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model=MeetingType
        fields = ['id', 'name']

class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model=Meeting
        fields = ['id', 'price', 'date', 'description', 'customer', 'auditor', 'meeting_type', 'state', 'meeting_class']

    def validate_customer(self, value):
        
        if value.is_staff or value.is_superuser:
            raise serializers.ValidationError("The user is not a customer")
        return value

    def validate_auditor(self, value):
        
        if value.is_staff and not value.is_superuser and not value.staff_profile.position.name=="Auditor":
            raise serializers.ValidationError("The user is not an auditor")
        elif not value.is_staff:
            raise serializers.ValidationError("The user is not an auditor") 
        return value
class MeetingInfoSerializer(serializers.ModelSerializer):

    meeting_class = MeetingClassSerializer()
    state = MeetingStateSerializer()
    meeting_type = MeetingTypeSerializer()

    class Meta:
        model=Meeting
        fields = ['id', 'price', 'date', 'description', 'customer', 'auditor', 'meeting_type', 'state', 'meeting_class']