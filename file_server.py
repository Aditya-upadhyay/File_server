import encodings.ascii
from encodings import hex_codec
from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import url_for
from werkzeug import secure_filename
from werkzeug import SharedDataMiddleware
import glob, os, sys, subprocess
app = Flask(__name__)
UPLOAD_FOLDER = '/home/monster/Downloads/uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
try:
	check = subprocess.check_output('rm  static/shared', shell= True)	
except:
	pass
try:
	check = subprocess.check_output('ln -s ' + sys.argv[1] + ' static/shared', shell= True)	
except:
	pass
@app.route('/')
def hello_world():
	path = 'static/shared/'
	files = check(path + '/*')
	return render_template('front1.html', files=sorted(files), path=path)

@app.route('/dir', methods = ['GET'])
def dir():
	path = request.args.get('dir', '')
	if path.find('static/shared') != -1:
		back_path = path.split('/')
		back_path = '/'.join(back_path[0:len(back_path)-1])
		files = check(path + '/*')
		return render_template('front1.html', files=sorted(files), path=path , back_path = back_path)
	else:
		return render_template('404.html', path=path)
@app.route('/search', methods = ['GET'])
def get():
		search = request.args.get('search','')
		searchLower = search.lower()
		finding = []
		r= request.args.get('path','')
		if r.find('static/shared') != -1:
			matches = []
			for root, dirnames, filenames in os.walk(r):
				for filename in filenames:
					matches.append(os.path.join(root, filename))
			for match in matches:
				found = match.split('/')[-1].lower().find(searchLower)
				if found != -1:
					finding.append(match)
			return render_template("front.html",search = search,path=r, finding = finding, len = len(finding))
		else:
			return render_template("404.html", path = r)
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    path = request.args.get('path','')
    print path
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.stream.seek(0)
            return redirect('/dir?dir=static/shared/Downloads/uploaded')
	return  render_template("front1.html",path = path)

def check(path):
		name_tuple = []
		files  = glob.glob(path)
		for file in files:
			name_tuple.append((file, os.path.isdir(file)))
		return name_tuple	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(sys.argv[2]), debug=True)
	
