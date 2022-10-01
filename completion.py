import requests
import json
import jotoba

def payload(query, search_type, lang):
    return {"input":query,"search_type":str(search_type),"lang":lang,"radicals":[]}

def request(payload):
    headers = {"Content-Type": "application/json; charset=utf-8", "Accept":"application/json"}
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    resp = requests.post(jotoba.COMPLETIONS, data = data, headers = headers)
    return json.loads(resp.text)
