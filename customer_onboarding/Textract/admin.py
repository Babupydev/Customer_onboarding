# Admin page

from django.contrib import admin
from .models import CountryModel, DocumentSetModel, CustomerModel, CustomerDocumentModel
import json

@admin.register(CountryModel)
class CountryModelAdmin(admin.ModelAdmin):
    pass

@admin.register(DocumentSetModel)
class DocumentSetModelAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomerDocumentModel)
class CustomerDocumentModelAdmin(admin.ModelAdmin):
    list_display = ('customer', 'file', 'display_extracted_data')

    def display_extracted_data(self, obj):
        # Convert the extracted data dictionary to a JSON string for better display
        return json.dumps(obj.extracted_data, indent=4)
    display_extracted_data.short_description = 'Extracted Data'

# @admin.register(CustomerDocumentModel)
# class CustomerDocumentModelAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'file', 'display_extracted_data')

#     def display_extracted_data(self, obj):
#         # Parse the JSON string and format it into a simple list of key-value pairs
#         extracted_data = obj.extracted_data
#         formatted_data = '\n'.join([f"{key}: {value}" for key, value in extracted_data.items()])
#         return formatted_data
#     display_extracted_data.short_description = 'Extracted Data'


# admin.py

from django.contrib import admin
from .models import UploadedImage

admin.site.register(UploadedImage)
