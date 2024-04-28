from django.db import models
class GeeksModel(models.Model):

	title = models.CharField(max_length = 200)
	description = models.TextField()

	
	def __str__(self):
		return self.title

# Create your models here.

  
# declare a new model with a name "GeeksModel"
class GeeksModel(models.Model):
        # fields of the model
    title = models.CharField(max_length = 200)
    description = models.TextField()
  
        # renames the instances of the model
        # with their title name
    def __str__(self):
        return self.title
