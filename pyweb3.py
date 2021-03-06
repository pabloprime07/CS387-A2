from http.server import HTTPServer, SimpleHTTPRequestHandler
import pgmeta
import dbexec

page ="""
<!DOCTYPE html>
<html>
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<head>
<style>
body {
  background-color: linen;
  margin: 10px; 
}
hr {
    display: block;
    width: 400px;
    margin-before: 0.5em;
    margin-after: 0.5em;
    margin-start: auto;
    margin-end: auto;
    overflow: hidden;
    border-style: inset;
    border-width: 1px;
}

.row {
}

.left {
   display: inline-block;
   text-align: right;
   width: 100px;
   padding: 10px;
}


.right {
   display: inline-block;
   padding: 10px;
}

</style>
</head>
<body>

<form action="/insert" method="post">
  <div>Tables:</div>
  <select name="table_select">
    <option value="student">student</option>
    <option value="university">university</option>
    <option value="teaches">teaches</option>
  </select>
  <input type="submit" value="Select table" >
</form>
<hr>
<form action="/insert" method="post">
  <div>Student:</div>
  <input type="hidden" name="table_name" value="student">
  <div class="row">
    <div class="left">id</div>
    <div class="right">
      <input type="text" name="id" value="2342">
    </div>
  </div>

  <div class="row">
    <div class="left">name</div>
    <div class="right">
      <input type="text" name="name">
    </div>
  </div>
    
  <div class="row">
    <div class="left">dept_name</div>
    <div class="right">
      <input type="text" name="dept_name">
    </div>
  </div>
    
  <div class="row">
    <div class="left">total_credit</div>
    <div class="right">
      <input type="text" name="total_credit">
    </div>
  </div>
 </div>
    
 <div class = "row">
   <div class="left"></div>
 <div class="right">
   <input type="submit" value="Add" >
 </div>
</form>

</body>

</html>
"""

class PGMetaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/meta":
            conn = dbexec.connect()
            meta = pgmeta.get_meta_data(conn)
            conn.close()
            s = pgmeta.to_graph(meta)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(page.format(repr(s)).encode())
        else:
            SimpleHTTPRequestHandler.do_GET(self)  # Fallback to built-in request handler

    def do_POST(self):
        if self.path == "/add":
            conn = dbexec.connect()
            meta = pgmeta.get_meta_data(conn)
            conn.close()
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(page.format(repr(s)).encode())
        
        SimpleHTTPRequestHandler.do_GET(self)        

httpd = HTTPServer( ('', 8000), PGMetaHandler)
httpd.serve_forever()
