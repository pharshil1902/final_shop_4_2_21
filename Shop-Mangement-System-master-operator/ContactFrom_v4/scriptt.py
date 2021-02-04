from flask import Flask,render_template,request, session, abort,flash,redirect,url_for, jsonify
import secrets
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
import pdfkit
import time 
import mysql.connector

from threading import Thread

global ip_list
ip_list = {'13.240.20.244':'palkesh','13.240.20.12':'yogesh','13.240.20.173':'bharat','13.240.20.106':'kansara','13.240.20.224':'new','127.0.0.1':'harshil','13.240.20.251':'new2'}
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

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
	search = request.form.get("text")
	conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
	curr = conn.cursor()
	query = f"select distinct company_name,mobile from main_shop  where company_name lIKE '{search}%' order by entry_code DESC; "
	curr.execute(query)
	result = curr.fetchall()

	b=[]
	m=[]
	print(result[0][0])
	
	for i in range(len(result)):
		if result[i][0] not in b:
			b.append(result[i][0]) 
			m.append(result[i][1]) 
	
	ans = [b,m]
	return jsonify(ans) 

@app.route('/')
def login():
	return render_template("login.html")


@app.route('/back_to_homepage')
def back_to_homepage():
	return redirect(url_for('login'))
#admin
@app.route('/special_admin')
def special_admin():
	d=['','','']
	return render_template("admin.html",data="0",d=d)

@app.route('/open_gst')
def open_gstt():
	print("hello")
	return render_template('gst_records.html')

		
			
@app.route('/print_delivery_ad',methods=['POST'])
def print_delivery_ad(): 
	data=[]
	e = datetime.datetime.now()
	dt = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}') #0
	data.append(dt[:16])
	
	
	cn = change_case(str(request.form.get('c_name'))) #1
	data.append(cn)
	operator = str(request.form.get('operator'))
	enc = str(request.form.get('enc'))
	data.append(str(request.form.get('mobile'))) #2
	rm=[]
	print(enc)
	print("------------------------")

	try:
		conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM second_shop WHERE entry_code={enc} """
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print(dataa)
		sql_create = f"""SELECT dc_code FROM admin_codes"""
		curr.execute(sql_create)
		code = curr.fetchall()
		
	except Exception as err:
		flash('error')
		print(err)
		return redirect(url_for('database_operator_open'))
	
	
	desc=[]
	qt=[]
	code = int(code[0][0])
	print(f'code:{code}')
	
	for i in range(0,len(dataa)):
		
		desc.append(str(dataa[i][7]+"-"+dataa[i][8]+"-"+dataa[i][9]+"-"+dataa[i][10]))
		qt.append(dataa[i][11])
		
		rm.append(str(dataa[i][14]))
		if(dataa[i][12]!='None'):
			desc.append(dataa[i][12])
			qt.append(dataa[i][13])
			

	data.append(str(operator))
	return render_template("delivery_challan.html",data=data,desc=desc,qt=qt,rm=rm,code=code)


@app.route('/print_delivery_op',methods=['POST'])
def print_delivery_op():
	try:
		data=[]
		e = datetime.datetime.now()
		dt = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}') #0
		#dt = f'31/10/2020:{e.hour}:{e.minute}'
		data.append(dt[:16])
		print(dt[:10])
		dt = str(f'{e.day}/{e.month}/{e.year}') #0
		print(dt)
		
		oper = str(request.form.get('operator'))
		cn = change_case(str(request.form.get('c_name'))) #1
		data.append(cn)

		enc = str(request.form.get('enc'))
	
		
		rm=[] 

		try:
			conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
			curr = conn.cursor()
			sql_create = f"""SELECT * FROM second_shop WHERE entry_code={enc} """
			curr.execute(sql_create)
			dataa = curr.fetchall()
			print(dataa[0][7])
			sql_create = f"""SELECT order_code from ORDER_CODES where operator_name = '{oper}'"""
			curr.execute(sql_create)
			dat = curr.fetchall()
			print(dat)
			dat = int(dat[0][0])
			print(f'dat{dat}')
			sql_create = f"""SELECT datee from ORDER_CODES where operator_name = '{oper}' and datee = '{dt}' """
			curr.execute(sql_create)
			datee = curr.fetchall()
			print(datee)
			
			if(len(datee)==0 ):
				ort = 1
			else: 
				ort = dat + 1	
		except Exception as err:
			flash('error')
			print(err)
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
			

	

		return render_template("orader_copy.html",data=data,desc=desc,qt=qt,rm=rm,ort=ort)	
	except:
		return redirect(url_for('open_database_op'))



@app.route('/increment_odc',methods=['POST'])
def increment_odc():
	try:
		e = datetime.datetime.now()
		dt = str(f'{e.day}/{e.month}/{e.year}')
		#dt = '31/10/2020'
		conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM order_codes where datee like '{dt}%' and  operator_name = '{ip_list[str(request.remote_addr)]}'"""
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print('hello----------------------')
		print(len(dataa))
		if len(dataa) == 0:
			dat=1
			dat=str(dat)
			sql_create = f"""UPDATE ORDER_CODES SET order_code='{dat}',datee='{dt}' where operator_name = '{ip_list[str(request.remote_addr)]}' """
			curr.execute(sql_create)
			conn.commit()
		else:
			sql_create = f"""SELECT order_code from ORDER_CODES where operator_name = '{ip_list[str(request.remote_addr)]}'"""
			curr.execute(sql_create)
			dat = curr.fetchall()
			print(dat)
			dat = int(dat[0][0])
			print(f'dat{dat}')
			dat+=1
			dat=str(dat)
			sql_create = f"""UPDATE ORDER_CODES SET order_code='{dat}' where operator_name = '{ip_list[str(request.remote_addr)]}' """
			curr.execute(sql_create)
			conn.commit()	
		return redirect(url_for('open_database_op'))
	except Exception as err:
		print(err)
		return redirect(url_for('open_database_op'))
#operator
@app.route('/special_operator')
def special_operator():
	d=['','','']
	return render_template("operator.html",data="0",d=d)

@app.route('/open_database_op',methods=['POST','GET'])
def open_database_op():
	try:
		if session[ip_list[str(request.remote_addr)]]==True:
			try:
				conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
				curr = conn.cursor()
				sql_create = """SELECT * FROM SECOND_SHOP order by entry_code + 0 DESC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				
				
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


@app.route('/operator',methods=['POST'])
def operator():
	operators={'palkesh':'palkesh','bharat':'bharat','kansara':'kansara','yogesh':'yogesh','new':'new','harshil':'harshil','new2':'new2'}
	global operator_name
	operator_name = request.form['username']
	
	if request.form['username'] in operators and  request.form['password'] == operators[request.form['username']]:
		session[ip_list[str(request.remote_addr)]] = True
		print(request.remote_addr)
		
		flash('Welcome '+str(ip_list[str(request.remote_addr)])+"!")
		d=['','','']
		return render_template("operator.html",data="0",d=d)
	else:
		flash('wrong password!')
		return render_template('operator_login.html')
	#return render_template("admin.html")

@app.route('/operator_login')
def operator_log():
	
	try:
		# create connection
		global con
		con =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
		flash('Operator Database Connected')
		#messagebox.showinfo("DATABASE CONNECTED!", "DATABASE CONNECTED!")
	except Exception as err:
		#messagebox.showerror("Error", "DATABASE NOT CONNECTED!")
		print(err)
		flash('Operator Database Not Connected')	
	

	if  session.get(ip_list[str(request.remote_addr)]):
                
                flash('Welcome!')
                return redirect(url_for('special_operator'))
		
	else:
                
                return render_template('operator_login.html')
		
	#return render_template("operator_login.html")
 


@app.route('/add_job_operator',methods=['POST','GET'])
def adding_job_operator():
	try:
		if session[ip_list[str(request.remote_addr)]]==True and request.method == "POST":
				print("HEREERE")
				try:
					conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
					e = datetime.datetime.now()
					date_time = str(f'{e.day}/{e.month}/{e.year}   :   {e.hour}:{e.minute}:{e.second}')
					
					cur = conn.cursor()
					#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
					
					

					sql = "SELECT enc from ENTRY_CODE"
					cur.execute(sql)
					enc = cur.fetchall()
					print(enc)
					if(int(request.form.get('choice')) == 0):
						enc=int(enc[0][0])+1
					else: 
						enc=int(enc[0][0])	
					
					sql = f"UPDATE  ENTRY_CODE SET enc={enc}"
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
					
					
					
				
					sql_create = """INSERT INTO SECOND_SHOP VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
					#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
					#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
					cur.execute(sql_create,(enc,date_time,str(ip_list[str(request.remote_addr)]),cn,dn,mobile,descrip,sz,ty,cl,dup,qt,add_service,add_qty,remark))
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
			print(session[ip_list[str(request.remote_addr)]])
			print(request.method)
			return redirect(url_for('operator_log'))	
			

	except Exception:
			flash('Error Occured!')
			return  redirect(url_for('special_operator'))
	return 	render_template("operator.html",data="0",d=d)	


@app.route('/operator_submit',methods=['POST'])	
def operator_submit():
	if session[ip_list[str(request.remote_addr)]]==True:
		print("HEREERE")
		try:
			conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
			e = datetime.datetime.now()
			date_time = str(f'{e.day}/{e.month}/{e.year}   :   {e.hour}:{e.minute}:{e.second}')
			cur = conn.cursor()
			#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
			print("hello")

			
			
			sql = "SELECT enc from ENTRY_CODE"
			cur.execute(sql)
			enc = cur.fetchall()
			print(enc)
			if(int(request.form.get('choice')) == 0):
				enc=int(enc[0][0])+1
			else: 
				enc=int(enc[0][0])	
			
			sql = f"UPDATE  ENTRY_CODE SET enc={enc}"
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
		
			print(ip_list[str(request.remote_addr)])
			sql_create = """INSERT INTO SECOND_SHOP VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
			#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
			#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
			cur.execute(sql_create,(enc,date_time,ip_list[str(request.remote_addr)],cn,dn,mobile,descrip,sz,ty,cl,dup,qt,add_service,add_qty,remark))
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
	    
		session[ip_list[str(request.remote_addr)]] = False
		flash('Log Out Successful!')
		return render_template("operator_login.html")

	
if __name__ == "__main__":
	
	app.run(debug=True,host="13.240.20.251", port=5000,threaded=True,use_reloader=False)
	

	#app.run(debug=False,host="127.0.0.1", port=5000, threaded=False,use_reloader=False)
	
