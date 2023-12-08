from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format='%m-%d-%Y')
    class Meta:
        model = User
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists.')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    iqama_number = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)


    def validate(self, attrs):
        iqama_number = attrs.get('iqama_number')
        password = attrs.get('password')

        if not iqama_number or not password:
            raise serializers.ValidationError("Please give both iqama_number and password.")

        if not User.objects.filter(iqama_number=iqama_number).exists():
            raise serializers.ValidationError('Iqama Number/ID not exist.')

        user = authenticate(request=self.context.get('request'), iqama_number=iqama_number,
                            password=password)
        print(user, "AAAAAAAARGH")
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        return attrs
