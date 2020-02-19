from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os

class Project(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  project_description = models.TextField(null=True,blank=True)
  task=models.CharField(max_length=900)
  date_posted = models.DateTimeField(default=timezone.now)
  configurations_varied=models.TextField(null=True,blank=True)	

  def __str__(self):
    return self.title
  def extension(self):
	  name, extension = os.path.splitext(self.file.name)
	  return extension

  def get_absolute_url(self):
	  return reverse('post-detail', kwargs={'pk': self.pk})

class DataSet(models.Model):
  project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='dataSetDetails')
  dataset_name=models.CharField(max_length=300,blank=False)
  dataset_url=models.URLField(max_length=1000,blank=True)
  dataset_file=models.FileField(null=True,blank=True,upload_to='Data_Set_Files')
  dataset_description= models.TextField(null=True,blank=True)


class DLModel(models.Model):
  project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='dlModelDetails')
  model_framework=models.CharField(max_length=100)
  model_url=models.URLField(max_length=1000,blank=True,null=True)
  model_file=models.FileField(null=True,blank=True,upload_to='DL_Model_Files')
  model_description= models.TextField(null=True,blank=True)

class PerformanceMetrics(models.Model):
  project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='performanceDetails')
  training_time=models.FloatField(null=True,blank=True)
  testing_time=models.FloatField(null=True,blank=True)
  accuracy_or_utilization=models.FloatField()
  metrics_description= models.TextField(null=True,blank=True)

