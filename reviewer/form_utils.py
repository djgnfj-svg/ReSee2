

from accounts.models import MyUser, PayPlan
from reviewer.models import Categories


def category_guard(count, user_id):
	temp_user = PayPlan.objects.filter(subscribers_id = user_id).first()
	print(temp_user.name)
	if temp_user.name == "FREE" and count >= 3:
		return True
	elif temp_user.name == "PRIMIUM" and count >= 5:
		return True
	elif temp_user.name == "MAXIMUM" and count >= 10:
		return True
	return False