from django.db import models
from django.utils import timezone
from django.conf import settings

class IntruderImage(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='intruder_images/%Y/%m/%d/')
	timestamp = models.DateTimeField(default=timezone.now)
	opened_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"Intruder Image - {self.timestamp}"

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	intruder_image = models.ForeignKey(IntruderImage, on_delete=models.SET_NULL, blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

# blog/models.py

class DoorStatus(models.Model):
	opened = models.BooleanField(default=False)
	opened_at = models.DateTimeField(blank=True, null=True)

	def open_door(self):
		self.opened = True
		self.opened_at = timezone.now()
		self.save()

	def close_door(self):
		self.opened = False
		self.save()
