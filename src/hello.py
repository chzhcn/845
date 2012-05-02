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
    l = lis()    
    
    threading.Thread(target=l.run, global_map=map)
    app.run(debug=True)
