import threading
from flask import Flask, render_template
import requests
import json

# ==============================
# جزء Flask
# ==============================
app = Flask(__name__)

API_URL = "https://sarfonlay.com/upadd3.php"
API_DATA = {"api": "fONoY+dZVo2MWqykBBU7aCjoRT5uU0NaLa16KEYPnvo="}

def fetch_currency_data():
    try:
        response = requests.post(API_URL, data=API_DATA, headers={"Content-Type": "application/x-www-form-urlencoded"})
        response.raise_for_status()
        jsonData = response.json()
        # إزالة الشرط المائل كما في الكود الأصلي
        raw_text = jsonData[0][0]["text"].replace("/", "").replace("\\", "")
        parsed_data = json.loads(raw_text)

        def Ms4(field):
            return parsed_data[0].get(field, "لا يوجد بيانات")

        return {
            "time": Ms4("T"),
            "aden": {
                "sar_buy": Ms4("A"),
                "sar_sell": Ms4("B"),
                "usd_buy": Ms4("C"),
                "usd_sell": Ms4("D")
            },
            "hadramout": {
                "sar_buy": Ms4("h1"),
                "sar_sell": Ms4("h2"),
                "usd_buy": Ms4("h3"),
                "usd_sell": Ms4("h4")
            },
            "sanaa": {
                "sar_buy": Ms4("s1"),
                "sar_sell": Ms4("s2"),
                "usd_buy": Ms4("s3"),
                "usd_sell": Ms4("s4")
            },
            "taiz": {
                "sar_buy": Ms4("t1"),
                "sar_sell": Ms4("t2"),
                "usd_buy": Ms4("t3"),
                "usd_sell": Ms4("t4")
            }
        }
    except Exception as e:
        print("❌ خطأ أثناء جلب البيانات:", e)
        return None

@app.route("/")
def index():
    data = fetch_currency_data()
    return render_template("index.html", data=data)

def run_flask():
    # تعطيل reloader لتجنب مشاكل الخيوط
    app.run(debug=True, host="0.0.0.0", use_reloader=False)

# ==============================
# جزء Kivy
# ==============================
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass
from android.runnable import run_on_ui_thread

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

class Wv(Widget):
    def __init__(self, **kwargs):
        super(Wv, self).__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setUseWideViewPort(True)          # يدعم meta viewport
        settings.setLoadWithOverviewMode(True)       # استخدام viewport
        settings.setSupportZoom(True)                # تمكين التكبير
        settings.setBuiltInZoomControls(True)        # عرض أدوات التكبير
        wvc = WebViewClient()
        webview.setWebViewClient(wvc)
        activity.setContentView(webview)
        # تأكد من كتابة عنوان URL بشكل صحيح مع الشرطتين //
        webview.loadUrl('http://127.0.0.1:5000')

class ServiceApp(App):
    def build(self):
        return Wv()

# ==============================
# التشغيل الرئيسي للتطبيق
# ==============================
if __name__ == "__main__":
    # تشغيل خادم Flask في خيط منفصل
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # تشغيل تطبيق Kivy
    ServiceApp().run()
