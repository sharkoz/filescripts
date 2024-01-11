import datetime
from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

root = '/files'  # Replace with the path to your directory
scripts_directory = '/scripts'  # Replace with the path to your scripts directory

@app.route('/list_scripts')
def list_scripts():
    scripts = [file[:-3] for file in os.listdir(scripts_directory) if file.endswith('.py')]
    return scripts

scripts=list_scripts()

def format_size(size):
    power = 2**10
    n = 0
    size_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.1f} {size_labels[n]}"

@app.route('/')
def index():
    path = request.args.get('path', '')
    
    directory=root
    if path != '':
        path=os.path.normpath(path)
        if path == '\\':
            path = ''
        print(root)
        print(path)
        #directory = os.path.join(root, path)
        directory = root + path
        print(directory)
        if path.startswith('.'):
            return 'Invalid path'
    items = os.listdir(directory)
    folders = []
    files = []

    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append({
                'name': item,
                'size': '',
                'last_modified': ''
            })
        else:
            size = format_size(os.path.getsize(item_path))
            last_modified = os.path.getmtime(item_path)
            last_modified = datetime.datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M:%S')
            files.append({
                'name': item,
                'size': size,
                'last_modified': last_modified
            })

    return render_template('index.html', path=path, files=files, folders=folders, scripts=scripts)

  



@app.route('/run/<script>/')
def run(script):
    filename=request.args.get('path', '')
    script_path = os.path.join(scripts_directory, script + '.py')  # Remplacez par le nom de votre script
    file_path = os.path.join(root, filename)  # Remplacez par le chemin de votre dossier
    result = subprocess.run(['python', script_path, file_path], capture_output=True, text=True)
    return '<a href="javascript:history.back()">Go Back</a></br>Result :</br>' + result.stdout

if __name__ == '__main__':
    app.run(debug=True)
