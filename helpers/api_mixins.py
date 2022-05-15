from rest_framework.response import Response
from rest_framework import status


class CustomAPIMixin:
	lookup_field = "uuid"

	def api_error_response(self, data, error_key='error', status=status.HTTP_400_BAD_REQUEST):
		error_data = data.copy()
		error_data['error_key'] = error_key
		return Response(error_data, status)

	def api_success_response(self, data, status=status.HTTP_200_OK):
		return Response(data, status)
 