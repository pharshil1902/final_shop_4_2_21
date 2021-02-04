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

global CONN_INFO 
CONN_INFO = {
    'host': '13.240.20.12',
    'port': 1521,
    'user': 'system',
    'psw': 'sankalp',
    'service': 'XE'
}

global CONN_STR 
CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)  


  
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


@app.route('/')
def login():
	return render_template("login.html")


@app.route('/back_to_homepage')
def back_to_homepage():
	return redirect(url_for('login'))
#admin
@app.route('/special_admin')
def special_admin():
	d=['Enter Company Name','Enter Mobile','Enter DeliveryMan Name']
	return render_template("admin.html",data="0",d=d)

@app.route('/open_gst')
def open_gstt():
	print("hello")
	return render_template('gst_records.html')

@app.route('/gst_submit',methods=['POST'])
def gst_submit():

	conn = cx_Oracle.connect(CONN_STR)
	curr = conn.cursor()
	c_name = str(change_case(str(request.form.get('c_name'))))
	gst_no = str(request.form.get('gst_no'))
	sql_create = f""" INSERT INTO GST_RECORDS VALUES('{c_name}','{gst_no}')"""
	curr.execute(sql_create)
	curr.close()
	conn.commit()
	print("hello")
	return redirect(url_for('open_gstt'))
	
global admin_name
admin='Yogesh'

@app.route('/admin_login')
def admin_log():
	

	if not session.get('logged_in_admin'):
		try:
			#	e connection
			
			conn = cx_Oracle.connect(CONN_STR)
			flash('Admin Database Connected')
			print(conn.version)
			#messagebox.showinfo("DATABASE CONNECTED!", "DATABASE CONNECTED!")
		except Exception as err:
			#messagebox.showerror("Error", "DATABASE NOT CONNECTED!")
			flash('Admin Database Not Connected')
		return render_template('admin_logon.html')
	else:
		flash('Welcome '+str(admin_name)+"!")
		return redirect(url_for('special_admin'))
	#return render_template("operator_login.html")	
@app.route('/admin',methods=['POST'])
def admin():
	global admin_name
	admin_name = request.form['username']
	
	ans = 'admin'
	ed=str(os.environ.get('__rt_p_aew_'))
	
	
	#ans=ans
	ff = "password"
	if request.form[ff] == ff and admin_name == ans :
		flash('Welcome '+str(admin_name)+"!")
		session['logged_in_admin'] = True
		d=['Enter Company Name','Enter Mobile','Enter DeliveryMan Name']
		return render_template("admin.html",data="0",d=d)
	else:
		flash('wrong password!')
		print("wrong")
		return render_template("admin_logon.html")
	#return render_template("admin.html")
@app.route('/logout_admin')	
def admin_logout():
		flash('Logout Successful')
		session['logged_in_admin'] = False
		return render_template("admin_logon.html")

@app.route('/search_db',methods=["POST"])
def search_database():
	try:
		if session['logged_in_admin']==True:
			try:
				conn = cx_Oracle.connect(CONN_STR)
				curr = conn.cursor()
				searchbox = str(change_case(str(request.form.get('search'))))
				sql_create = f""" SELECT * FROM MAIN_SHOP WHERE company_name LIKE '{searchbox}%' order by entry_code"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				month = request.form.get('month')
		        
				dt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
				
				print(f'ddddd{dataa}')
				print(conn.version)
				
				c=1
				i=0
				while(i<len(dataa)):
					s=""
					print(dataa[i][1])
					s+=dataa[i][1][3]
					if(dataa[i][1][4]!='/'):
						s+=dataa[i][1][4]
					s=int(s)
					print(f's:{s}')
					print(f'month:{month}')
					j=0
					if int(month)==13 or s == int(month):
						while(j<(len(dataa[i]))):
							dt[j].append(dataa[i][j])
							j+=1
						c+=1
					i+=1		
				dictt = {}
				i=0
			
				while(i<23):
					dictt.update({i:dt[i]})
					i+=1
				
				data = pd.DataFrame(dictt)
				
				curr.close()
				print(f'data: {data}')
				html = data.values.tolist()
				print(len(html))
				if len(html) != 0:
					flash(html)
				print("herre")	
				return render_template("database.html")
				
				
			except Exception as err:	
				flash('Admin Database Not Connected')
				print(f'error: {err}')
				return redirect(url_for("admin_logout"))
		
		else:
			flash('Not logged in!')
			return  redirect(url_for('admin_logout'))	
	except Exception:
			flash('Not logged in!')
			return  redirect(url_for('admin_logout'))	

@app.route('/export_search_db',methods=["POST"])
def export_search_database():
	try:
		if session['logged_in_admin']==True:
			try:
				conn = cx_Oracle.connect(CONN_STR)
				curr = conn.cursor()
				searchbox = str(change_case(str(request.form.get('search'))))
				sql_create = f""" SELECT * FROM MAIN_SHOP WHERE company_name LIKE '{searchbox}%' order by entry_code"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				month = request.form.get('month')
		        
				dt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
				
				print(f'ddddd{dataa}')
				print(conn.version)
				
				c=1
				i=0
				while(i<len(dataa)):
					s=""
					print(dataa[i][1])
					s+=dataa[i][1][3]
					if(dataa[i][1][4]!='/'):
						s+=dataa[i][1][4]
					s=int(s)
					print(f's:{s}')
					print(f'month:{month}')
					j=0
					if int(month)==13 or s == int(month):
						while(j<(len(dataa[i]))):
							dt[j].append(dataa[i][j])
							j+=1
						c+=1
					i+=1		
				dictt = {}
				i=0
			
				while(i<23):
					dictt.update({i:dt[i]})
					i+=1
				
				data = pd.DataFrame(dictt)
				
				curr.close()
				print(f'data: {data}')
				dataa = data.values.tolist()
				data=[]
				dt = str(datetime.datetime.now()) #0
				data.append(dt[:10])
	
				cn = change_case(str(searchbox)) #1
				data.append(cn)

				enc = str(dataa[0][0])
				data.append(str(dataa[0][5])) #2
				data.append(str(dataa[0][21])) #3
				data.append(str(dataa[0][20])) #4  

		
    
				desc=[]
				qt=[]
				rt=[]
				amt=[]
				sb=[]
	
				for i in range(0,len(dataa)):
		
					desc.append(str(dataa[i][7]+"-"+dataa[i][8]+"-"+dataa[i][9]+"-"+dataa[i][10]))
					qt.append(dataa[i][11])
					rt.append(dataa[i][12])
					amt.append(dataa[i][13])
					if(dataa[i][14]!='None'):
						desc.append(dataa[i][14])
						qt.append(dataa[i][15])
						rt.append(dataa[i][16])
						amt.append(dataa[i][17])
		
					sb.append(float(dataa[i][19]))
    
				fin = 0.0
				cgst = float(str(dataa[0][21]))
				sgst = float(str(dataa[0][20]))
				subtotal = 0
				for i in sb:
					subtotal+=i
					fin+=(i*cgst/100)
					fin+=(i*sgst/100)
				fin+=subtotal
				f_cgst = subtotal*cgst/100
				f_sgst = subtotal*sgst/100



				data.append(round(fin)) #5
				data.append(f_cgst) #6
				data.append(f_sgst) #7
				data.append(str(fin)) #8
				data.append(str(subtotal)) #9

	
				try:
							conn = cx_Oracle.connect(CONN_STR)
							curr = conn.cursor()
							sql_create = f"""SELECT GST_NO FROM GST_RECORDS WHERE COMPANY_NAME LIKE '{cn}' """
							curr.execute(sql_create)
							dataa = curr.fetchall()
							print(dataa[0][0])
							print("hehehehe")
							data.append(str(dataa[0][0])) #10
							print(conn.version)
							curr.close()

							return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb)
				
				
				except Exception as err:
							dataa=""
							print(f"nooo:{err}")	
				
							data.append(str(dataa))
							return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb)
	
	
				return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb)


				
				
				
			except Exception as err:	
				flash('Admin Database Not Connected')
				print(f'error: {err}')
				return redirect(url_for("admin_logout"))
		
		else:
			flash('Not logged in!')
			return  redirect(url_for('admin_logout'))	
	except Exception:
			flash('Not logged in!')
			return  redirect(url_for('admin_logout'))	

@app.route('/export_search_db_m',methods=["POST"])
def export_search_database_m():
	try:
		if session['logged_in_admin']==True:
			try:
				conn = cx_Oracle.connect(CONN_STR)
				curr = conn.cursor()
				searchbox = str(change_case(str(request.form.get('search'))))
				sql_create = f""" SELECT * FROM MAIN_SHOP WHERE company_name LIKE '{searchbox}%' order by date_time"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				output = io.BytesIO()
			
				month = request.form.get('month')
		        
				dt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
				
				print(dataa)
				print(conn.version)
				
				c=1

				for i in range(len(dataa)):
					s=""
					print(dataa[i][0])
					s+=dataa[i][0][3]
					if(dataa[i][0][4]!='/'):
						s+=dataa[i][0][4]
					s=int(s)
					print(s)
				
					j=0
					if int(month)==13 or s == int(month):
						while(j<(len(dataa[i]))):
							dt[j].append(dataa[i][j])
							j+=1
						c+=1
			
				output.seek(0)			
				curr.close()
			
				dictt = {}
				i=0
				header=[
					'Date-Time',
					'Operator/Admin',
					'Company Name',
					'DeliveryMan',
					'Mobile Number',
					'Description',
					'Size',
					'Media-type',
					'Color',
					'Duplex',
					'Quantity',
					'Rate',
					'Amount',
					'ADD_SERVICE',
					'REMARKS',
					'ADD_QUANTITY',
					'ADD_RATE',
					'ADD_AMOUNT',
					'Final-Total'
				]

				while(i<19):
					dictt.update({header[i]:dt[i]})
					i+=1
				data = pd.DataFrame(dictt)
				
				root = tkinter.Tk()
				root.geometry("500x500")
				root.after(1, lambda: root.focus_force())	
				root.attributes("-topmost", True)
				root.attributes('-alpha', 0)
				filename = filedialog.asksaveasfilename(title="Save as", defaultextension=".xls")
				root.destroy()
				root.mainloop()
				if(len(filename)>0):
					data.to_excel(filename,index=False)
				
				print(data)
				html = data.values.tolist()
				flash(html)
				return render_template("database.html")
				
				
			except Exception as err:	
				flash('Admin Database Not Connected or Export Unsuccessful!')
				print(err)
				return render_template("admin_logout")
			
		else:
			flash('Not logged in!')
			return  redirect(url_for('admin_logout'))	
	except Exception:
			flash('Not logged in!')
			return  redirect(url_for('admin_logout'))	

@app.route('/database_operators')
def database_operator_open():
	try:
		if session['logged_in_admin']==True:
			try:
				conn = cx_Oracle.connect(CONN_STR)
				curr = conn.cursor()
				sql_create = """SELECT * FROM SECOND_SHOP order by entry_code + 0 DESC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				print(dataa)
				print(conn.version)
				curr.close()
				flash(dataa,'category2')
				data=[]
				return render_template("database_operator.html")
				
				
			except Exception as err:	
				flash('Admin Database Not Connected')
				print(err)
				return render_template("admin_logout")
			
		else:
			flash('Not logged in!')
			return  redirect(url_for('admin_logout'))	
	except Exception:
			flash('Not logged in!')
			return  redirect(url_for('admin_logout'))	

@app.route('/edit_admin', methods=["POST"])
def edit_admin():
	if request.method == "POST":
		try:
			res = request.form
			print("HERERERE")
			print(res)
			return render_template('admin_edit.html',res=res,data="0")
		except Exception as err:
			flash(f"Edit Unsuccessful! + {err}",'category1')
			return redirect(url_for('database_operator_open'))

@app.route('/edit_submit', methods=["POST"])
def edit_submit():
	try:
		if session['logged_in_admin']==True and request.method == "POST":
			print("HEREERE")
			try:
				conn = cx_Oracle.connect(CONN_STR)
				e = datetime.datetime.now()
				date_time = str(request.form.get('date'))
				print(f'datetime={date_time}')
				cur = conn.cursor()
				#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
				enc = str(request.form.get('enc'))
				print(conn.version)
				people = str(request.form.get('operator'))
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
				rt = str(request.form.get('rate'))
				am = str(float(qt)*float(rt))
				add_service = str(request.form.get('add_service'))
				remark = str(request.form.get('add_remark'))
				add_qty = str(request.form.get('add_qty'))
				add_rate = str(request.form.get('add_rate'))
				add_amt = float(add_qty)*float(add_rate)
				subtotal = str(request.form.get('subtotal'))
				sgst = str(request.form.get('sgst'))
				cgst = str(request.form.get('cgst'))
				finalamount = str(request.form.get('famt'))
				print(am)
				sql_create = """INSERT INTO MAIN_SHOP VALUES(:enc,:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:dup,:qt,:rt,:am,:add_service,:add_qty,:add_rate,:add_amt,:remark,:subtotal,:sgst,:cgst,:famt)"""
				#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
				#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
				cur.execute(sql_create,{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'dup':dup,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'remark':remark,'subtotal':subtotal,'sgst':sgst,'cgst':cgst,'famt':finalamount,'enc':enc})
			
				conn.commit()
			
				sql_create = f"""DELETE FROM SECOND_SHOP WHERE date_time='{date_time}'  """
				cur.execute(sql_create)
				cur.close()
				conn.commit()
				flash('Entry Editted & Submitted!','category1')
				return redirect(url_for('database_operator_open'))

			except Exception as err:
				print("error while inserting data:", err)
				flash("Error while inserting data!",'category1')
				return render_template("database_operator_open")
		else:
			flash('You are not logged in!')
			return redirect(url_for('admin_log'))	
	except Exception:
			flash('Error Occured!','category1')
			return  redirect(url_for('database_operator_open'))


@app.route('/database')
def database_open():
	try:
		if session['logged_in_admin']==True:
			try:
				conn = cx_Oracle.connect(CONN_STR)
				curr = conn.cursor()
				sql_create = """SELECT * FROM MAIN_SHOP order by entry_code + 0 DESC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				print(dataa)
				print(conn.version)
				curr.close()
				flash(dataa)
				data=[]
				return render_template("database.html")
				
				
			except Exception as err:	
				flash('Admin Database Not Connected')
				print(err)
				d=['Enter Company Name','Enter Mobile','Enter DeliveryMan Name']
				return render_template("admin.html",data="0",d=d)
			
		else:
			flash('Not logged in!')
			return  redirect(url_for('special_admin'))	
	except Exception:
			flash('Not logged in!')
			return  redirect(url_for('special_admin'))	

@app.route('/admin_submit',methods=['POST','GET'])	
def admin_submit():
	try:
		if session['logged_in_admin']==True and request.method == "POST":
			print("HEREERE")
			try:
				conn = cx_Oracle.connect(CONN_STR)
				e = datetime.datetime.now()
				date_time = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}:{e.second}')
				
				cur = conn.cursor()
				#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
				print(conn.version)
				people = admin_name

				sql = "SELECT enc from ENTRY_CODE"
				cur.execute(sql)
				enc = cur.fetchall()
				print(enc)
				if(int(request.form.get('choice')) == 0):
						enc=int(enc[0][0])+1
				else: 
						enc=int(enc[0][0])
				sql = f"UPDATE ENTRY_CODE SET enc={enc}"
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
				rt = str(request.form.get('rate'))
				am = float(qt)*float(rt)
				add_service = str(request.form.get('add_service'))
				remark = str(request.form.get('add_remark'))
				add_qty = str(request.form.get('add_qty'))
				add_rate = str(request.form.get('add_rate'))
				add_amt = float(add_qty)*float(add_rate)
				subtotal = str(request.form.get('subtotal'))
				sgst = str(request.form.get('sgst'))
				cgst = str(request.form.get('cgst'))
				finalamount = str(request.form.get('famt'))
				print(finalamount)
				
				print(am)
				sql_create = """INSERT INTO MAIN_SHOP VALUES(:enc,:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:dup,:qt,:rt,:am,:add_service,:add_qty,:add_rate,:add_amt,:remark,:subtotal,:sgst,:cgst,:famt)"""
				#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
				#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
				cur.execute(sql_create,{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'dup':dup,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'remark':remark,'subtotal':subtotal,'sgst':sgst,'cgst':cgst,'famt':finalamount,'enc':enc})
				cur.close()
				conn.commit()
				flash('Entry Submitted!')
				d=['Enter Company Name','Enter Mobile','Enter DeliveryMan Name']
				return redirect(url_for('special_admin'))
			except Exception as err:
				print("error while inserting data:", err)
				flash("Error while inserting data!")
				return render_template("admin.html",data="0",d=d)
		else:
			flash('You are not logged in!')
			return redirect(url_for('admin_log'))	
	except Exception:
			flash('Error Occured!')
			return  redirect(url_for('special_admin'))	



@app.route('/add_job',methods=['POST','GET'])
def adding_job():
	try:
		if session['logged_in_admin']==True and request.method == "POST":
				print("HEREERE")
				try:
					conn = cx_Oracle.connect(CONN_STR)
					e = datetime.datetime.now()
					date_time = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}:{e.second}')
					
					cur = conn.cursor()
					#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
					print(conn.version)
					people = admin_name

					sql = "SELECT enc from ENTRY_CODE"
					cur.execute(sql)
					enc = cur.fetchall()
					print(enc)
					if(int(request.form.get('choice')) == 0):
						enc=int(enc[0][0])+1
					else: 
						enc=int(enc[0][0])	
					
					sql = f"UPDATE ENTRY_CODE SET enc={enc}"
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
					rt = str(request.form.get('rate'))
					am = float(qt)*float(rt)
					add_service = str(request.form.get('add_service'))
					remark = str(request.form.get('add_remark'))
					add_qty = str(request.form.get('add_qty'))
					add_rate = str(request.form.get('add_rate'))
					add_amt = float(add_qty)*float(add_rate)
					subtotal = str(request.form.get('subtotal'))
					sgst = str(request.form.get('sgst'))
					cgst = str(request.form.get('cgst'))
					finalamount = str(request.form.get('famt'))
					print(finalamount)
					
					print(am)
					sql_create = """INSERT INTO MAIN_SHOP VALUES(:enc,:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:dup,:qt,:rt,:am,:add_service,:add_qty,:add_rate,:add_amt,:remark,:subtotal,:sgst,:cgst,:famt)"""
					#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
					#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
					cur.execute(sql_create,{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'dup':dup,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'remark':remark,'subtotal':subtotal,'sgst':sgst,'cgst':cgst,'famt':finalamount,'enc':enc})
					cur.close()
					conn.commit()
					flash('Entry Submitted!')
					d=[cn,mobile,dn]
					
					return render_template("admin.html",data=str(int(request.form.get('choice'))+1),d=d)
				except Exception as err:
					print("error while inserting data:", err)
					flash("Error while inserting data!")
					return render_template("admin.html",data=str(int(request.form.get('choice'))),d=d)
				
		else:
			flash('You are not logged in!')
			return redirect(url_for('admin_log'))	

	except Exception:
			flash('Error Occured!')
			return  redirect(url_for('special_admin'))
	return 	render_template("admin.html",data="0",d=d)	

@app.route('/back_to_admin',methods=['POST'])
def back_to_admin():		
		d=['Enter Company Name','Enter Mobile','Enter DeliveryMan Name']
		return render_template('admin.html',data="0",d=d)


@app.route('/print_delivery_ad_m',methods=['POST'])
def print_delivery_ad_m():
	data=[]
	dt = str(datetime.datetime.now()) #0
	data.append(dt[:10])
	
	cn = change_case(str(request.form.get('c_name'))) #1
	data.append(cn)
	operator = str(request.form.get('operator'))
	enc = str(request.form.get('enc'))
	data.append(str(request.form.get('mobile'))) #2
	rm=[]

	try:
		conn = cx_Oracle.connect(CONN_STR)
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM main_shop WHERE entry_code={enc} """
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print(dataa[0][7])
	except Exception as err:
		flash('error')
		print(err)
		return redirect(url_for('database_operator_open'))	
    
	desc=[]
	qt=[]
	
	
	
	for i in range(0,len(dataa)):
		
		desc.append(str(dataa[i][7]+"-"+dataa[i][8]+"-"+dataa[i][9]+"-"+dataa[i][10]))
		qt.append(dataa[i][11])
		rm.append(str(dataa[i][18]))
		
		if(dataa[i][14]!='None'):
			desc.append(dataa[i][14])
			qt.append(dataa[i][15])
		
	data.append(str(operator))
	return render_template("delivery_challan.html",data=data,desc=desc,qt=qt,rm=rm)


@app.route('/print_delivery_ad',methods=['POST'])
def print_delivery_ad():
	data=[]
	dt = str(datetime.datetime.now()) #0
	data.append(dt[:10])
	
	cn = change_case(str(request.form.get('c_name'))) #1
	data.append(cn)
	operator = str(request.form.get('operator'))
	enc = str(request.form.get('enc'))
	data.append(str(request.form.get('mobile'))) #2
	rm=[]
	
	

	try:
		conn = cx_Oracle.connect(CONN_STR)
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM second_shop WHERE entry_code={enc} """
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print(dataa[0][7])
	except Exception as err:
		flash('error')
		print(err)
		return redirect(url_for('database_operator_open'))	
    
	desc=[]
	qt=[]
	
	
	for i in range(0,len(dataa)):
		
		desc.append(str(dataa[i][7]+"-"+dataa[i][8]+"-"+dataa[i][9]+"-"+dataa[i][10]))
		qt.append(dataa[i][11])
		
		rm.append(str(dataa[i][14]))
		if(dataa[i][12]!='None'):
			desc.append(dataa[i][12])
			qt.append(dataa[i][13])
			

	data.append(str(operator))
	return render_template("delivery_challan.html",data=data,desc=desc,qt=qt,rm=rm)


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


@app.route('/print_retail',methods=['POST'])
def print_retail():
	data=[]
	dt = str(datetime.datetime.now()) #0
	data.append(dt[:10])
	
	cn = change_case(str(request.form.get('c_name'))) #1
	data.append(cn)

	enc = str(request.form.get('enc'))
	data.append(str(request.form.get('mobile'))) #2
	data.append(str(request.form.get('cgst'))) #3
	data.append(str(request.form.get('sgst'))) #4  

	try:
		conn = cx_Oracle.connect(CONN_STR)
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM main_shop WHERE entry_code={enc} """
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print(dataa[0][7])
	except Exception as err:
		flash('error')
		return redirect(url_for('database_open'))	
    
	desc=[]
	qt=[]
	rt=[]
	amt=[]
	sb=[]
	
	for i in range(0,len(dataa)):
		
		desc.append(str(dataa[i][7]+"-"+dataa[i][8]+"-"+dataa[i][9]+"-"+dataa[i][10]))
		qt.append(dataa[i][11])
		rt.append(dataa[i][12])
		amt.append(dataa[i][13])
		if(dataa[i][14]!='None'):
			desc.append(dataa[i][14])
			qt.append(dataa[i][15])
			rt.append(dataa[i][16])
			amt.append(dataa[i][17])
		
		sb.append(float(dataa[i][19]))
    
	fin = 0.0
	cgst = float(str(request.form.get('cgst')))
	sgst = float(str(request.form.get('sgst')))
	subtotal = 0
	for i in sb:
		subtotal+=i
		fin+=(i*cgst/100)
		fin+=(i*sgst/100)
	fin+=subtotal
	f_cgst = subtotal*cgst/100
	f_sgst = subtotal*sgst/100



	data.append(round(fin)) #5
	data.append(f_cgst) #6
	data.append(f_sgst) #7
	data.append(str(fin)) #8
	data.append(str(subtotal)) #9
	return render_template("retail_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb)

@app.route('/print_challan',methods=['POST'])
def print_challan():
	data=[]
	dt = str(datetime.datetime.now()) #0
	data.append(dt[:10])
	
	cn = change_case(str(request.form.get('c_name'))) #1
	data.append(cn)

	enc = str(request.form.get('enc'))
	data.append(str(request.form.get('mobile'))) #2
	data.append(str(request.form.get('cgst'))) #3
	data.append(str(request.form.get('sgst'))) #4  

	try:
		conn = cx_Oracle.connect(CONN_STR)
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM main_shop WHERE entry_code={enc} """
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print(dataa[0][7])
	except Exception as err:
		flash('error')
		return redirect(url_for('database_open'))	
    
	desc=[]
	qt=[]
	rt=[]
	amt=[]
	sb=[]
	
	for i in range(0,len(dataa)):
		
		desc.append(str(dataa[i][7]+"-"+dataa[i][8]+"-"+dataa[i][9]+"-"+dataa[i][10]))
		qt.append(dataa[i][11])
		rt.append(dataa[i][12])
		amt.append(dataa[i][13])
		if(dataa[i][14]!='None'):
			desc.append(dataa[i][14])
			qt.append(dataa[i][15])
			rt.append(dataa[i][16])
			amt.append(dataa[i][17])
		
		sb.append(float(dataa[i][19]))
    
	fin = 0.0
	cgst = float(str(request.form.get('cgst')))
	sgst = float(str(request.form.get('sgst')))
	subtotal = 0
	for i in sb:
		subtotal+=i
		fin+=(i*cgst/100)
		fin+=(i*sgst/100)
	fin+=subtotal
	f_cgst = subtotal*cgst/100
	f_sgst = subtotal*sgst/100



	data.append(round(fin)) #5
	data.append(f_cgst) #6
	data.append(f_sgst) #7
	data.append(str(fin)) #8
	data.append(str(subtotal)) #9

	
	try:
				conn = cx_Oracle.connect(CONN_STR)
				curr = conn.cursor()
				sql_create = f"""SELECT GST_NO FROM GST_RECORDS WHERE COMPANY_NAME LIKE '{cn}' """
				curr.execute(sql_create)
				dataa = curr.fetchall()
				print(dataa[0][0])
				print("hehehehe")
				data.append(str(dataa[0][0])) #10
				print(conn.version)
				curr.close()

				return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb)
				
				
	except Exception as err:
				dataa=""
				print(f"nooo:{err}")	
				
				data.append(str(dataa))
				return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb)
	
	
	return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb)



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
global CONN_INFO_o 
CONN_INFO_o = {
    'host': '13.240.20.12',
    'port': 1521,
    'user': 'operator1',
    'psw': 'operator1',
    'service': 'XE'
}

global CONN_STR_o 
CONN_STR_o = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO_o)

global operator_name
operator_name='operator1'

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
		flash(f'Operator Database Not Connected {err}')	
	

	if not session.get('logged_in'):
		return render_template('operator_login.html')
	else:
		flash('Welcome '+str(operator_name)+"!")
		return redirect(url_for('special_operator'))
	#return render_template("operator_login.html")	
@app.route('/operator',methods=['POST'])
def operator():
	operators={'operator1':'operator1','operator2':'operator2','operator2':'operator2'}
	global operator_name
	operator_name = request.form['username']
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
	
