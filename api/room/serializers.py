# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from awesome_rooms.models import Room
from awesome_users.models import GameUser
from awesome_users.serializers import UserSerializer
from django.core.urlresolvers import reverse
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_url(self, obj):
        return reverse("room:detail", args=[obj.slug])


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)
    recaptcha = serializers.CharField(required=True, write_only=True, min_length=100)

    class Meta:
        model = GameUser
        fields = ['username', 'email', 'password', 'password2', 'recaptcha']

    def validate_username(self, username):
        if username.startswith('guest'):
            raise serializers.ValidationError('Nazwa użytkownika nie może zaczynać się od nazwy guest')
        return username

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = GameUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', '')
        }


class LoginGuestSerializer(serializers.Serializer):
    recaptcha = serializers.CharField(required=True, write_only=True, min_length=100)
