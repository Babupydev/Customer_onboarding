AWS.config.region = 'ap-south-1'; 
    var textract = new AWS.Textract();

    // Function to extract text from uploaded document using AWS Textract
    function extractTextFromDocument(file) {
        var params = {
            Document: {
                Bytes: file
            }
        };

        textract.detectDocumentText(params, function(err, data) {
            if (err) {
                console.error(err, err.stack);
                // Handle error
            } else {
                console.log(data); // Extracted text
                // Send extracted text to backend for further processing
            }
        });
    }

    // Event listener for document upload input
    document.getElementById('documentUpload').addEventListener('change', function(event) {
        var file = event.target.files[0];
        extractTextFromDocument(file);
    });