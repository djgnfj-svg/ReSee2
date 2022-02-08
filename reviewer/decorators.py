
from functools import wraps
from django.http import Http404


def admin_only(function):
	@wraps(function)
	def wrap(request, *args, **kwargs):
		is_admin = request.user.is_admin
		if is_admin:
			return function(request, *args, **kwargs)
		else:
			raise Http404

	return wrap