from bbat.web.sanic import app, success, error
from bbat.date import time_to_str
import os

@app.route('/hi')
def hi(request):
    return success({}, "Hi")


@app.route("/api/upload", methods=['POST'])
def upload(request):
    if 'file' not in request.files:
        return error('No file uploaded')

    file = request.files['file'][0]
    file_name = file.name

    try:
        date = time_to_str("%Y-%m-%d")
        os.makedirs(f"static/uploads/{date}/", exist_ok=True)
        file_path = f'static/uploads/{date}/{file_name}'  # 保存文件的路径
        with open(file_path, 'wb') as f:
            f.write(file.body)
    except Exception as e:
        return error(f'Failed to upload file: {e}')

    return success({"path": file_path}, '上传成功')


app.run(debug=True)