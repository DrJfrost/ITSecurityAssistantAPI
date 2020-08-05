from rest_framework import serializers
from users.models import Identification, StaffProfile, User, Position

class IdentificationSelializer(serializers.ModelSerializer):

    class Meta:
        model = Identification
        fields = ['id']

class StaffProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffProfile
        fields = ['id', 'join_date', 'position', 'user']

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'image', 'phone', 'identification']
        extra_kwargs = {'password': {'write_only':True}}

class UserNestedSerializer(serializers.ModelSerializer):

    identification = IdentificationSelializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'image', 'phone', 'identification']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        identification = validated_data.pop("identification")
        identification_obj = Identification.objects.create(**identification)

        user = User.objects.create(**validated_data, identification=identification_obj)
        user.set_password(user.password)
        user.save()

        return user
    
    def update(self, instance, validated_data):

        identification_data = validated_data.pop("identification")
        instance.username = validated_data.get("username", instance.username)

        identification_obj = instance.identification
        identification_obj.id = identification_data.get("id", identification_obj.id)

        identification_obj.save()

        instance.save()

        return instance

class StaffUserNestedSerializer(serializers.ModelSerializer):

    staff_profile = StaffProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'image', 'phone', 'identification', 'staff_profile']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):

        identification = validated_data.pop("identification")
        identification_obj = Identification.objects.create(id=identification)

        user = User.objects.create(**validated_data, identification=identification_obj)
        user.set_password(user.password)
        user.save()

        staff_data = validated_data.pop("staff_profile")
        staff_obj = StaffProfile.objects.create(**staff_data, user=user)
        staff_obj.save()

        return user
    
    def update(self, instance, validated_data):

        staff_data = validated_data.pop("staff_profile")
        staff_obj = instance.staff_profile
        staff_obj.position = staff_data.get("position", staff_obj.position)
        instance.username = validated_data.get("username", instance.username)

        instance.save()

        return instance
    
    def validate_identification(self, data):
        identification = Identification.objects.filter(id=data.id)
        if identification.exists():
            raise serializers.ValidationError("User id already exists")


class PositionSelializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ['id', 'name']

