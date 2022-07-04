from tokenize import blank_re
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.balance}"

 
class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Transactions(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    type_choices = ((IN, IN), (OUT, OUT))
    _type = models.CharField(choices=type_choices, max_length=3)
    amount = models.IntegerField()
    photo = models.ImageField(upload_to='photo', null=True, blank=True)
    comment = models.TextField()
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    


