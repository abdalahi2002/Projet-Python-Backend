# dans serializers.py
from rest_framework import serializers
from .models import Wilaya, Type_Sang, Donateur,Administrateur


class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = ['nom']
        

class Type_SangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Sang
        fields = ['nom']  
        
class TestDonateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donateur
        fields = ['id_d','test']

from datetime import datetime, timedelta
class Admin_DonateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donateur
        #exclude = ['a_fait_don']  # Exclure le champ pre_don du serializer
        fields = ['id_d','date_don','date_don_active','a_fait_don']
        
        
    # def update(self, instance, validated_data):
    #     # Si le don a été fait, mettre a_fait_don à True et mettre à jour les dates de donation
    #     if validated_data.get('a_fait_don', False):
    #         instance.a_fait_don = True
    #         instance.date_don = datetime.now().date()
    #         instance.date_don_active = datetime.now().date() + timedelta(days=6*30)
        
    #     instance.save()
    #     return instance
    
class Affiche_DonateurSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Donateur
        fields = ['id_d', 'first_name','last_name','tel','email','test','date_naissance','wilaya','a_fait_don','date_don','date_don_active','type_sang', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }       
class DonateurSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True,required=False)
    
    class Meta:
        model = Donateur
        fields = ['id_d', 'first_name','last_name','tel','email','date_naissance','wilaya','type_sang','a_fait_don', 'password','password_confirm']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            print(f"Password: {password}, Password Confirm: {password_confirm}")
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")

        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        validated_data.pop('password_confirm', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance

class AdminSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = Administrateur
        fields = ['id_A', 'first_name','last_name','tel','email', 'password','password_confirm']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            print(f"Password: {password}, Password Confirm: {password_confirm}")
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")

        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        validated_data.pop('password_confirm', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance
