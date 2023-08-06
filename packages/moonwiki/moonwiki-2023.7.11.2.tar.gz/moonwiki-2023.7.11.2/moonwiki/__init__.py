class moonwiki(object): # A bit of support 4 2.0
	def __init__(self, wD):
		import os
		if str(wD) != wD:
			wD = "wiki"
		if not os.path.isdir(wD):
			raise TypeError(f"\"{wD}\" is not a directory")
		self.wD = wD
	def __repr__(self):
		return type(self).__name__ + "(" + self.wD + ")"
	def run(self, host, port):
		from http.server import HTTPServer, BaseHTTPRequestHandler
		import socket
		from configparser import ConfigParser as Inifile
		import os
		cfg = Inifile()
		if not os.path.isfile(os.path.join(self.wD, "settings.ini")):
			raise RuntimeError(f"Cannot read {os.path.join(self.wD, 'settings.ini')}")
		cfg.read(os.path.join(self.wD, "settings.ini"))
		if "moonwiki" not in cfg:
			raise NameError("Section \"moonwiki\" missing")
		reqKeys = ["name", "index", "temp"]
		for key in reqKeys:
			if key not in cfg["moonwiki"]:
				raise NameError(f"Key {key} at section \"moonwiki\" missing")
			if key == "temp":
				if not os.path.isfile(os.path.join(self.wD, cfg["moonwiki"][key] + ".html")):
					raise ValueError(f"{os.path.join(self.wD, cfg['moonwiki'][key] + '.html')} is non-existent nor is a file")
		def txt2Temp(txt):
			res = []
			with open(os.path.join(self.wD, cfg["moonwiki"][key] + ".html"), "r") as tempFilIO:
				for line in tempFilIO.read().split("\n"):
					resL = line
					if line.count("$$$$") > 1:
						raise SyntaxError(f"Line {tempFilIO.readlines().index(line) + 1} contains more than 1 `$$$$`")
					if bool(line.count("$$$$")):
						if line.strip() == "$$$$":
							line = line.replace("$$$$", "")
							resL = []
							for txtL in txt.split("\n"):
								resL.append(line + txtL)
							resL = "\n".join(resL)
					res.append(resL)
			return "\n".join(res)
		class moonwikiRequestHandler(BaseHTTPRequestHandler):
			def do_GET(req):
				if req.path == "/":
					req.send_response(200)
					req.send_header("Content-type", "text/html")
					req.end_headers()
					with open(os.path.join(self.wD, cfg["moonwiki"]["index"] + ".txt"), "rb") as indexIO:
						req.wfile.write(txt2Temp(indexIO.read().decode()).encode())
			def log_message(req, format, *args):
				pass
		serv = HTTPServer((host, port), moonwikiRequestHandler)
		print (f"moonwiki running @ http://{host}:{port}/ as \"{cfg['moonwiki']['name']}\"")
		serv.serve_forever()