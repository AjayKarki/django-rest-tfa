from rest_framework import serializers
from rest_framework.settings import api_settings
from .serializer_fields import CustomRelatedField


class CustomModelSerializer(serializers.ModelSerializer):
	serializer_related_field = CustomRelatedField
	idx = serializers.CharField(read_only=True)

	class Meta:
		exclude = ("id", "modified_on", "is_obsolete", "deleted_at")
		extra_kwargs = {
			"created_on": {"read_only": True},
			"modified_on": {"read_only": True}
		}

