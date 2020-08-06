from rest_framework            import serializers
from reports_management.models import OperatingSystem, SystemType, ReportState, System, Complexity, AttackType, Report

#OperatingSystem serializer
class OperatingSystemOldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=25)

    def create(self, validated_data):
        return OperatingSystem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name=validated_data.get("name", instance.name)
        instance.save()
        return instance

class OperatingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = ['id', 'name']

#SystemType Serializer
class SystemTypeOldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=25)
    

    def create(self, validated_data):
        return SystemType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name=validated_data.get("name", instance.name)
        instance.save()
        return instance

class SystemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemType
        fields = ['id', 'name']

#ReportState Serializer
class ReportStateOldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=25)

    def create(self, validated_data):
        return ReportState.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name=validated_data.get("name", instance.name)
        instance.save()
        return instance

class ReportStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportState
        fields = ['id', 'name']

#System serializer
class SystemNestedSerializer(serializers.ModelSerializer):

    OS = OperatingSystemSerializer(read_only=True)
    system_type = SystemTypeSerializer(read_only=True)

    class Meta:
        model = System
        fields = ['id', 'name', 'description', 'OS', 'system_type', 'customer']


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ['id', 'name', 'description', 'OS', 'system_type', 'customer']


#Complexity serializer
class ComplexityOldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=25)

    def create(self, validated_data):
        return Complexity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name=validated_data.get("name", instance.name)
        instance.save()
        return instance

class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity
        fields = ['id', 'name']

#AttackType serializer
class AttackTypeNestedSerializer(serializers.ModelSerializer):
    complexity = ComplexitySerializer()
    class Meta:
        model = AttackType
        fields = ['id', 'name', 'description', 'risk', 'complexity']

class AttackTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttackType
        fields = ['id', 'name', 'description', 'risk', 'complexity']

#Report serializer
class ReportNestedSerializer(serializers.ModelSerializer):
    system = SystemSerializer(read_only=True)
    state = ReportStateSerializer(read_only=True)
    attacks = AttackTypeSerializer(many=True,read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'price', 'date', 'diagnostic', 'solution', 'cve_codes', 'system', 'meeting', 'state', 'auditor',  'analyst', 'attacks']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'price', 'date', 'diagnostic', 'solution', 'cve_codes', 'system', 'meeting', 'state', 'auditor',  'analyst', 'attacks']