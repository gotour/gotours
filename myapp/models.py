from django.db import models
from django.utils import timezone

# Create your models here.
class Tourist(models.Model):
	fname=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	mobile=models.CharField(max_length=200)
	password=models.CharField(max_length=200)
	cpassword=models.CharField(max_length=200)

	def __str__(self):
		return self.fname
class Destinations(models.Model):
	from_to=models.CharField(max_length=200,default="")
	duration=models.CharField(max_length=200,default="")
	price=models.CharField(max_length=100,default="")
	from_s=models.CharField(max_length=200,default="")
	destinations_image=models.ImageField(upload_to='images/',default="")
	destinations_d_image1=models.ImageField(upload_to='images/',default="")
	destinations_d_image2=models.ImageField(upload_to='images/',default="")
	destinations_d_image3=models.ImageField(upload_to='images/',default="")


	def __str__(self):
		return self.from_to


class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)  
	remarks=models.TextField()

	def __str__(self):
		return self.name

class Book_trip(models.Model):
	destinations=models.ForeignKey(Destinations,on_delete=models.CASCADE)
	tourist=models.ForeignKey(Tourist,on_delete=models.CASCADE)
	trip_date=models.CharField(max_length=100)	
	adult=models.CharField(max_length=100)	

	def __str__(self):
		return self.tourist.fname+' ---'+self.destinations.from_to
	
		
class Transaction(models.Model):
    made_by = models.ForeignKey(Tourist, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
        