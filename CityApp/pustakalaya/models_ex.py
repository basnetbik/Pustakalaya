from django.db import models

class Interest(models.Model):
    """docstring for Interest"""

    topic 		= models.CharField("keywords", max_length=30)

    def __str__(self):
        return self.topic

class User(models.Model):
    """docstring for user"""

    first_name 	= models.CharField("person's first name", max_length=30)
    last_name 	= models.CharField("person's last name", max_length=30)
    username	= models.CharField("username", max_length=30, unique=True, primary_key=True)
    password	= models.CharField("password", max_length=30)
    address		= models.CharField("person's address", max_length=30)
    email		= models.EmailField("person's email address", max_length=75)
    phone_number= models.CharField("person's phone number", max_length=30)
    lat 		= models.FloatField("Address latitude", blank=True)
    lon			= models.FloatField("Address longtitude", blank=True)
    current_worth= models.FloatField(default=0.)
    account_type= models.CharField("person's account type", default='inactive', max_length=30)
    #interest = models.ForeignKey(to=Interest)
    interest 	= models.ManyToManyField(to= Interest, verbose_name="interest", related_name='+')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Book(models.Model):
    """docstring for Book"""

    name 		= models.CharField("book name", max_length=30)
    author	 	= models.CharField("author name", max_length=30)
    description	= models.CharField("Book Description", max_length=100)
    value		= models.IntegerField()
    published_date = models.DateTimeField(blank=True)
    lend 		= models.OneToOneField(User, related_name=" books on lend")
    borrow 		= models.OneToOneField(User, related_name="books borrowed")
    # interest    = models.ForeignKey(to=Interest)
    # waiting_list = models.ForeignKey(to=User, to_field="username")
    waiting_list 	= models.ManyToManyField(User, related_name="wating users")
    interest = models.ManyToManyField(Interest, verbose_name="book tag")

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    timestamp = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField("Transaction Type", max_length=30)


class Log(models.Model):
    title = models.CharField("Log Heading", max_length=100)
    details = models.CharField("Log Details", max_length=100)
    date = models.DateTimeField(auto_now=True)



# Create your models here.
