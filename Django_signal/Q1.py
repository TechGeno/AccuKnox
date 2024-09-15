'''
In Django signals are executed synchronously by default. This means that when a signal is sent, the sender waits for all receivers to complete their processing before continuing execution.
'''
# Example code for better understanding

from django.db import models
from django.db.models.signals import post_save  # Import the signal triggered after saving a model instance
from django.dispatch import receiver  # Import the decorator for connecting signals to functions
import time  # Import the time module to track execution time




class MyModel(models.Model):
    name = str(models.CharField(max_length=100))  
# Signal receiver function that gets executed after a 'MyModel' instance is saved
@receiver(post_save, sender=MyModel)  # Decorator to connect 'my_slow_callback' to the 'post_save' signal of 'MyModel'
def my_slow_callback(sender, instance, created, **kwargs):
    #Get start time of the signal receiver
    print(f"Signal receiver started at {time.time()}")
    time.sleep(5)  # A 5-second delay simulation
    # Get the end time of the signal receiver
    print(f"Signal receiver finished at {time.time()}")


def create_model_instance():
    # Time at instance creation
    print(f"Creating model instance at {time.time()}")
    obj = MyModel.objects.create(name="Test")  # New instance creation of 'MyModel' with name "Test"
    # Model instance is creation time.
    print(f"Model instance created at {time.time()}")


'''
Conclusion:
Here the signal post_save is connected to my_slow_callback, and within that function, a delay of 5 seconds is introduced using time.sleep(5),thus ,the above code clearly demonstrates that the signal is handled synchronously because the execution of the model instance creation is paused until the signal handler completes its task.
'''