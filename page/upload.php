<!DOCTYPE html>
<html>
<head>
    <title>MP4 Datei hochladen</title>
    <style>
        #progressBar {
            width: 100%;
            background-color: #f3f3f3;
            margin-top: 10px;
        }

        #progressBarFill {
            width: 0%;
            height: 30px;
            background-color: #4caf50;
            text-align: center;
            line-height: 30px;
            color: white;
        }
    </style>
</head>
<body>
    <h1>MP4 Datei hochladen</h1>
    <form id="uploadForm" action="/upload_duration/" method="post" enctype="multipart/form-data">
        <input name="file" type="file" accept=".mp4">
        <input type="submit" value="Hochladen">
    </form>
</body>
</html>
