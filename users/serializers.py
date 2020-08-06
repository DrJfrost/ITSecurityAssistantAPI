from rest_framework import serializers
from users.models import Identification, StaffProfile, User, Position

class IdentificationSelializer(serializers.ModelSerializer):

    class Meta:
        model = Identification
        fields = ['id']

class StaffProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffProfile
        fields = ['id', 'join_date', 'position']

class CustomerUserNestedSerializer(serializers.ModelSerializer):

    identification = IdentificationSelializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'image', 'phone', 'identification']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        identification = validated_data.pop("identification")
        identification_obj = Identification.objects.create(**identification)

        user = User.objects.create(**validated_data, identification=identification_obj, is_staff=False)
        user.set_password(user.password)
        user.save()

        return user
    
    def update(self, instance, validated_data):

        return instance

class StaffUserNestedSerializer(serializers.ModelSerializer):

    identification = IdentificationSelializer()
    staff_profile = StaffProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'image', 'phone', 'identification', 'staff_profile']
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):

        print(validated_data)
        identification = validated_data.pop("identification")
        identification_obj = Identification.objects.create(id=identification["id"])

        staff_data = validated_data.pop("staff_profile")

        user = User.objects.create(**validated_data, identification=identification_obj, is_staff=True)
        user.set_password(user.password)
        user.save()

        staff_obj = StaffProfile.objects.create(**staff_data, user=user)
        staff_obj.save()

        return user
    
    def update(self, instance, validated_data):

        return instance
    

class PositionSelializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ['id', 'name']

