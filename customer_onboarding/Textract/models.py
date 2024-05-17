# Model for Textract App

from django.db import models
from django.contrib.auth.models import User

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CountryModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DocumentSetModel(models.Model):
    name = models.CharField(max_length=100)
    countries = models.ManyToManyField(CountryModel)
    has_backside = models.BooleanField(default=False)
    ocr_labels = models.JSONField()

    def __str__(self):
        return self.name

class CustomerModel(models.Model):
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    nationality = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.surname}"

class CustomerDocumentModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    file = models.FileField(upload_to='customer_documents/')
    extracted_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.created_at}"
