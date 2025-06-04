from django.contrib.auth.models import User
from django.core.validators import *
from django.db import models
from django.core.exceptions import *
from django.http import HttpResponse
from django.template.defaultfilters import title


class Kind(models.IntegerChoices):
    Buy=1,'Куплю'
    Sell=2,'Продам'
    Change=3,'Обмен'

class Rubric(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/app/rubric/{self.pk}/"


def validate_even(value):
    if value % 2 == 0:
        raise ValidationError(f"Число четное")

class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value):
        if value <= self.min_value or value >= self.max_value:
            raise ValidationError("Ваша цена вышла за диапазон")

    def deconstruct(self):
        return (
            f"{self.__class__.__module__}.{self.__class__.__name__}",
            (),
            {"min_value": self.min_value, "max_value": self.max_value},
        )

class Bb(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,verbose_name="Заголовок",validators=[RegexValidator("^.{4,}$")])
    price = models.FloatField(blank=True,null=True,verbose_name="Цена",validators=[MinMaxValueValidator(0,1000)])
    content = models.TextField(blank=True,null=True,verbose_name="Контент",validators=[MaxLengthValidator(100)])
    # published=models.DateTimeField(auto_now_add=True,verbose_name="Дата")
    published=models.DateTimeField(null=True,blank=True,verbose_name="Дата")

    def get_absolute_url(self):
        return f"/app/bb/{self.pk}/"

    def save(self,*args,**kwargs):
        if self.title=="Оружие":
            raise ValidationError('Нельзя оружие')
        super().save(*args,**kwargs)

    def delete(self,*args,**kwargs):
        if self.title=="Мяч":
            raise ValidationError('Нельзя удалять')
        super().delete(*args,**kwargs)


    def title_and_price(self):
        if self.price:
            return f"Title: {self.title}, Price: {self.price}$"
        else:
            return f"Title: {self.title}$"






    # KINDS=(
    #     ('Куплю-продам',
    #         ('b','Куплю'),
    #         ('s', 'Продам'),
    #      ),
    #     ('Обмен',
    #     ('c', 'Обменяю'),)
    # )
    # kind=models.CharField(max_length=1,default='s',choices=KINDS)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="Объявления"
        verbose_name="Объявление"
        ordering=["-published"]
        # index_together = ['title','published']
        # constraints = (
        #     models.CheckConstraint(
        #     check=models.Q(price__gt=0) & models.Q(price__lte=1000),
        #     name='bboard_price_check',
        #     )
        # )


class Passport(models.Model):
    country=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE)


class Spare(models.Model):
    name=models.CharField(max_length=30)

class Machine(models.Model):
    name=models.CharField(max_length=30)
    spares=models.ManyToManyField(Spare)


# validators=[]
# default="...",editable=True
# unique=True,unique_for_month='published'
# BooleanField
# DecimalField(max_digits=2,decimal_places=2)
# URLField
# DateTimeField
# TimeField
# DateField
# SlugField
# EmailField
# AutoField
# UUIDField
# ImageField
# FileField
# IntergerField
# PositiveIntegerField
class Quiz(models.Model):
    title=models.CharField(max_length=100)
    def str(self):
        return self.title

class Question(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    def str(self):
        return self.text

#dz-17
class Book(models.Model):

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    author = models.CharField(max_length=100, verbose_name="Автор")
    price = models.FloatField(blank=True, null=True, verbose_name="Цена", validators=[MinMaxValueValidator(0, 1000)])
    year = models.IntegerField( verbose_name="Год издания")