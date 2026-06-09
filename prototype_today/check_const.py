import urllib.request, json

code = "typeof SKIN_TONES + ' ' + typeof HAIR_COLORS + ' ' + typeof EYE_COLORS + ' | ' + (typeof initCreation) + ' | ' + document.getElementById('skinColors')"
req = urllib.request.Request("http://127.0.0.1:10086/command",
    data=json.dumps({"action":"evaluate","args":{"code":code},"session":"fish-game"}).encode(),
    headers={"Content-Type":"application/json"})
resp = urllib.request.urlopen(req)
print(json.loads(resp.read()))
