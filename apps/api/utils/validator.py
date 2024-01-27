from rest_framework import serializers




class UserRegisterValidator:

    def password_validateor(self, validate_data):
        password1 = validate_data.get('password')
        password2 = validate_data.get('password2')
        if password1 != password2:
            raise serializers.ValidationError("password and password2 not matche", code=400)
        