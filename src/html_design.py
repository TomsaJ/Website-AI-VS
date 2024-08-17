class Html:

    def foot_script():
        content = ''' </style>
    <script>
        function get_height() {
            return window.innerHeight;
        }

        function foot() {
            return get_height() - 46;
        }

        function setFooterPosition() {
            var footer = document.getElementById('myFooter');
            footer.style.marginTop = foot() + 'px';
        }

        window.onload = setFooterPosition;
        window.onresize = setFooterPosition; // Adjust footer position if window is resized
    </script> '''
        return content
    def header(logged_in):
        content = '''<ul>
        <li><a href="/">Home</a></li>
        <li><a href="/upload/">Upload</a></li>
        <li><a href="/me">My Videos</a></li>
        
    '''
        if logged_in:
            content += '''<li style="float: right"><a href="/logout">Logout</a></li>'''
        else:
            content += '''<li style="float: right"><a href="/login/e">Login</a></li>'''
    
        content += '''<li style="float: right"><a href="/about">About</a></li>
        </ul>'''
        return content
    
    def foot(user):
        if user is not None:
            content = f'''
        <footer id="myFooter">
        <p style="float:left; margin-left: 10px; color: white">Angemeldet als: {user}</p>
        <p style="float:right; margin-right: 10px; color: white"> Developer: <a href="https://github.com/LaRocc" style="color: white;">LaRocc</a> and <a href="https://github.com/TomsaJ" style="color: white;">TomsaJ</a></p>
        </footer>
        '''
        else:
            content = '''
        <footer id="myFooter">
        <p style="float:right; margin-right: 10px; color: white"> Developer: <a href="https://github.com/LaRocc" style="color: white;">LaRocc</a> and <a href="https://github.com/TomsaJ" style="color: white;">TomsaJ</a></p>
        </footer>
        '''
        return content

    def upload(lang):
        content = '''
        <div class="card">
        <span class="title">Video hochladen</span>
        <form class="form" id="uploadForm" action="/upload_duration/" method="post" enctype="multipart/form-data">
          <div class="group">
          <input  name="file" type="file" accept=".mp4" required="">
          <label for="name">Datei</label>
          </div>
      <div class="group">
        <select id="lang" name="lang" required>
            <option value="" disabled selected>Bitte auswählen ...</option>
            ''' + lang + '''
        </select>
          <label for="lang">Sprache</label>
          </div>
          <input type="hidden" name="user" value="{{ user }}">
          <br>
          <button type="submit">Hochladen</button>
        </form>
      </div>
        '''
        return content