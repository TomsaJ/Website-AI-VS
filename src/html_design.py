class HTML:
    def header(logged_in):
        content = '''<ul>
        <li><a href="/">Home</a></li>
        <li><a href="/upload/">Upload</a></li>
        <li><a href="/me">My Videos</a></li>
    '''
        if logged_in:
            content += '''<li style="float: right"><a href="/logout">Logout</a></li>'''
        else:
            content += '''<li style="float: right"><a href="/login">Login</a></li>'''
    
        content += '''</ul>'''
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
            background-color: darkolivegreen;
            width: 100%;
            padding: 10px 0;
            text-align: center;
            color: white;
            font-size: 14px;
        }
        </style>
            '''
        return content
    
    def foot():
        content = '''
        <footer id="myFooter">
        <p style="float:right; margin-right: 10px; color: white"> Developer: <a href="https://github.com/TomsaJ" style="color: white;">TomsaJ</a> and <a href="https://github.com/LaRocc" style="color: white;">LaRocc</a></p>
        </footer>
        '''
        return content
