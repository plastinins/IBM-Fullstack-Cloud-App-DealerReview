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
        return self.make.name + " " + \
               self.name + ", " + \
               "Year: " + str(self.year.year) + ", " + \
               "DealerID: " + str(self.dealer_id)

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, state, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.state = state
        # Dealer state (short)
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, dealer_id, id, name, purchase, review, make="", model="", year=None, purchase_date=None):
        self.make = make
        self.model = model
        self.year = year
        self.dealer_id = dealer_id
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        # Sentiment attribute will be determined by Watson NLU service. It could be positive, neutral, or negative
        self.sentiment = ""

    def __str__(self):
        return "Customer name: " + self.name
