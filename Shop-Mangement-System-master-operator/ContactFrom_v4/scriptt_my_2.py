from flask import Flask,render_template,request, session, abort,flash,redirect,url_for
import secrets
import cx_Oracle
import xlwt
import io
import datetime
import pandas as pd
from tkinter import filedialog
import tkinter
import logging
from base64 import b64encode
import math
import sys, os
from PyQt5 import *
import time 

from threading import Thread


  
def change_case(word):
	wr = ""
	for i in word:
		if i.isupper() ==True:
			wr+=(i.lower())
		else:
			wr+=i	
	return wr			

global app
app = Flask(__name__)

app.config['SECRET_KEY'] = "HY998246sedgsdJjw#%"




global operator_name
operator_name = "operator1"

global CONN_INFO_o 
CONN_INFO_o = {
    'host': 'PATIL-PC',
    'port': 1521,
    'user': 'operator1',
    'psw': 'operator1',
    'service': 'XE'
}

global CONN_STR_o 
CONN_STR_o = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO_o)




@app.route('/print_delivery_op',methods=['POST'])
def print_delivery_op():
	try:
		data=[]
		dt = str(datetime.datetime.now()) #0
		data.append(dt[:16])
	
		cn = change_case(str(request.form.get('c_name'))) #1
		data.append(cn)

		enc = str(request.form.get('enc'))
	
		
		rm=[] 

		try:
			conn = cx_Oracle.connect(CONN_STR_o)
			curr = conn.cursor()
			sql_create = f"""SELECT * FROM system.second_shop WHERE entry_code={enc} """
			curr.execute(sql_create)
			dataa = curr.fetchall()
			print(dataa[0][7])
		except Exception as err:
			flash('error')
			return redirect(url_for('open_database_op'))	
    
		desc=[]
		qt=[]
		data.append(str(request.form.get('operator')))
		for i in range(0,len(dataa)):
		
			desc.append(str(dataa[i][7]+"-"+dataa[i][8]+"-"+dataa[i][9]+"-"+dataa[i][10]))
			qt.append(dataa[i][11])
		
			rm.append(str(dataa[i][14]))
			if(dataa[i][12]!='None'):
				desc.append(dataa[i][12])
				qt.append(dataa[i][13])
			

	

		return render_template("orader_copy.html",data=data,desc=desc,qt=qt,rm=rm)	
	except:
		return redirect(url_for('open_database_op'))


#operator
@app.route('/special_operator')
def special_operator():
	d=['Enter Company Name','Enter Mobile','Enter DeliveryMan Name']
	return render_template("operator.html",data="0",d=d)

@app.route('/open_database_op',methods=['POST','GET'])
def open_database_op():
	try:
		if session['logged_in']==True:
			try:
				conn = cx_Oracle.connect(CONN_STR_o)
				curr = conn.cursor()
				sql_create = """SELECT * FROM system.SECOND_SHOP order by entry_code + 0 DESC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				print(dataa)
				print(conn.version)
				curr.close()
				flash(dataa,'category2')
				data=[]
				return render_template('database_op.html')
				
				
			except Exception as err:	
				flash('Admin Database Not Connected')
				print(err)
				return render_template("operator.html")
			
		else:
			flash('Not logged in!')
			return  redirect(url_for('special_operator'))
		
	except:
		return redirect(url_for('special_operator'))

@app.route('/operator_login')
def operator_log():
	
	try:
		# create connection
		global con
		con = cx_Oracle.connect(CONN_STR_o)
		flash('Operator Database Connected')
		#messagebox.showinfo("DATABASE CONNECTED!", "DATABASE CONNECTED!")
	except Exception as err:
		#messagebox.showerror("Error", "DATABASE NOT CONNECTED!")
		flash('Operator Database Not Connected')	
	

	if not session.get('logged_in'):
		return render_template('operator_login.html')
	else:
		flash('Welcome '+"operator1"+"!")
		return redirect(url_for('special_operator'))
	#return render_template("operator_login.html")	
@app.route('/operator',methods=['POST'])
def operator():
	operators={'operator1':'operator1','operator2':'operator2','operator2':'operator2'}

	if operator_name in operators and  request.form['password'] == operators[operator_name]:
		session['logged_in'] = True
		flash('Welcome '+str(operator_name)+"!")
		d=['Enter Company Name','Enter Mobile','Enter DeliveryMan Name']
		return render_template("operator.html",data="0",d=d)
	else:
		flash('wrong password!')
		return render_template('operator_login.html')
	#return render_template("admin.html")



@app.route('/add_job_operator',methods=['POST','GET'])
def adding_job_operator():
	try:
		if session['logged_in']==True and request.method == "POST":
				print("HEREERE")
				try:
					conn = cx_Oracle.connect(CONN_STR_o)
					e = datetime.datetime.now()
					date_time = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}:{e.second}')
					
					cur = conn.cursor()
					#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
					print(conn.version)
					people = str(operator_name)

					sql = "SELECT enc from system.ENTRY_CODE"
					cur.execute(sql)
					enc = cur.fetchall()
					print(enc)
					if(int(request.form.get('choice')) == 0):
						enc=int(enc[0][0])+1
					else: 
						enc=int(enc[0][0])	
					
					sql = f"UPDATE system.ENTRY_CODE SET enc={enc}"
					cur.execute(sql)
					conn.commit()

					print(request.form.get('c_name'))
					cn = change_case(str(request.form.get('c_name')))
					dn = str(request.form.get('delivery'))
					mobile = str(request.form.get('mobile'))
					descrip =  str(request.form.get('message'))
					sz = str(request.form.get('size'))
					ty = str(request.form.get('type'))
					cl = str(request.form.get('color'))
					dup = str(request.form.get('duplex'))
					qt = str(request.form.get('quantity'))
				
				
					add_service = str(request.form.get('add_service'))
					
					add_qty = str(request.form.get('add_qty'))
					remark = str(request.form.get('add_remark'))
					
					
					
				
					sql_create = """INSERT INTO system.SECOND_SHOP VALUES(:enc,:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:dup,:qt,:add_service,:add_qty,:remark)"""
					#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
					#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
					cur.execute(sql_create,{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'dup':dup,'qt':qt,'add_service':add_service,'add_qty':add_qty,'remark':remark,'enc':enc})
					cur.close()
					conn.commit()
					flash('Entry Submitted!')
					d=[cn,mobile,dn]
					return render_template("operator.html",data=str(int(request.form.get('choice'))+1),d=d)
				except Exception as err:
					print("error while inserting data:", err)
					flash("Error while inserting data!")
					return render_template("operator.html",data=str(int(request.form.get('choice'))),d=d)
				
		else:
			flash('You are not logged in!')
			return redirect(url_for('operator_log'))	

	except Exception:
			flash('Error Occured!')
			return  redirect(url_for('special_operator'))
	return 	render_template("operator.html",data="0",d=d)	


@app.route('/operator_submit',methods=['POST'])	
def operator_submit():
	if session['logged_in']==True:
		print("HEREERE")
		try:
			conn = cx_Oracle.connect(CONN_STR_o)
			e = datetime.datetime.now()
			date_time = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}:{e.second}')
			cur = conn.cursor()
			#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
			print(conn.version)
			people = operator_name
			
			sql = "SELECT enc from system.ENTRY_CODE"
			cur.execute(sql)
			enc = cur.fetchall()
			print(enc)
			if(int(request.form.get('choice')) == 0):
				enc=int(enc[0][0])+1
			else: 
				enc=int(enc[0][0])	
			
			sql = f"UPDATE system.ENTRY_CODE SET enc={enc}"
			cur.execute(sql)
			conn.commit()

			print(request.form.get('c_name'))
			cn = str(request.form.get('c_name'))
			dn = str(request.form.get('delivery'))
			mobile = str(request.form.get('mobile'))
			descrip =  str(request.form.get('message'))
			sz = str(request.form.get('size'))
			ty = str(request.form.get('type'))
			cl = str(request.form.get('color'))
			dup = str(request.form.get('duplex'))
			qt = str(request.form.get('quantity'))
		
			add_service = str(request.form.get('add_service'))
			remark = str(request.form.get('add_remark'))
			add_qty = str(request.form.get('add_qty'))
		
		
			sql_create = """INSERT INTO system.SECOND_SHOP VALUES(:enc,:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:dup,:qt,:add_service,:add_qty,:remark)"""
			#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
			#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
			cur.execute(sql_create,{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'dup':dup,'qt':qt,'add_service':add_service,'remark':remark,'add_qty':add_qty,'enc':enc})
			cur.close()
			conn.commit()
			flash('Entry Submitted!')
			return redirect(url_for('special_operator'))
		except Exception as err:
			print("error while inserting data:", err)
			flash("Error while inserting data!")
			return redirect(url_for('operator_submit'))	
	else:
		flash('You are not logged in!')
		return redirect(url_for('operator_submit'))	


@app.route('/logout',methods=['POST'])	
def logout():
	
		session['logged_in'] = False
		flash('Log Out Successful!')
		return render_template("operator_login.html")

	
if __name__ == "__main__":
	
	app.run(debug=True,host="127.0.0.1", port=5000,threaded=False,use_reloader=False)
	

	#app.run(debug=False,host="127.0.0.1", port=5000, threaded=False,use_reloader=False)
	
