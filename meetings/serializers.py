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

class MeetingInfoSerializer(serializers.ModelSerializer):

    meeting_class = MeetingClassSerializer()
    state = MeetingStateSerializer()
    meeting_type = MeetingTypeSerializer()

    class Meta:
        model=Meeting
        fields = ['id', 'price', 'date', 'description', 'customer', 'auditor', 'meeting_type', 'state', 'meeting_class']