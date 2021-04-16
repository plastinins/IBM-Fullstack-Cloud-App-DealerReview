from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(null=False)
    # Car Types
    BUGGY = 'buggy'
    CABRIOLET = 'cabriolet'
    COUPE = 'coupe'
    HATCHBACK = 'hatchback'
    SUV = 'suv'
    LIMOUSINE = 'limousine'
    MICROVAN = 'microvan'
    MINIVAN = 'minivan'
    PICKUP = 'pickup'
    ROADSTER = 'roadster'
    SEDAN = 'sedan'
    WAGON = 'wagon'
  
    TYPE_CHOICES = [
        (BUGGY, 'buggy'),
        (CABRIOLET, 'cabriolet'),
        (COUPE, 'coupe'),
        (HATCHBACK, 'hatchback'),
        (SUV, 'suv'),
        (LIMOUSINE, 'limousine'),
        (MICROVAN, 'microvan'),
        (MINIVAN, 'minivan'),
        (PICKUP, 'pickup'),
        (ROADSTER, 'roadster'),
        (SEDAN, 'sedan'),
        (WAGON, 'wagon')
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    year = models.DateField()

    def __str__(self):
        return "Make: " + self.make.name + ", " + \
               "Model: " + self.name + ", " + \
               "Year: " + str(self.year.year) + ", " + \
               "DealerID: " + str(self.dealer_id)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
