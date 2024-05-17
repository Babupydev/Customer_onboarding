from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CountryModel, DocumentSetModel, CustomerModel, CustomerDocumentModel

def index(request):
    return render(request, "Textract/index.html")
# registation page
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful. Welcome, {}!'.format(username))
                return redirect('login')  
            else:
                messages.error(request, 'Failed to authenticate user. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = UserCreationForm()
    return render(request, 'Textract/register.html', {'form': form})

# Login page

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the dashboard
            return redirect('dashboard')
        else:
            # Authentication failed
            # Display an error message
            messages.error(request, 'Invalid username or password. Please try again.')
            # You may also want to clear the input fields or provide other feedback
            return render(request, 'Textract/login.html', {'username': username})
    return render(request, 'Textract/login.html')

# Store the upload images
from django.http import JsonResponse
from .models import UploadedImage

def upload_images(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        uploaded_images = request.FILES.getlist('images')
        # Process and store the images in the database
        for image in uploaded_images:
            UploadedImage.objects.create(image=image)
        return JsonResponse({'message': 'Images uploaded successfully'}, status=200)
    else:
        return JsonResponse({'error': 'No images uploaded'}, status=400)

# Sucess page

def success(request):
    return render(request, 'Textract/success.html')

#  Dashboard page
@login_required
def dashboard(request):
    return render(request, 'Textract/dashboard.html')

# Data extraction

import boto3

# Configure AWS credentials
AWS_ACCESS_KEY_ID = 'AKIAWXVGSAXIU5OVEIFI'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'us-east-2'  

# Initialize Textract client
textract_client = boto3.client('textract', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Function to extract text from an uploaded document using AWS Textract
def extract_text_from_document(file):
    # Read file content
    file_content = file.read()

    # Call DetectDocumentText API
    response = textract_client.detect_document_text(Document={'Bytes': file_content})

    # Extract text from response
    extracted_text = '\n'.join([block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE'])

    return extracted_text

from django.http import Http404

@login_required
def create_customer(request):
    if request.method == 'POST':
        # Extract text from uploaded document using AWS Textract
        extracted_text = extract_text_from_document(request.FILES['document'])
        
        # Split the extracted text into lines
        lines = extracted_text.split('\n')

        # Initialize variables to store extracted data
        surname = ''
        first_name = ''
        nationality_name = ''  # Store nationality name extracted from text

        # Parse each line to extract relevant information
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value = parts[1].strip()
                if key == 'surname':
                    surname = value
                elif key == 'first name':
                    first_name = value
                elif key == 'nationality':
                    nationality_name = value  # Store nationality name

        # Check if nationality name is not empty
        if nationality_name:
            # Attempt to get the CountryModel instance for the extracted nationality
            try:
                nationality = CountryModel.objects.get(name=nationality_name)
            except CountryModel.DoesNotExist:
                # Set a default country if extracted nationality is not found
                default_country_name = 'India'
                default_country, created = CountryModel.objects.get_or_create(name=default_country_name)
                nationality = default_country
        else:
            # Handle case where extracted nationality is empty
            # Set a default country
            default_country_name = 'India'
            default_country, created = CountryModel.objects.get_or_create(name=default_country_name)
            nationality = default_country

        # Create a new customer instance with extracted data
        customer = CustomerModel(
            surname=surname,
            first_name=first_name,
            nationality=nationality,  # Use the CountryModel instance
            gender='',  # Set gender to empty for now, update as needed
            created_by=request.user
        )
        customer.save()

        # Create a new CustomerDocumentModel instance to store the uploaded document and extracted data
        customer_document = CustomerDocumentModel(
            customer=customer,
            file=request.FILES['document'],
            extracted_data=extracted_text
        )
        customer_document.save()

        # Redirect to a success page or return a success message
        return redirect('success')
    else:
        # Render the form for uploading documents
        return render(request, 'Textract/create_customer.html')


# Customer details

@login_required
def customer_list(request):
    # Retrieve all customer documents
    customer_documents = CustomerDocumentModel.objects.all()
    return render(request, 'Textract/customer.html', {'customer_documents': customer_documents})


# View of customer document
from django.http import FileResponse
from django.conf import settings
from django.http import HttpResponseNotFound
import os

def view_customer_document(request, filename):
    document_path = os.path.join(settings.MEDIA_ROOT, 'customer_documents', filename)
    if os.path.exists(document_path):
        with open(document_path, 'rb') as document:
            response = FileResponse(document)
            return response
    else:
        # Handle the case where the document file does not exist
        return HttpResponseNotFound("Document not found")
