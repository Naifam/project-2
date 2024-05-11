from django.db import models 
   
# declare a new model with a name "GeeksModel" 
class GeeksModel(models.Model): 
  
    # fields of the model 
    UserName = models.CharField(max_length = 200) 
    Password = models.CharField(max_length = 200) 
  
   
    def __str__(self): 
        return self.title 