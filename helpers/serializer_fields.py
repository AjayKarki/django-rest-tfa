from rest_framework import serializers
from rest_framework.fields import get_attribute, is_simple_callable

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _


class DetailRelatedField(serializers.RelatedField):

	def __init__(self, model, **kwargs):
		if not kwargs.get("read_only"):
			kwargs["queryset"] = model.objects.all()

		self.lookup = kwargs.pop("lookup", None) or "uuid"

		try:
			self.representation = kwargs.pop("representation")
		except KeyError:
			raise Exception("Please supply representation.")

		super(DetailRelatedField, self).__init__(**kwargs)

	def to_internal_value(self, data):
		try:
			return self.queryset.get(**{self.lookup: data})
		except ObjectDoesNotExist:
			raise serializers.ValidationError("Object does not exist.")

	def to_representation(self, obj):
		return getattr(obj, self.representation)()

	def get_choices(self, cutoff=None):
		queryset = self.get_queryset()
		if queryset is None:
			return {}

		if cutoff is not None:
			queryset = queryset[:cutoff]

		# cast representation of item to str because
		# to representation could return a dict
		# and dicts can't be used as key on dicts because dicts are not hashable
		return {
			str(self.to_representation(item)): self.display_value(item)
			for item in queryset
		}


class UUIDOnlyObject:
	def __init__(self, uuid):
		self.uuid = uuid

	def __str__(self):
		return "%s" % self.uuid


class CustomRelatedField(serializers.PrimaryKeyRelatedField):
	default_error_messages = {
		'required': _('This field is required.'),
		'does_not_exist': _('Invalid uuid "{pk_value}" - object does not exist.'),
		'incorrect_type': _('Incorrect type. Expected uuid value, received {data_type}.'),
	}

	def get_attribute(self, instance):
		if self.use_pk_only_optimization() and self.source_attrs:
			try:
				instance = get_attribute(instance, self.source_attrs[:-1])
				value = instance.serializable_value(self.source_attrs[-1])
				if is_simple_callable(value):
					value = value().uuid
				else:
					value = getattr(instance, self.source_attrs[-1]).uuid
				return UUIDOnlyObject(uuid=value)
			except AttributeError:
					pass

	def to_representation(self, obj):
		return obj.uuid

	def to_internal_value(self, data):
		try:
			return self.queryset.get(uuid=data)
		except ObjectDoesNotExist:
			self.fail('does_not_exist', pk_value=data)
		except (TypeError, ValueError):
			self.fail('incorrect_type', data_type=type(data).__name__)
