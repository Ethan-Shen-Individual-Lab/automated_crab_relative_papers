from flask import Flask, jsonify, send_file, request
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path == "":
        return send_file('../index.html')
    return f"Path {path} not found", 404

@app.route('/api/start_crawler', methods=['POST'])
def start_crawler():
    try:
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['article_name', 'work_dir']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': '缺少必要参数'
            })
        
        # 在 Vercel 环境中启动爬虫
        # 注意：Vercel 是无状态的，不能直接运行长时间任务
        # 这里需要改为调用其他服务或使用队列系统
        
        return jsonify({
            'success': True,
            'message': '爬虫请求已接收'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

# Vercel 需要这个处理函数
def handler(request, context):
    return app(request) 