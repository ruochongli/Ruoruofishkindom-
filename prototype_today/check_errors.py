import urllib.request, json

code = """(()=>{const errs=[];for(let i=0;i<Math.min(20,window.__errors?.length||0);i++)errs.push(window.__errors[i]);return errs.length?errs.join(String.fromCharCode(10)):'No errors';})()"""
req = urllib.request.Request("http://127.0.0.1:10086/command",
    data=json.dumps({"action":"evaluate","args":{"code":code},"session":"fish-game"}).encode(),
    headers={"Content-Type":"application/json"})
resp = urllib.request.urlopen(req)
print(json.loads(resp.read()))
