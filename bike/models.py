from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Customer(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    unique = models.CharField(max_length=8, unique=True, default=uuid4().hex[:8], verbose_name="ID")
    balance = models.FloatField(max_length=8,  default=0.0)

    def __str__(self):
        return self.account.__str__()


class Bike(models.Model):
    unique = models.CharField(max_length=12, unique=True, default=uuid4().hex[:12], verbose_name="ID")
    available = models.BooleanField(default=True)
    position_lat = models.FloatField(default=0.0)
    position_lng = models.FloatField(default=0.0)
    need_repair = models.BooleanField(default=False)

    def __str__(self):
        return self.unique

    def position(self):
        return f"{self.position_lat}, {self.position_lng}"


class Transaction(models.Model):
    unique = models.CharField(max_length=16, unique=True, default=uuid4().hex, verbose_name="ID")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    start_position_lat = models.FloatField(default=0.0)
    start_position_lng = models.FloatField(default=0.0)
    finish_position_lat = models.FloatField(default=0.0, null=True, blank=True)
    finish_position_lng = models.FloatField(default=0.0, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def calculate(self):
        return round(abs(self.finish_time - self.start_time).seconds / 600, 2)

    def start_position(self):
        return f"{self.start_position_lat}, {self.start_position_lng}"

    def finish_position(self):
        return f"{self.finish_position_lat}, {self.finish_position_lng}"

    def __str__(self):
        return self.unique


class Record(models.Model):
    unique = models.CharField(max_length=16, unique=True, default=uuid4().hex, verbose_name="ID")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return self.unique
