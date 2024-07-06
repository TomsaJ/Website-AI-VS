class HTML:
    def header():
        content = ''' <ul>
        <li><a href= "/"> Home </a></li>
        <li><a href= "/upload/"> Upload </a></li>
        </ul>  '''
        return content
    def sty():
        content = '''
        <style>
        body {
            margin: 0;
            padding: 0;
        }
        footer {
            position: fixed;
            bottom: 0;
            background-color: #4caf50;
            width: 100%;
            padding: 10px 0;
            text-align: center;
            color: white;
            font-size: 14px;
        }
        </style>
            '''
        return content
