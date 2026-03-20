import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class RestarHandler(BaseHTTPRequestHandler):
	def _send_json(self, data, status=200):
		body = json.dumps(data).encode("utf-8")
		self.send_response(status)
		self.send_header("Content-Type", "application/json; charset=utf-8")
		self.send_header("Content-Length", str(len(body)))
		self.end_headers()
		self.wfile.write(body)

	def do_GET(self):
		parsed = urlparse(self.path)

		if parsed.path != "/restar":
			self._send_json({"error": "Ruta no encontrada"}, status=404)
			return

		params = parse_qs(parsed.query)
		a_raw = params.get("a", [None])[0]
		b_raw = params.get("b", [None])[0]

		if a_raw is None or b_raw is None:
			self._send_json({"error": "Debes enviar los parametros a y b"}, status=400)
			return

		try:
			a = float(a_raw)
			b = float(b_raw)
		except ValueError:
			self._send_json({"error": "Los parametros a y b deben ser numericos"}, status=400)
			return

		self._send_json({"operacion": "resta", "a": a, "b": b, "resultado": a - b})


if __name__ == "__main__":
	server = HTTPServer(("0.0.0.0", 5001), RestarHandler)
	print("Servidor corriendo en http://0.0.0.0:5001")
	server.serve_forever()
