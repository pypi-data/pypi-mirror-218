import json

__all__ = [
	'Pyaella_JSON_Renderer', 'Pyaella_XML_Renderer'
]


class Pyaella_JSON_Renderer(object):
	"""Renders a JSON formatted representation"""

	def __init__(self, info):
		pass

	def __call__(self, value, system):
		request = system.get('request')
		if request is not None:
			if not hasattr(request, 'response_content_type'):
				request.response_content_type = 'application/json'
		return json.dumps(value)


class Pyaella_XML_Renderer(object):
	"""Renders an XML formatted representation"""

	def __init__(self, info):
		pass

	def __call__(self, value, system):
		request = system.get('request')
		if request is not None:
			# if not hasattr(request, 'response_content_type'):
			request.response_content_type = 'text/xml'
			request.response_charset = 'UTF-8'
		return str(value)
