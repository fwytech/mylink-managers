from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 飞书应用配置
FEISHU_APP_ID = os.getenv('FEISHU_APP_ID')
FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET')
BASE_ID = os.getenv('BASE_ID')
TABLE_ID = os.getenv('TABLE_ID')

# 飞书API相关函数
def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json().get("tenant_access_token")

def get_table_records(query_str=None):
    token = get_tenant_access_token()
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BASE_ID}/tables/{TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {}
    if query_str:
        params['filter'] = f'OR(Contains(内容简介,"{query_str}"),Contains(核心看点,"{query_str}"))'
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get("data", {}).get("items", [])
    
    # 处理每条记录
    for record in data:
        fields = record.get('fields', {})
        # 处理文章封面
        if '文章封面' in fields and fields['文章封面'] and isinstance(fields['文章封面'], list) and len(fields['文章封面']) > 0:
            cover_info = fields['文章封面'][0]
            if 'token' in cover_info:
                # 使用getAttachmentUrl获取附件的实际URL
                attachment_url = requests.get(
                    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BASE_ID}/tables/{TABLE_ID}/attachments/{cover_info['token']}/url",
                    headers={
                        "Authorization": f"Bearer {get_tenant_access_token()}",
                        "Content-Type": "application/json"
                    }
                ).json()
                fields['封面'] = attachment_url.get('data', {}).get('url', '/static/default-cover.jpg')
            else:
                fields['封面'] = '/static/default-cover.jpg'
        else:
            fields['封面'] = '/static/default-cover.jpg'
            
        # 处理文章链接
        if '链结' in fields and fields['链结']:
            # 飞书多维表格超链接字段的值格式为：{"text": "显示文本", "link": "URL地址"}
            link_data = fields['链结']
            if isinstance(link_data, dict) and 'link' in link_data:
                fields['文章标题链接'] = link_data['link']
            else:
                fields['文章标题链接'] = '#'
        else:
            fields['文章标题链接'] = '#'
            
        # 处理文章分类
        if '文章分类' in fields:
            fields['文章分类'] = fields['文章分类']
    
    return data

# 路由定义
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/articles')
def get_articles():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    records = get_table_records(search)
    
    if category:
        records = [r for r in records if category in r['fields'].get('分类', '')]
    
    # 分页处理
    start = (page - 1) * 10
    end = start + 10
    paginated_records = records[start:end]
    
    return jsonify({
        'articles': paginated_records,
        'total': len(records)
    })

if __name__ == '__main__':
    app.run(debug=True)