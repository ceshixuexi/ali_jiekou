import json

from base.base_analyze import analyze_file


import requests
import json
request_data_list=analyze_file('../data/ali_request.json')

print(request_data_list)
# url = 'https://aliae.apexglobe.info/aliapi/webapi/OrderNotify/AliOrderNotify'
data=dict()
# data['sign']='HyixAMNtSXEw4260t43RospI/xiDQldy2Xlou+KSJC7WYI1VkaFoOD7Z4TnM+nBMoT30a5QY2x0vOFQ+S9kCUWGkr92CzFvaqPXoMadwu0iFXq3FdThJLcqONvTyo/kqChcgdDicoybevYw8S3NefWLWqy1B4k6JM+XlipyVtt4DrnktJsEdZZBVAGELQ+BXU/kb43samIjcVL3FXZdH4oTDhYtF8G38YI+UCmaGo8RhVj0LYZVfGtwponUDZQZYAwPu+Im9HaXiwuJ6fv5c+dxiIX1ZhBebewG11lkp+QBI0CwrVI2txPJlHdpxkUxsFds6T+0278T01o143tKAfQ=='
# data['appkey']='962333'

# s='{\"aliOrderNo\":\"1531471592262\",\"notifyInfoCode\":\"DECLARATION_FILES_NOTIFY\",\"notifyEventTime\":\"2021-07-20T13:13:02+0800\",\"content\":[{\"fileType\":\"TAX_FILE\",\"fileName\":\"taxFileForDeclaration\",\"fillUrl\":\"https://ae01.alicdn.com/kf/UT8ot5bXbtaXXbyTXbXg.xml\",\"remark\":\"\"},{\"fileType\":\"TAX_FILE\",\"fileName\":\"taxFileForDeclaration\",\"fillUrl\":\"https://ae01.alicdn.com/kf/UT8ot5bXbtaXXbyTXbXg.xml\",\"remark\":\"\"}]}'
# data['request']=s
for i in request_data_list:
    url=i['url']
    data['sign']=i['sign']
    data['appkey'] = i['appkey']
    data['request'] = json.dumps(i['request'])
    print(data)
    response = requests.post(url=url,json=data)
    print(response.json())