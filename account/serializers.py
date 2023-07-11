from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True,
                                     required=True)
    password_confirmation = serializers.CharField(min_length=8, write_only=True,
                                                  required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation')

    def validate(self, attrs):
        password_confirmation = attrs.pop('password_confirmation')
        if password_confirmation != attrs['password']:
            raise serializers.ValidationError(
                'Пароль не совподает'
            )
        if not attrs['first_name'].istitle():
            raise serializers.ValidationError(
                'Имя долно начинатся с большой буквы'
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        request = self.context.get('request')
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username,
                                password=password,
                                request = request)

            if not user:
                raise serializers.ValidationError(
                    'неверные данные'
                )
        else:
            raise serializers.ValidationError(
                'заполни данные!'
            )
        data['user'] = user
        return data

    def validate_usename(self, username):
        print(username)
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'пользователь с таким именем не найден'
            )

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)