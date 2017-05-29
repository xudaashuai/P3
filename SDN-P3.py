# coding:utf-8
from flask import Flask
from flask import render_template, request
from flask_bootstrap import Bootstrap
import requests, json

app = Flask(__name__)
bootstrap = Bootstrap(app)
floodlight_ip = '172.29.27.144'
server_ip = '10.0.0.3'
url_clear = 'http://' + floodlight_ip + ':8080/wm/staticflowpusher/clear/all/json'
url_get = 'http://' + floodlight_ip + ':8080/wm/staticflowpusher/list/all/json'
url_set = 'http://' + floodlight_ip + ':8080/wm/staticflowpusher/json'


def getlist():
    k = requests.get(url_get, timeout=10)
    json.loads(k.text)


def add_filter(name, ip_proto, ip_src, port):
    tran = {
        'UDP': "0x11",
        'TCP': '0x06'
    }
    flow1 = {
        "switch": "00:00:00:00:00:00:00:01",
        "name": name,
        "eth_type": "0x0800",
        "priority": "32768",
        ip_proto + "_dst": str(port),
        "ipv4_src": ip_src,
        "ip_proto": tran[ip_proto],
        "ipv4_dst": server_ip,
        "active": "true",
        "actions": "output="
    }
    k = requests.post(url_set, data=json.dumps(flow1))
    return k.status_code


def remove_filter(name):
    k = requests.delete(url_set, data=json.dumps({'name': name}))
    return k.text


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        form = request.form
        print form
        if 'ip_proto' not in form:
            add_filter(form['flow_name'], form['ip_proto'], form['ip'], form['port'])
        else:
            remove_filter(form['flow_name'])
    return render_template('index.html', content=getlist())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
