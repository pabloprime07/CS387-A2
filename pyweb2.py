from http.server import HTTPServer, SimpleHTTPRequestHandler
import pgmeta
import dbexec


page ="""
<script src="view/dist/main.js"></script>

<canvas id="target-canvas"></canvas>
<script>
    var canvas = document.getElementById('target-canvas');
    var source = {};
    nomnoml.draw(canvas, source);
</script>
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
            SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        SimpleHTTPRequestHandler.do_GET(self)        

httpd = HTTPServer( ('', 8000), PGMetaHandler)
httpd.serve_forever()
