from django.db import models


# Create your models here.
class Hotel(models.Model):
    hotel_name = models.CharField(max_length=50)
    hotel_description = models.CharField(max_length=3000)
    hotel_address = models.CharField(max_length=150)
    hotel_region = models.CharField(max_length=20)
    hotel_town = models.CharField(max_length=20)
    hotel_tel = models.CharField(max_length=40)
    hotel_pic = models.CharField(max_length=100)
    hotel_px = models.FloatField()
    hotel_py = models.FloatField()

    def __str__(self):
        return self.hotel_name


class Attraction(models.Model):
    attraction_name = models.CharField(max_length=50)
    attraction_description = models.CharField(max_length=3000)
    attraction_open_time = models.CharField(max_length=150)
    attraction_address = models.CharField(max_length=80)
    attraction_region = models.CharField(max_length=20)
    attraction_town = models.CharField(max_length=20)
    attraction_tel = models.CharField(max_length=40)
    attraction_pic = models.CharField(max_length=100)
    attraction_px = models.FloatField()
    attraction_py = models.FloatField()

    def __str__(self):
        return self.attraction_name


class Food(models.Model):
    food_name = models.CharField(max_length=50)
    food_description = models.CharField(max_length=3000)
    food_open_time = models.CharField(max_length=100)
    food_address = models.CharField(max_length=150)
    food_region = models.CharField(max_length=20)
    food_town = models.CharField(max_length=20)
    food_tel = models.CharField(max_length=40)
    food_pic = models.CharField(max_length=100)
    food_px = models.FloatField()
    food_py = models.FloatField()

    def __str__(self):
        return self.food_name

