import threading
import listen_sys
from flask import Flask, render_template
from defines import *

app = Flask(__name__)

map = {}

@app.route('/')
def index():
    return render_template('hello.html', num_cell_x=num_cell_x, num_cell_y=num_cell_y, map=map)
if __name__ == '__main__' :
    l = listen_sys.lis()
    
    threading.Thread(target=l.run, args=(map,)).start()
    app.run(debug=True)
