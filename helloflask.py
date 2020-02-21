from flask import Flask, render_template, url_for, request, redirect,flash, jsonify, send_from_directory, send_file, g, make_response, json
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_wtf import FlaskForm
import pandas as pd
import csv
import os
import codecs
import webbrowser

from flask import session
# import dash_html_components as html
import plotly.graph_objs as go
import visualization 
import numpy as np
from chart_studio.plotly import iplot
import plotly.figure_factory as ff
import plotly.plotly as py
import plotly.offline as plotly
app = Flask(__name__)#,root_path='C:/Users/Marcel Sutedja/Documents/Python Scripts/flask-python/'
app.config.from_object(__name__)


upload_folder = 'C:/Users/Marcel Sutedja/Documents/Python Scripts/flask-python/plotly.html'
app.config['upload_folder'] = upload_folder
app.config['SECRET_KEY'] = '58a5df3259fc0f9f8f33580eb473b0cc'



class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])    
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)     
        if request.method == 'POST':
            name=request.form['name']
            print (name)
        if form.validate():
            # Save the comment here.
            flash('Hello ' + name)
        else:
            flash('All the form fields are required. ')
        return render_template('home.html', form=form)
@app.route('/home/')
def home():
	return render_template('newHome.html')
 	
@app.route('/load',methods =['GET','POST'])
def home1():
	datalist=[]
	# visualization.getDataFromDB(datalist)

	if request.method == 'POST':
		dic={}
		
		#get input from viz.html using name=csv
		filename = request.form['filename']
		filename2 = request.form['filename2']
		#request filename from web pages
		# session['file'] = request.form['filename']		
		# variable2 = request.form['csv2']
	
		session['variable'] = request.form['csv']
		session['variable2'] = request.form['csv2']
		
		# tempList = [session['file'],session['variable']]
		# datalist.append(tempList)
		
		# visualization.storeDataToDB(datalist)
		#display name of dataset
		return render_template('load.html',filename=filename,filename2=filename2)
	return render_template('load.html',datalist=datalist, len=len(datalist))

@app.route('/table')
def table():
	if 'variable' in session:
		variable2 = session['variable']
		visualization.display_csv(variable2)
	return render_template('table.html')
#load table


@app.route('/plot')
def plot1():
	if 'variable' in session:
		
		variable = session['variable']
		df = pd.read_csv(variable)
		visualization.line_plot(df)
	return render_template('plotly2.html')


@app.route('/table/<datalist>')
def table1(datalist):
	datalist=[]
	visualization.getDataFromDB(datalist) 
	namelist = []
	for i in range(0,len(datalist)):
		namelist.append(datalist[i][1])
		visualization.display_csv(datalist[i][1])


	# if 'variable' in session:
	# 	variable = session['variable']
	# 	visualization.display_csv(variable)
	return render_template('table.html',datalist=datalist)


@app.route('/table2')
def table2():
	if 'variable2' in session:
		variable2 = session['variable2']
		visualization.display_csv(variable2)
	return render_template('table.html')

@app.route('/plot2')
def plot2():
	global datalist
	if 'variable2' in session:
		
		variable2 = session['variable2']
		df = pd.read_csv(variable2)
		visualization.line_plot(df)
	return render_template('plotly2.html')

# @app.route('/load/preview')
# def preview():
# 	datalist=[]
# 	visualization.getDataFromDB(datalist)
# 	return render_template('load.html',datalist=datalist, len=len(datalist))



@app.route('/preview',methods=['GET','POST'])
def preview1():
	if 'file' and 'file2' in session:
		file = session['file']
		file2 = session['file2']
		return render_template('preview.html',file=file,file2=file2)




@app.route('/fe',methods =['GET','POST'])
def FE():
	
	if request.method == 'POST':
		
		#get input from viz.html using name=csv
		# webbrowser.open('C:/Users/Marcel Sutedja/Documents/Python Scripts/flask-python/templates/plotly.html')
		if request.form['chart'] == '3D_plot':

			
			return render_template('iris3.html')
		elif request.form['chart'] == 'radar':
			
			return render_template('Radar1.html')
		elif request.form['chart'] == 'plot':
			
			return render_template('plotly2.html')
	if 'file' and 'file2' in session:
		file = session['file']
		file2 = session['file2']
		return render_template('featuresEngineering.html',file=file,file2=file2)
	

	return render_template('featuresEngineering.html')

#  


		
	
	# return render_template('plotly.html')

@app.route('/interactive/')
def interactive():
	
	return render_template('iris.html')		
	#change title to marcel sutedja in home.html
    
@app.route('/index')
def about():
    return render_template('index.html')
@app.route('/about', methods=['POST','GET'])

# @app.route('/register/', methods=['GET','POST'])
# def register():
# 	form =RegistrationForm()
# 	if form.validate_on_submit():
# 		flash(f'Accont created for {form.username.data}!', 'success')
# 		return redirect(url_for('home'))
#     return render_template('register.html',title='register', form=form )

@app.route('/astar', methods=['POST'])
def background_process():
	req = request.get_json()
	print(req)
	res = make_response(jsonify({req}),200)
	return res

@app.route('/viz', methods = ['GET','POST'])
def viz():
	if request.method == 'POST':
		filename = request.form['filename']
		filename2 = request.form['filename2']
		session['file'] = request.form['filename']
		session['file2']= request.form['filename2']

		
		# variable = request.form['csv']
		# variable2 = request.form['csv2']
		session['variable'] = request.form['csv']
		session['variable2'] = request.form['csv2']
		return render_template('viz.html')
	return render_template('viz.html')
@app.route('/test',methods =['GET','POST'])
def test():
	
	list = ["pikacu","barabara","coco"]
	variablelist = []
	if request.method == 'POST':
		
		filename = request.form['filename']
		list.append(filename)
		session['file1']= list[3]
		
		variable=session['file1']

		
		session['file'] = request.form['filename']
		session['variable']= request.form['csv']
		# variable = request.form['csv']
		# variablelist.append(variable)
		
		return render_template('test.html', list=list, len=len(session), variable=variable, session=session)

	return render_template('test.html', list=list, len=len(list))
def table4():
	return render_template('table.html')


# @app.route('/login')
# def login():
# 	form = LoginForm()
#     return render_template('login.html', title='Login', form=form)





if __name__=='__main__':
    
    app.run(debug=True)
