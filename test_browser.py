import urllib.request
try:
    resp = urllib.request.urlopen("http://localhost:8080/debate2.html")
    html = resp.read().decode('utf-8')
    if "<div" in html:
        print("HTML length:", len(html))
        print("Success loading debate2.html via HTTP")
except Exception as e:
    print("Error:", e)
