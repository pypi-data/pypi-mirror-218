from django.contrib.auth import get_user_model
from rest_framework import serializers


class EmailUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
        )

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'password']
        read_only_fields = ['id',]

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.get('email', None)
        if email is not None:
            validated_data['email'] = email.lower()
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
