'''
Yes, Django signals run in the same database transaction as the caller by default, So it means that if the caller's transaction is rolled back, any changes made by the signal receivers will also be rolled back providing consistency.
'''
#code example
from django.db import models, transaction  
from django.db.models.signals import post_save  
from django.dispatch import receiver  
from django.core.exceptions import ValidationError  


# The MainModel
class MainModel(models.Model):
    name = models.CharField(max_length=100)  


# The RelatedModel which is related to MainModel via a ForeignKey
class RelatedModel(models.Model):
    main = models.ForeignKey(MainModel, on_delete=models.CASCADE)  # ForeignKey
    value = models.IntegerField()  


    # Overriding the save method to add custom validation
    def save(self, *args, **kwargs):
        if self.value < 0:  #Checking for correct validation value
            raise ValidationError("Value must be non-negative")  
        super().save(*args, **kwargs)  


# Signal receiver for MainModel's post_save signal
@receiver(post_save, sender=MainModel)
def main_model_signal(sender, instance, created, **kwargs):
    print(f"MainModel signal: {'created' if created else 'updated'} - {instance.name}")


# Signal receiver for RelatedModel's post_save signal
@receiver(post_save, sender=RelatedModel)
def related_model_signal(sender, instance, created, **kwargs):
    print(f"RelatedModel signal: {'created' if created else 'updated'} - {instance.value}")


def test_transaction():
    try:
        with transaction.atomic():
            main = MainModel.objects.create(name="Test Main")
            print("MainModel created")
            related = RelatedModel.objects.create(main=main, value=-1)
            print("RelatedModel created")  #This line shouldnt get executed due to validation error
    except ValidationError:
        print("Transaction rolled back due to ValidationError")
    # Checking the number of MainModel and RelatedModel instances created
    print(f"MainModel count: {MainModel.objects.count()}")  
    print(f"RelatedModel count: {RelatedModel.objects.count()}")  




test_transaction()

