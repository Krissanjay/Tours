from rest_framework import serializers

from tourist_app.models import Tour


class TourSerializers(serializers.ModelSerializer):
    image1=serializers.ImageField(required=False)
    image2=serializers.ImageField(required=False)

    class Meta:
        model=Tour
        fields='__all__'