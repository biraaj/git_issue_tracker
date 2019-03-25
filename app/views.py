from app import app
from app import count_issues
from flask import request, render_template

@app.route('/')
def index():
	return render_template('welcome.html',result={},url='')

@app.route('/', methods=['POST'])
def display_table():
	git_url = request.form['search'].strip()
	processed_stats = count_issues.get_issues_stats(git_url)
	return render_template('welcome.html',result=processed_stats,url=git_url)
