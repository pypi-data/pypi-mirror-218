from bbat.web.flask import app
from bbat.db.mysql import Mysql
from bbat.config import Config
from flask import request, jsonify, render_template, redirect
import hashlib


@app.route('/hi')
def hi():
    return jsonify({})

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conf = Config('./setting.yaml')
dbconf = conf.get('db')
db = Mysql(**dbconf)


@app.route('/data', methods=['GET'])
def query_data():
    # 获取请求参数
    table_name = request.args.get('table', '')
    where_params = request.args.to_dict()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    if page < 1: page = 1
    # 构造 SQL 语句
    sql = f"SELECT * FROM {table_name} WHERE 1=1 "
    for key, value in where_params.items():
        if key not in ['table', 'page', 'page_size']:
            sql += f"AND {key} = '{value}' "
    offset = (page - 1) * page_size
    sql += f"LIMIT {offset}, {page_size}"

    data = db.query(sql)
    if len(data) == 0:
        return render_template('data.html', table=table_name, page=page, page_size=page_size)
    field = data[0].keys()
    return render_template("data.html", data=data, field=field, table=table_name, page=page, page_size=page_size)

@app.route('/register', methods=['GET', 'POST'])
def register():
    data = {}
    if request.method == 'GET':
        return render_template('register.html', data={})
    
    name = request.form['name']
    phone = request.form['phone']
    password = request.form['password']
    if not all([name, phone, password]):
        data['message'] = "注册信息不完整，请仔细填写"
        return render_template('register.html', data)
    pw_md5  = hashlib.md5(password.encode()).hexdigest()
    db.insert('user', [{
        'name': name,
        'phone': phone,
        'password': pw_md5,
    }])
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = {}
    if request.method == 'GET':
        return render_template('login.html', data={})
    
    phone = request.form['phone']
    password = request.form['password']

    pw_md5  = hashlib.md5(password.encode()).hexdigest()
    data = db.fetch('user', ('*',), f'phone="{phone}" AND password="{pw_md5}"')
    if len(data) == 0:
        data['message'] = "用户的手机号或者密码错误"
        return render_template('login.html', data=data)
    return redirect('/')


# run server
app.run(debug=True)