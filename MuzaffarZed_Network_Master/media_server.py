"""
MuzaffarZed 4K Cinema | Smart TV UPnP/DLNA & Web Streaming Engine
Muallif: MuzaffarZed
Standart: Mutlaq Mukammallik (Zero-Defect)
"""

import os
import sys
import socket
import struct
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import html

DEFAULT_MEDIA_DIR = r"C:\Users\MuzaffarZed\Videos"
SERVER_PORT = 8899
UPNP_UUID = "uuid:muzaffarzed-4k-cinema-978852003"


def get_local_ip():
    """Lokal tarmoqdagi IP manzilni aniqlash"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.16.1", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("192.168.1.1", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "192.168.16.187"


class DLNAHTTPHandler(BaseHTTPRequestHandler):
    """HTTP 4K Range Streaming + UPnP DLNA Controller"""
    media_dir = DEFAULT_MEDIA_DIR
    local_ip = "192.168.16.187"

    def log_message(self, format, *args):
        # pythonw muhitida sys.stderr None bo'lgani sababli xatolikni oldini oladi
        pass

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', 'Range, Content-Type, SOAPAction')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_POST(self):
        """UPnP SOAP ContentDirectory Browse Action Handling"""
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/ctl/ContentDir":
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len).decode('utf-8', errors='ignore')
            
            # Smart TV Browse request
            didl_xml = self.generate_didl_lite()
            soap_resp = (
                '<?xml version="1.0" encoding="utf-8"?>\r\n'
                '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
                '<s:Body>'
                '<u:BrowseResponse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">'
                f'<Result>{html.escape(didl_xml)}</Result>'
                f'<NumberReturned>{self.get_item_count()}</NumberReturned>'
                f'<TotalMatches>{self.get_item_count()}</TotalMatches>'
                '<UpdateID>1</UpdateID>'
                '</u:BrowseResponse>'
                '</s:Body>'
                '</s:Envelope>'
            ).encode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type', 'text/xml; charset="utf-8"')
            self.send_header('Content-Length', str(len(soap_resp)))
            self.send_header('EXT', '')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(soap_resp)
            return
        elif parsed.path == "/ctl/ConnMgr":
            soap_resp = (
                '<?xml version="1.0" encoding="utf-8"?>\r\n'
                '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
                '<s:Body>'
                '<u:GetCurrentConnectionIDsResponse xmlns:u="urn:schemas-upnp-org:service:ConnectionManager:1">'
                '<ConnectionIDs>0</ConnectionIDs>'
                '</u:GetCurrentConnectionIDsResponse>'
                '</s:Body>'
                '</s:Envelope>'
            ).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml; charset="utf-8"')
            self.send_header('Content-Length', str(len(soap_resp)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(soap_resp)
            return

        self.send_error(404, "Not Found")

    def generate_didl_lite(self):
        """DIDL-Lite XML for Smart TV remote browsing"""
        items = []
        base_url = f"http://{self.local_ip}:{SERVER_PORT}"
        idx = 1
        if os.path.exists(self.media_dir):
            for root, _, files in os.walk(self.media_dir):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in ['.mp4', '.mkv', '.avi', '.mov', '.ts', '.m4v']:
                        full_p = os.path.join(root, f)
                        rel_p = os.path.relpath(full_p, self.media_dir)
                        enc_url = f"{base_url}/{urllib.parse.quote(rel_p.replace(os.sep, '/'))}"
                        size = os.path.getsize(full_p)
                        mime = "video/mp4" if ext == ".mp4" else "video/x-matroska"
                        title = html.escape(f)

                        # Subtitr tekshiruvi (.srt)
                        srt_p = os.path.splitext(full_p)[0] + ".srt"
                        sub_xml = ""
                        if os.path.exists(srt_p):
                            srt_rel = os.path.relpath(srt_p, self.media_dir)
                            srt_url = f"{base_url}/{urllib.parse.quote(srt_rel.replace(os.sep, '/'))}"
                            sub_xml = (
                                f'<res protocolInfo="http-get:*:text/srt:*">{srt_url}</res>'
                                f'<sec:CaptionInfo xmlns:sec="http://www.sec.co.kr/" sec:type="srt">{srt_url}</sec:CaptionInfo>'
                            )

                        item_xml = (
                            f'<item id="{idx}" parentID="0" restricted="1">'
                            f'<dc:title>{title}</dc:title>'
                            f'<upnp:class>object.item.videoItem.movie</upnp:class>'
                            f'<res size="{size}" protocolInfo="http-get:*:{mime}:DLNA.ORG_OP=01;DLNA.ORG_CI=0;DLNA.ORG_FLAGS=01700000000000000000000000000000">{enc_url}</res>'
                            f'{sub_xml}'
                            f'</item>'
                        )
                        items.append(item_xml)
                        idx += 1
        didl = (
            '<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/">'
            + ''.join(items) +
            '</DIDL-Lite>'
        )
        return didl

    def get_item_count(self):
        cnt = 0
        if os.path.exists(self.media_dir):
            for root, _, files in os.walk(self.media_dir):
                for f in files:
                    if os.path.splitext(f)[1].lower() in ['.mp4', '.mkv', '.avi', '.mov', '.ts', '.m4v']:
                        cnt += 1
        return cnt

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # UPnP Device Description
        if path == "/description.xml":
            xml = f"""<?xml version="1.0" encoding="utf-8"?>
<root xmlns="urn:schemas-upnp-org:device-1-0">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>
  <device>
    <deviceType>urn:schemas-upnp-org:device:MediaServer:1</deviceType>
    <friendlyName>MuzaffarZed 4K Cinema</friendlyName>
    <manufacturer>MuzaffarZed</manufacturer>
    <modelDescription>MuzaffarZed 4K Ultra-HD Cinema Streamer</modelDescription>
    <modelName>MuzaffarZed MediaServer 4K</modelName>
    <modelNumber>2.0</modelNumber>
    <UDN>{UPNP_UUID}</UDN>
    <serviceList>
      <service>
        <serviceType>urn:schemas-upnp-org:service:ContentDirectory:1</serviceType>
        <serviceId>urn:upnp-org:serviceId:ContentDirectory</serviceId>
        <SCPDURL>/ContentDir.xml</SCPDURL>
        <controlURL>/ctl/ContentDir</controlURL>
        <eventSubURL>/evt/ContentDir</eventSubURL>
      </service>
      <service>
        <serviceType>urn:schemas-upnp-org:service:ConnectionManager:1</serviceType>
        <serviceId>urn:upnp-org:serviceId:ConnectionManager</serviceId>
        <SCPDURL>/ConnMgr.xml</SCPDURL>
        <controlURL>/ctl/ConnMgr</controlURL>
        <eventSubURL>/evt/ConnMgr</eventSubURL>
      </service>
    </serviceList>
  </device>
</root>""".strip().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml; charset="utf-8"')
            self.send_header('Content-Length', str(len(xml)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(xml)
            return

        elif path == "/ContentDir.xml":
            scpd = """<?xml version="1.0" encoding="utf-8"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion><major>1</major><minor>0</minor></specVersion>
  <actionList>
    <action>
      <name>Browse</name>
      <argumentList>
        <argument><name>ObjectID</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_ObjectID</relatedStateVariable></argument>
        <argument><name>BrowseFlag</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_BrowseFlag</relatedStateVariable></argument>
        <argument><name>Filter</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_Filter</relatedStateVariable></argument>
        <argument><name>StartingIndex</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_Index</relatedStateVariable></argument>
        <argument><name>RequestedCount</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable></argument>
        <argument><name>SortCriteria</name><direction>in</direction><relatedStateVariable>A_ARG_TYPE_SortCriteria</relatedStateVariable></argument>
        <argument><name>Result</name><direction>out</direction><relatedStateVariable>A_ARG_TYPE_Result</relatedStateVariable></argument>
        <argument><name>NumberReturned</name><direction>out</direction><relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable></argument>
        <argument><name>TotalMatches</name><direction>out</direction><relatedStateVariable>A_ARG_TYPE_Count</relatedStateVariable></argument>
        <argument><name>UpdateID</name><direction>out</direction><relatedStateVariable>A_ARG_TYPE_UpdateID</relatedStateVariable></argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_ObjectID</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_Result</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_BrowseFlag</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_Filter</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_SortCriteria</name><dataType>string</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_Index</name><dataType>ui4</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_Count</name><dataType>ui4</dataType></stateVariable>
    <stateVariable sendEvents="no"><name>A_ARG_TYPE_UpdateID</name><dataType>ui4</dataType></stateVariable>
  </serviceStateTable>
</scpd>""".encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml; charset="utf-8"')
            self.send_header('Content-Length', str(len(scpd)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(scpd)
            return

        elif path == "/ConnMgr.xml":
            scpd = """<?xml version="1.0" encoding="utf-8"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion><major>1</major><minor>0</minor></specVersion>
  <actionList>
    <action>
      <name>GetCurrentConnectionIDs</name>
      <argumentList>
        <argument><name>ConnectionIDs</name><direction>out</direction><relatedStateVariable>CurrentConnectionIDs</relatedStateVariable></argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="no"><name>CurrentConnectionIDs</name><dataType>string</dataType></stateVariable>
  </serviceStateTable>
</scpd>""".encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml; charset="utf-8"')
            self.send_header('Content-Length', str(len(scpd)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(scpd)
            return

        # Web portal
        if path == "/" or path == "/index.html":
            self.serve_portal()
            return

        # Serve video files
        decoded_path = urllib.parse.unquote(path.lstrip("/"))
        file_path = os.path.join(self.media_dir, decoded_path)

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_error(404, "Fayl topilmadi")
            return

        self.stream_video_file(file_path)

    def serve_portal(self):
        """Smart TV va Mobil Brauzer uchun Shaffof Dark Portal"""
        videos = []
        if os.path.exists(self.media_dir):
            for root, _, files in os.walk(self.media_dir):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in ['.mp4', '.mkv', '.avi', '.mov', '.ts', '.m4v']:
                        full_p = os.path.join(root, f)
                        rel_p = os.path.relpath(full_p, self.media_dir)
                        size_mb = os.path.getsize(full_p) / (1024 * 1024)
                        videos.append({
                            "name": f,
                            "path": urllib.parse.quote(rel_p.replace(os.sep, '/')),
                            "size": f"{size_mb:.1f} MB"
                        })

        cards_html = ""
        for v in videos:
            cards_html += f"""
            <div class="card" onclick="playVideo('{v['path']}', '{v['name']}')">
                <div class="icon">🎬</div>
                <div class="info">
                    <div class="title">{v['name']}</div>
                    <div class="badge">4K ULTRA HD • {v['size']}</div>
                </div>
            </div>
            """

        if not cards_html:
            cards_html = '<div class="empty">📂 Hozircha videolaringiz mavjud emas. Fayllarni "Videolar" papkasiga joylang.</div>'

        html_content = f"""<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MuzaffarZed 4K Cinema | Smart TV Portal</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #0a0d14; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; padding: 25px; }}
    .header {{ display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid #1e2638; }}
    .logo {{ font-size: 26px; font-weight: 800; background: linear-gradient(135deg, #00e676, #00b0ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .tv-badge {{ background: #1e293b; padding: 8px 18px; border-radius: 20px; border: 1px solid #334155; font-size: 14px; color: #94a3b8; }}
    .player-box {{ margin: 25px 0; background: #000; border-radius: 16px; overflow: hidden; display: none; box-shadow: 0 10px 40px rgba(0, 230, 118, 0.2); }}
    video {{ width: 100%; max-height: 75vh; display: block; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; margin-top: 25px; }}
    .card {{ background: #111726; border: 1px solid #1e293b; border-radius: 14px; padding: 18px; cursor: pointer; transition: 0.2s; display: flex; align-items: center; gap: 15px; }}
    .card:hover, .card:focus {{ transform: translateY(-3px); border-color: #00e676; background: #162035; box-shadow: 0 6px 25px rgba(0, 230, 118, 0.25); }}
    .icon {{ font-size: 32px; }}
    .title {{ font-size: 15px; font-weight: 600; line-height: 1.4; color: #f1f5f9; word-break: break-all; }}
    .badge {{ font-size: 12px; color: #00e676; margin-top: 5px; font-weight: 500; }}
    .empty {{ text-align: center; color: #64748b; padding: 50px; font-size: 18px; width: 100%; grid-column: 1 / -1; }}
    .footer {{ margin-top: 40px; text-align: center; font-size: 13px; color: #475569; }}
</style>
</head>
<body>
    <div class="header">
        <div class="logo">⚡ MuzaffarZed 4K Cinema</div>
        <div class="tv-badge">📺 Smart TV & Mobil: http://{self.local_ip}:{SERVER_PORT} (DLNA Faol)</div>
    </div>

    <div class="player-box" id="playerBox">
        <video id="tvVideo" controls autoplay playsinline></video>
    </div>

    <div class="grid">
        {cards_html}
    </div>

    <div class="footer">Dasturchi: MuzaffarZed • Smart TV 4K Ultra-HD DLNA Engine</div>

    <script>
        function playVideo(url, name) {{
            var box = document.getElementById('playerBox');
            var v = document.getElementById('tvVideo');
            box.style.display = 'block';
            v.src = '/' + url;
            v.play();
            box.scrollIntoView({{ behavior: 'smooth' }});
        }}
    </script>
</body>
</html>
"""
        body = html_content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def stream_video_file(self, file_path):
        """Televizor va pleyerlar uchun HTTP 206 Partial Content (Range) oqimi"""
        file_size = os.path.getsize(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "video/mp4"

        range_header = self.headers.get('Range')

        if not range_header:
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(file_size))
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('transferMode.dlna.org', 'Streaming')
            self.send_header('contentFeatures.dlna.org', 'DLNA.ORG_OP=01;DLNA.ORG_CI=0;DLNA.ORG_FLAGS=01700000000000000000000000000000')
            self.send_cors_headers()
            self.end_headers()
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(64 * 1024)
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except Exception:
                        break
            return

        # Parse Range: bytes=start-end
        bytes_range = range_header.strip().split('=')[-1]
        start_str, end_str = bytes_range.split('-')
        start = int(start_str) if start_str else 0
        end = int(end_str) if end_str else file_size - 1

        if start >= file_size:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{file_size}')
            self.end_headers()
            return

        chunk_size = end - start + 1

        self.send_response(206)
        self.send_header('Content-Type', mime_type)
        self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
        self.send_header('Content-Length', str(chunk_size))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('transferMode.dlna.org', 'Streaming')
        self.send_header('contentFeatures.dlna.org', 'DLNA.ORG_OP=01;DLNA.ORG_CI=0;DLNA.ORG_FLAGS=01700000000000000000000000000000')
        self.send_cors_headers()
        self.end_headers()

        with open(file_path, 'rb') as f:
            f.seek(start)
            bytes_left = chunk_size
            while bytes_left > 0:
                read_len = min(64 * 1024, bytes_left)
                chunk = f.read(read_len)
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                    bytes_left -= len(chunk)
                except Exception:
                    break


class SSDPResponder(threading.Thread):
    """Smart TV lar uchun UPnP/DLNA SSDP Discovery Broadcaster"""
    def __init__(self, local_ip, port=SERVER_PORT):
        super().__init__(daemon=True)
        self.local_ip = local_ip
        self.port = port
        self.running = True

    def run(self):
        MCAST_GRP = '239.255.255.250'
        MCAST_PORT = 1900
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', MCAST_PORT))
            mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.settimeout(2.0)
        except Exception:
            return

        while self.running:
            try:
                data, addr = sock.recvfrom(2048)
                msg = data.decode('utf-8', errors='ignore')
                if "M-SEARCH" in msg:
                    # Respond to TV discovery
                    resp = (
                        "HTTP/1.1 200 OK\r\n"
                        f"LOCATION: http://{self.local_ip}:{self.port}/description.xml\r\n"
                        "CACHE-CONTROL: max-age=1800\r\n"
                        "EXT:\r\n"
                        "SERVER: Windows/10.0 UPnP/1.0 MuzaffarZed-DLNA/2.0\r\n"
                        "ST: urn:schemas-upnp-org:device:MediaServer:1\r\n"
                        f"USN: {UPNP_UUID}::urn:schemas-upnp-org:device:MediaServer:1\r\n"
                        "\r\n"
                    ).encode('utf-8')
                    sock.sendto(resp, addr)
            except socket.timeout:
                pass
            except Exception:
                pass


class MediaServerEngine:
    """4K Cinema Server Engine (DLNA + HTTP)"""
    def __init__(self, media_dir=DEFAULT_MEDIA_DIR, port=SERVER_PORT):
        self.media_dir = media_dir
        self.port = port
        self.local_ip = get_local_ip()
        self.httpd = None
        self.thread = None
        self.ssdp = None
        self.running = False

    def start(self):
        if self.running:
            return True, f"Server allaqachon ishlab turibdi: http://{self.local_ip}:{self.port}"
        try:
            DLNAHTTPHandler.media_dir = self.media_dir
            DLNAHTTPHandler.local_ip = self.local_ip
            HTTPServer.allow_reuse_address = True
            self.httpd = HTTPServer(('0.0.0.0', self.port), DLNAHTTPHandler)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()

            # Start SSDP Broadcaster for Smart TVs
            self.ssdp = SSDPResponder(self.local_ip, self.port)
            self.ssdp.start()

            self.running = True
            return True, f"4K Cinema Server faol (DLNA + Web): http://{self.local_ip}:{self.port}"
        except Exception as e:
            return False, f"Serverni ishga tushirishda xatolik: {e}"

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.running = False
        if self.ssdp:
            self.ssdp.running = False
        return True, "Server to'xtatildi"


if __name__ == '__main__':
    srv = MediaServerEngine()
    ok, msg = srv.start()
    print(msg)
    import time
    while True:
        time.sleep(1)
