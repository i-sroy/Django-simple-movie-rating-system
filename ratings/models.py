from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class MyUser(AbstractUser):
    email = models.EmailField('email_address',unique = True)
    password = models.CharField(max_length=128)
    user_id = models.AutoField(primary_key=True)
    REQUIRED_FIELDS = ['first_name','last_name','email','password']


class movies(models.Model):
    m_id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=500)
    lang = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class ratings(models.Model):
    r_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('MyUser',default=None,on_delete=models.SET_DEFAULT)
    rating = models.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    m_id = models.ForeignKey('movies', default=None, on_delete=models.SET_DEFAULT)




