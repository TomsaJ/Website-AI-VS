<!DOCTYPE html>
<html>
<head>
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
