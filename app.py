from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import requests

# আপনার টেলিগ্রাম বট টোকেন এবং ইউজার আইডি
BOT_TOKEN = '8860365714:AAE1QxmOz4wx4oIz1jByNLhCmDYpNm-nU7A'
USER_ID = '6421195166'

class PostbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        
        if parsed_path.path == '/postback':
            query_params = urlparse.parse_qs(parsed_path.query)
            
            # Monetag-এর সঠিক ম্যাক্রো অনুযায়ী ডাটা রিড করা
            telegram_id = query_params.get('telegram_id', ['N/A'])[0]
            zone_id = query_params.get('zone_id', ['N/A'])[0]
            sub_zone_id = query_params.get('sub_zone_id', ['N/A'])[0]
            event_type = query_params.get('event_type', ['N/A'])[0]
            reward = query_params.get('reward', ['N/A'])[0]
            price = query_params.get('price', ['0.00'])[0]
            ymid = query_params.get('ymid', ['N/A'])[0]

            # টেলিগ্রাম মেসেজের আকর্ষণীয় এবং সুন্দর ফরম্যাট
            message = (
                "🎯 <b>New Monetag Notification!</b>\n"
                "────────────────────────\n"
                f"🔹 <b>Event Type:</b> <code>{event_type.upper()}</code>\n"
                f"👤 <b>Telegram ID:</b> <code>{telegram_id}</code>\n"
                f"🌐 <b>Zone ID:</b> <code>{zone_id}</code>\n"
                f"📂 <b>Sub Zone ID:</b> <code>{sub_zone_id}</code>\n"
                f"🎁 <b>Reward:</b> <b>{reward.upper()}</b>\n"
                f"💰 <b>Price:</b> <code>${price}</code>\n"
                f"🆔 <b>YMID:</b> <code>{ymid}</code>\n"
                "────────────────────────"
            )

            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': USER_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            try:
                response = requests.post(telegram_url, json=payload)
                if response.status_code == 200:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"OK - Message Sent")
                else:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"Failed to send telegram notification")
            except Exception as e:
                print("Error:", e)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Internal Server Error")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def run(server_class=HTTPServer, handler_class=PostbackHandler, port=8080):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    
    print("------------------------------------------")
    print(f" Server is running successfully!")
    print(f" Localhost Link: http://localhost:{port}/postback")
    print("------------------------------------------")
    
    httpd.serve_forever()

if __name__ == '__main__':
    run()
