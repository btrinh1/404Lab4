import sqlite3
from flask import Flask, request, url_for, redirect

conn = None
app= Flask(__name__)

def db_connect():
	global conn
	if conn is None:
		conn = sqlite3.connect('lab4.db', check_same_thread=False)
		conn.row_factory = sqlite3.Row
	return conn

def query_db(query, args=(), one=False):
	cur = db_connect().cursor()
	cur.execute(query, args)
	r = cur.fetchall()
	cur.close()
	return (r[0] if r else None) if one else r
def get_tasks():
    return query_db("SELECT * FROM tasks")

def insert_task(category, priority, description):
	query_db('INSERT INTO tasks values(?, ?, ?)', (category, priority, description))
	db_connect().commit()

@app.route('/', methods=['GET'])
def index():
    return '''<p>Click here -> <a href="/task">Task</a>.</p>%s''' % (get_footer())

@app.route('/task', methods=['GET', 'POST'])
def tasks():
    tasks = get_tasks()
    data = '%s' % get_header(request.method)
    data += '''<table border = "1" style="width:50%">
    		   <th>Category</th>
    		   <th>Priority</th> 
               <th>Description</th>
  			   </tr>
  			   <tr>'''
    if len(tasks) <= 0:
        data = data + '<b>No tasks found.</b><br/>'

    for info in tasks:
        data = data + ('''<td>%s</td>
        			<td>%d</td> 
        			<td>%s</td>
        			</tr>''' % (info['category'], info['priority'], info['description']))

    data += '</table>'
    if len(tasks) > 0:
        data = data
    data = data + get_footer()
    return data

@app.route('/task/add', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
    	category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']

        insert_task(description, priority, category)

        return redirect(url_for('tasks'))
    else:
        return '''%s<form method="post" action="%s">
            <div class="field">
                <label for="description">Description:</label>
                <input type="text" name="description" id="description">
            </div>
            <div class="field">
                <label for="category">Category:</label>
                <input type="text" name="category" id="category">
            </div>
            <div class="field">
                <label for="priority">Priority:</label>
                <input type="number" name="priority" id="priority">
            </div>
            <div class="field">
                <input type="submit" value="Add">
            </div>
        </form>
        %s''' % (get_header('Add New Task'), url_for('new_task'), get_footer())

def get_header(method):
	if(method == 'GET'):
		return '''<!DOCTYPE html>
				<html>
				<head>
 				   <title></title>
				<style>
					table, th, td{
						border: 1px solid black;
						border-collapse: collapse;
					}
				</style>
				</head>
				<body>
				<h1>Lab 4</h1>
    			<form method="post" action="%s">
            		<div class="field">
              		  <label for="category">Category:</label>
                	  <input type="text" name="category" id="category">
            		</div>
            		<div class="field">
              		  <label for="priority">Priority:</label>
             	      <input type="number" name="priority" id="priority">
           			</div>
            		<div class="field">
                		<label for="description">Description:</label>
                		<input type="text" name="description" id="description">
            		</div>
            		<div class="field">
                		<input type="submit" value="Add">
            		</div>
        		</form>%s<br/><br/>''' % (url_for('new_task'), get_footer())


def get_footer():
    return '''</body></html>'''

if __name__ == "__main__":
    query_db("CREATE TABLE IF NOT EXISTS tasks (description TEXT, priority INTEGER, category TEXT)")
    app.debug = True
    app.run()
