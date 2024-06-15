# Website-AI-VS
Die nachstehenden Kapitel: Beschreibung, Programmsprache und Voraussetzung wurd von dem Projekt [Projekt-KI-Untertitel](https://github.com/TomsaJ/Projekt-KI-Untertitel) übernommen.

## Beschreibung
Diese Anwendung erstellt einen Untertitel mit dem KI-Model [Whisper](https://github.com/openai/whisper), das von OpenAI entwickelt worden ist. Es wird zum einen eine Untertitel-Datei (srt) erstellt,
die anschließend mit einem Video (mp4) zusammen kombiniert wird. Außerdem wird eine Text-Datei (txt) erstellt, in der der gesamte gesprochenen Text gespeichert wird.

### Version
    Aktuelle Version: v0.5

### Programmsprache
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![PHP](https://img.shields.io/badge/php-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

## Voraussetzung
whisper-openai wird beim Programmstart automatisch installiert sowie movipy und ffmepg-python. Wichtig ist auch, dass ffmpeg installiert ist.

## Autor
Entwickelt wurde dieses Projekt von [LaRocc](https://www.github.com/LaRocc) und [TomsaJ](https://www.github.com/TomsaJ)

## Datenbank
Es wird die Datenbank <b>WS-AI-VS </b> benötigt. Diese Datenbank braucht einmal die Tabelle <b> videos </b> diese wird wie folgt erstellt.
<br>

<b> Datenbank: </b>
<br>
<code> CREATE DATABASE WS-AI-VS; </code>

<b>Tabelle:</b>
<br>
<code> CREATE TABLE `videos` (
`id` int(11) NOT NULL,
`pfad` varchar(255) NOT NULL,
`tags` varchar(255) NOT NULL)

ALTER TABLE `videos`
ADD PRIMARY KEY (`id`);

ALTER TABLE `videos`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;
</code>


