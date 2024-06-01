<?php
require 'frontend/head.php';
head();
?>
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/page/css/style.css">

    <title>Datei hochladen</title>
</head>
<style>
    ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: darkolivegreen;
}

nav{
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: darkolivegreen;
}

li {
    float: left;
}

li a {
    display: block;
    color: white;
    text-align: center ;
    padding: 14px 16px;
    text-decoration: none;
}

li a:hover:not(.active) {
    background-color: white;
    color: #212121;
}

.active {
    background-color: #212121;
}

.active:hover{
    background-color: white;
    color: #212121;
}
body{
    /*background-color: #212121;*/
    margin: 0;
    padding: 0;
}
</style>
<body>
<ul>
    <li><a href= "/"> Home </a></li>
    <li><a href= "/upload/"> Upload </a></li>
</ul>

    <h1>Datei hochladen</h1>

    <!-- from datbase in next time -->
    <button> <a href="upload/"> Klick Me </a></button>
    <video width="320" height="270" controls >
    <source src="/videos/d/d_subtitle.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video><video width="320" height="270" controls >
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
