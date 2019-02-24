from flask import Flask,render_template,request,redirect,url_for
import os,datetime,base64
import qrcode
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        (shotname, extension) = os.path.splitext(f.filename)
        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        ex_name=shotname+'_'+datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')+extension
        s1 = base64.b64encode(ex_name .encode(encoding='utf-8'))
        urlname=str(s1,'utf-8')
        upload_path = os.path.join(basepath, 'static/img/',ex_name)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        content='http://zhada.emx6.com/image/'+urlname
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image()

        save_path='/static/qrcode/'+urlname+'.png'

        img.save(basepath+save_path)
        return redirect(url_for('index',qrcode=urlname))
    else:
        showcode=request.args.get('qrcode')
        if showcode:
            sourse = base64.b64decode(showcode)
            soursename = sourse.decode()
            return render_template('index.html', qrcode=showcode, sourse=soursename)
        else:
            return render_template('index.html')

# 图片访问地址：http://zhada.emx6.com/image/filename
@app.route('/image/<id>')
def image(id):
    decodestr = base64.b64decode(id)
    imageName=decodestr.decode()
    return render_template('image.html',id=imageName)

if __name__ == '__main__':
    app.run()
