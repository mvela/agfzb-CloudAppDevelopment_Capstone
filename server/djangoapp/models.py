"""
Defines the models for the djangoapp app.
"""
from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    """
    Represents a car make.

    Attributes:
        id (AutoField): The primary key of the car make.
        name (CharField): The name of the car make.
        description (CharField): The description of the car make.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=30, default='None')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


class CarModel(models.Model):
    """
    Represents a car model.

    Attributes:
        id (AutoField): The primary key of the car model.
        dealerId (IntegerField): The ID of the dealer associated with the car model.
        name (CharField): The name of the car model.
        type (CharField): The type of the car model (e.g., sedan, SUV, wagon).
        year (PositiveIntegerField): The year of the car model.
        make (ForeignKey): The foreign key to the CarMake model.
    """

    id = models.AutoField(primary_key=True)
    dealerId = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=30, default='None')
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    type = models.CharField(
        null=False,
        max_length=5,
        choices=TYPE_CHOICES,
        default=SEDAN,
    )
    year = models.PositiveIntegerField(null=False)
    make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Type: " + self.type + "," + \
               "Year: " + str(self.year)

class DealerReview():
    """
    Represents the review of a dealer.
    """
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, 
                 car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

class CarDealer:
    """
    Represents a car dealer.
    """

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name
