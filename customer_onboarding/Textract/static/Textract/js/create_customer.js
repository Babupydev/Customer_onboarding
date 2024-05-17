const documentDescription = document.getElementById('documentDescription');
const uploadDescription = document.getElementById('uploadDescription');
const uploadSection = document.getElementById('uploadSection');
const documentUpload = document.getElementById('documentUpload');

document.querySelectorAll('input[name="documentOption"]').forEach((option) => {
    option.addEventListener('change', (event) => {
        const selectedOption = event.target.value;
        switch (selectedOption) {
            case 'idProof':
                documentDescription.innerText = 'Upload National ID';
                uploadDescription.innerText = 'Please upload a clear photo of both the front and back of your national identification (ID) card. You can upload the document by scanning with your camera.';
                break;
            case 'addressProof':
                documentDescription.innerText = 'Upload Address Proof';
                uploadDescription.innerText = 'Please upload a clear photo of both the front and back of your Address Proof. You can upload the document by scanning with your camera.';
                break;
            case 'incomeProof':
                documentDescription.innerText = 'Upload Proof of Income';
                uploadDescription.innerText = 'Please upload a clear photo of both the front and back of your Proof of Income. You can upload the document by scanning with your camera.';
                break;
            default:
                documentDescription.innerText = 'Please select a document type.';
                uploadDescription.innerText = '';
        }
        uploadSection.classList.remove('hidden');
    });
});

documentUpload.addEventListener('change', (event) => {
    const fileList = event.target.files;
    uploadDescription.innerHTML = ''; 
    for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i];
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('uploaded-image');
            const div = document.createElement('div');
            div.classList.add('uploaded-image-container');
            div.appendChild(img);
            uploadDescription.appendChild(div);
        };
        reader.readAsDataURL(file);
    }
});
// Function to get CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie contains the CSRF token
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.querySelector('.continue-button').addEventListener('click', () => {
    const formData = new FormData();
    const fileList = document.getElementById('documentUpload').files;
    for (let i = 0; i < fileList.length; i++) {
        formData.append('document', fileList[i]);
    }

    // Get CSRF token from the cookie
    const csrftoken = getCookie('csrftoken');

    fetch('/create-customer/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken 
        }
    })
    .then(response => {
        if (response.ok) {
            // Redirect to success page
            window.location.href = '/success/';
        } else {
            throw new Error('Error creating customer');
        }
    })
    .catch(error => {
        // Handle error
        console.error('Error:', error.message);
        
    });
});
