<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datei hochladen</title>
</head>
<body>
    <h1>Datei hochladen</h1>
    <form id="uploadForm" enctype="multipart/form-data">
        <input type="file" name="file" id="fileInput" required>
        <button type="submit">Hochladen</button>
    </form>
    <!-- from datbase in next time -->
    <button> <a href="upload/"> Klick Me </a></button>
    <video width="320" height="270" controls autoplay>
    <source src="/videos/d/d_subtitle.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video><video width="320" height="270" controls autoplay>
    <source src="/videos/d/d.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>


    <script>
        document.getElementById('uploadForm').addEventListener('submit', async function(event) {
            event.preventDefault(); // Prevent the default form submission

            const form = event.target;
            const formData = new FormData();
            const fileInput = document.getElementById('fileInput');
            formData.append('file', fileInput.files[0]);
            fetch('/uploadfile/')
            window.location.href = '/upload.php';
            try {
                const response = await fetch('/uploadfile/', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    console.log('Upload successful');
                    // Redirect to upload.php on successful upload
                    window.location.href = '/upload.php';
                } else {
                    console.error('Upload failed', response.status, response.statusText);
                    // Handle error
                    alert('Upload failed: ' + response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while uploading the file');
            }
        });
    </script>
</body>
</html>
