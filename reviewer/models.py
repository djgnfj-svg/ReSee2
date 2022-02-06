from typing import Dict

from django.db import models
from django.contrib.gis.geoip2 import GeoIP2

from ReSee.settings import AUTH_USER_MODEL
from reviewer.models_utils import dict_filter, dict_slice

# Create your models here.
class TimeStampedModel(models.Model):
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		abstract = True

class EmailVerification(TimeStampedModel):
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
	key = models.CharField(max_length=100, null=True)
	verified = models.BooleanField(default=False)

class Categories(TimeStampedModel):
	name = models.CharField(max_length=20,null=True)
	creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
	category_count = models.IntegerField(default=0)

	def create_cate(self, request):
		self.category_count += 1
		self.creator_id = request.user.id
		self.name = "temp category" + self.category_count
		self.save()

	def cate_count_up(self):
		self.category_count += 1
		self.save()


class StudyList(TimeStampedModel):
	review_count = models.IntegerField(null=False, default=0)
	category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
	creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)    
	study_title = models.CharField(max_length=30)
	study_content = models.TextField()

	def review_count_up(self):
		self.review_count += 1
		self.save()

class Statistic(TimeStampedModel):
	class ApproachDevice(models.TextChoices):
		PC = "pc"
		MOBILE = "mobile"
		TABLET = "tablet"
	category = models.ForeignKey(Categories, on_delete=models.CASCADE)
	study = models.ForeignKey(StudyList, on_delete=models.CASCADE)
	ip = models.CharField(max_length=15)
	web_browser = models.CharField(max_length=50)
	device = models.CharField(max_length=6, choices=ApproachDevice.choices)
	device_os = models.CharField(max_length=30)
	country_code = models.CharField(max_length=2, default="XX")
	country_name = models.CharField(max_length=100, default="UNKNOWN")
	custom_parms = models.JSONField(null=True)

	def record(self, request, category:Categories, study:StudyList, params: Dict):
		self.category = category
		self.study = study
		self.ip = request.META["REMOTE_ADDR"]
		self.web_browser = request.user_agent.browser.family
		self.device = (
			self.ApproachDevice.MOBILE
			if request.user_agent.is_mobile
			else self.ApproachDevice.TABLET
			if request.user_agent.is_tablet
			else self.ApproachDevice.PC
		)
		self.device_os = request.user_agent.os.family
		t = TrackingParams.get_tracking_params(category.id)
		self.custom_parms = dict_slice(dict_filter(params, t), 5)
		
		try: 
			country = GeoIP2().country(self.ip)
			self.country_code = country.get("country_code", "XX")
			self.country_name = country.get("country_name", "UNKNOWN")
		except:
			pass
		self.save()

class TrackingParams(TimeStampedModel):
	category = models.ForeignKey(Categories, on_delete=models.CASCADE)
	params = models.CharField(max_length=20)

	@classmethod
	def get_tracking_params(cls, category_id):
			return cls.objects.filter(category_id=category_id).values_list("params", flat=True)