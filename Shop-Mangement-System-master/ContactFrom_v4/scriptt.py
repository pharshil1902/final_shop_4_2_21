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

global CONN_INFO 
CONN_INFO = {
    'host': '13.240.20.12',
    'port': 3306,
    'user': 'system',
    'psw': '1902',
    'service': 'XE'
}

global CONN_STR 
CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)  
CONN_STR = "host='13.240.20.12',user='root',passwd='1902',database='sys'"
global admin_name
admin_name = "yogesh"

  
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
	d=['','','']
	return render_template("admin.html",data="0",d=d)

@app.route('/open_gst')
def open_gstt():
	print("hello")
	return render_template('gst_records.html')

@app.route('/gst_submit',methods=['POST'])
def gst_submit():

	conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
	curr = conn.cursor()
	c_name = str(change_case(str(request.form.get('c_name'))))
	gst_no = str(request.form.get('gst_no'))
	sql_create = f""" INSERT INTO GST_RECORDS VALUES('{c_name}','{gst_no}')"""
	curr.execute(sql_create)
	curr.close()
	conn.commit()
	print("hello")
	return redirect(url_for('open_gstt'))
	

# cx_Oracle.connec
@app.route('/admin_login')
def admin_log():
	

	if not session.get('logged_in_admin'):
		try:
			#	e connection
			
			conn = mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
			flash('Admin Database Connected')
			
			#messagebox.showinfo("DATABASE CONNECTED!", "DATABASE CONNECTED!")
		except Exception as err:
			#messagebox.showerror("Error", "DATABASE NOT CONNECTED!")
			flash('Admin Database Not Connected')
			print(err)
		return render_template('admin_logon.html')
	else:
		flash('Welcome '+str(admin_name)+"!")
		return redirect(url_for('special_admin'))
	#return render_template("operator_login.html")	
@app.route('/admin',methods=['POST'])
def admin():
	
	
	ans = 'yogesh'
	ed=str(os.environ.get('__rt_p_aew_'))
	
	
	#ans=ans
	ff = "password"
	if request.form[ff] == 'yogesh' and admin_name == ans :
		flash('Welcome '+str(admin_name)+"!")
		session['logged_in_admin'] = True
		d=['','','']
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
				conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
				curr = conn.cursor()
				searchbox = str(change_case(str(request.form.get('search'))))
				sql_create = f""" SELECT * FROM MAIN_SHOP WHERE company_name LIKE '{searchbox}%' order by entry_code"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				month = request.form.get('month')
		        
				dt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
				
				print(f'ddddd{dataa}')
				
				
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

@app.route('/inc_tax_code',methods=['POST'])
def inc_tax_code():
	e = datetime.datetime.now()
	dt = str(f'{e.day}/{e.month}/{e.year}')
	#dt = '31/10/2020'
	req_data = request.form
	conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
	curr = conn.cursor()
	try:
		
		sql_create = f"""SELECT tax_code from admin_codes"""
		curr.execute(sql_create)
		dat = curr.fetchall()
		print(dat)
		dat = int(dat[0][0])
		print(f'dat{dat}')
		dat+=1
		dat=str(dat)
		sql_create = f"""UPDATE admin_codes SET tax_code='{dat}'  """
		curr.execute(sql_create)
		conn.commit()
		print("done")
		

		return redirect(url_for('database_open'))

	except Exception as err:	
		print(err)
		return redirect(url_for('database_open'))

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
	search = request.form.get("text")
	conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
	curr = conn.cursor()
	query = f"select distinct company_name,mobile from main_shop  where company_name lIKE '{search}%' order by entry_code DESC;"
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

@app.route('/inc_retail_code',methods=['POST'])
def inc_retail_code():
	e = datetime.datetime.now()
	dt = str(f'{e.day}/{e.month}/{e.year}')
	#dt = '31/10/2020'
	conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
	curr = conn.cursor()
	try:
		
		sql_create = f"""SELECT retail_code from admin_codes"""
		curr.execute(sql_create)
		dat = curr.fetchall()
		print(dat)
		dat = int(dat[0][0])
		print(f'dat{dat}')
		dat+=1
		dat=str(dat)
		sql_create = f"""UPDATE admin_codes SET retail_code='{dat}'  """
		curr.execute(sql_create)
		conn.commit()
		return redirect(url_for('database_open'))

	except Exception:	

		return redirect(url_for('database_open'))		
@app.route('/inc_dc_code',methods=['POST'])
def inc_dc_code():
	e = datetime.datetime.now()
	dt = str(f'{e.day}/{e.month}/{e.year}')
	#dt = '31/10/2020'
	conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
	curr = conn.cursor()
	try:
		
		sql_create = f"""SELECT dc_code from admin_codes"""
		curr.execute(sql_create)
		dat = curr.fetchall()
		print(dat)
		dat = int(dat[0][0])
		print(f'dat{dat}')
		dat+=1
		dat=str(dat)
		sql_create = f"""UPDATE admin_codes SET dc_code='{dat}'  """
		curr.execute(sql_create)
		conn.commit()
		return redirect(url_for('database_open'))

	except Exception:	

		return redirect(url_for('database_open'))

@app.route('/delete_entry',methods=["POST"])
def delete_entry():
        try:
                date_time = str(request.form.get('date'))
                conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
                cur = conn.cursor()
                sql_create = f"""DELETE FROM SECOND_SHOP WHERE date_time='{date_time}'  """
                cur.execute(sql_create)
                cur.close()
                conn.commit()
                flash('Entry Deleted!','category1')
                return redirect(url_for('database_operator_open'))
        except Exception as err:
                print(f'{err}')
                flash('Error!','category1')
                return redirect(url_for('database_operator_open'))
                

@app.route('/export_search_db',methods=["POST"])
def export_search_database():
	try:
		if session['logged_in_admin']==True:
			try:
				conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
				curr = conn.cursor()
				searchbox = str(change_case(str(request.form.get('search'))))
				sql_create = f""" SELECT * FROM MAIN_SHOP WHERE company_name LIKE '{searchbox}%' order by entry_code + 0 DESC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				month = request.form.get('month')
		        
				dt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
				
				print(f'ddddd{dataa}')
				
				
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
				e = datetime.datetime.now()
				dt = str(f'{e.day}/{e.month}/{e.year}')#0
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
				print(desc)
				print(qt)
				print(rt)
				print(amt)
				if len(desc)>8:
					sr=8
				else:
					sr=len(desc)	
	
				try:
							conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
							curr = conn.cursor()
							sql_create = f"""SELECT GST_NO FROM GST_RECORDS WHERE COMPANY_NAME LIKE '{searchbox}' """
							curr.execute(sql_create)
							dataa = curr.fetchall()
							print(dataa[0][0])
							print("hehehehe")
							data.append(str(dataa[0][0])) #10
							
							sql_create = f"""SELECT tax_code FROM admin_codes"""
							curr.execute(sql_create)
							code = curr.fetchall()
							curr.close()
							code = int(code[0][0])
							return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb,sr=sr,code=code)
				
				
				except Exception as err:
							dataa=""
							print(f"nooo:{err}")	
				
							data.append(str(dataa))
							return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb,sr=sr,code=code)
	
	
				return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb,sr=sr,code=code)


				
				
				
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
				conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
				curr = conn.cursor()
				searchbox = str(change_case(str(request.form.get('search'))))
				sql_create = f""" SELECT * FROM MAIN_SHOP WHERE company_name LIKE '{searchbox}%' order by entry_code + 0 ASC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				output = io.BytesIO()
			
				month = request.form.get('month')
		        
				dt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
				
				print(dataa)
				
				
				c=1

				for i in range(len(dataa)):
					s=""
					print(dataa[i][1])
					s+=dataa[i][1][3]
					if(dataa[i][1][4]!='/'):
						s+=dataa[i][1][4]
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
				
				header=[
					'Entry_Code',
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
					'ADD_QUANTITY',
					'ADD_RATE',
					'ADD_AMOUNT',
					'REMARKS',
					'Sub-Total',
					'SGST',
					'CGST',
					'Final-Total'
				]
				i=0
				print("-----------------------------------------")
				while(i<23):
					dictt.update({header[i]:dt[i]})
					i+=1
				data = pd.DataFrame(dictt)
				
				root = tkinter.Tk()
				root.geometry("500x500")
				root.after(1, lambda: focus_force())	
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
				conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
				curr = conn.cursor()
				sql_create = """SELECT * FROM SECOND_SHOP order by entry_code + 0 DESC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				print(dataa)
				
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
			add_qty=0
			if res['add_qty']!='':
                                add_qty = res['add_qty']
			return render_template('admin_edit.html',add_qty=add_qty,res=res,data="0")
		except Exception as err:
			flash(f"Edit Unsuccessful! + {err}",'category1')
			return redirect(url_for('database_operator_open'))

@app.route('/edit_submit', methods=["POST"])
def edit_submit():
	try:
		if session['logged_in_admin']==True and request.method == "POST":
			print("HEREERE")
			try:
				conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
				e = datetime.datetime.now()
				date_time = str(request.form.get('date'))
				print(f'datetime={date_time}')
				cur = conn.cursor()
				#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
				enc = str(request.form.get('enc'))
				
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
				subtotal = float(request.form.get('subtotal'))
				sgst = str(request.form.get('sgst'))
				cgst = str(request.form.get('cgst'))
				finalamount = float(request.form.get('famt'))
				print(am)
				print(subtotal)
				subtotal = str('%.2f' % finalamount)
				
				finalamount = str('%.2f' % finalamount)
				print(finalamount)
				
				sql_create = """INSERT INTO MAIN_SHOP VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
				#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
				#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
				val = (enc,date_time,people,cn,dn,mobile,descrip,sz,ty,cl,dup,qt,rt,am,add_service,add_qty,add_rate,add_amt,remark,subtotal,sgst,cgst,finalamount)
				cur.execute(sql_create,val)
			
				conn.commit()
			
				sql_create = f"""DELETE FROM SECOND_SHOP WHERE date_time='{date_time}'  """
				cur.execute(sql_create)
				cur.close()
				conn.commit()
				flash('Entry Editted & Submitted!','category1')
				return redirect(url_for('database_operator_open'))

			except Exception as err:
				print("error while inserting data:", err)
				flash(f"Error while inserting data! {err}",'category1')
				return redirect(url_for('database_operator_open'))
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
				conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
				curr = conn.cursor()
				sql_create = """SELECT * FROM MAIN_SHOP order by entry_code + 0 DESC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				print(dataa)
				
				curr.close()
				flash(dataa)
				data=[]
				return render_template("database.html")
				
				
			except Exception as err:	
				flash('Admin Database Not Connected')
				print(err)
				d=['','','']
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
				conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
				e = datetime.datetime.now()
				date_time = str(f'{e.day}/{e.month}/{e.year}  :  {e.hour}:{e.minute}:{e.second}')
				
				cur = conn.cursor()
				#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
				
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
				subtotal = float(request.form.get('subtotal'))
				sgst = str(request.form.get('sgst'))
				cgst = str(request.form.get('cgst'))
				finalamount = float(request.form.get('famt'))
				print(finalamount)
				subtotal = '%.2f' % subtotal
				finalamount = '%.2f' % finalamount
				
				print(am)
				sql_create = """INSERT INTO MAIN_SHOP VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
				#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
				#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
				val = (enc,date_time,people,cn,dn,mobile,descrip,sz,ty,cl,dup,qt,rt,am,add_service,add_qty,add_rate,add_amt,remark,subtotal,sgst,cgst,finalamount)
				cur.execute(sql_create,val)
				cur.close()
				conn.commit()
				flash('Entry Submitted!')
				d=['','','']
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
					conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
					e = datetime.datetime.now()
					date_time = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}:{e.second}')
					
					cur = conn.cursor()
					#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
					
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
					sql_create = """INSERT INTO MAIN_SHOP VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
					#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
					#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
					val = (enc,date_time,people,cn,dn,mobile,descrip,sz,ty,cl,dup,qt,rt,am,add_service,add_qty,add_rate,add_amt,remark,subtotal,sgst,cgst,finalamount)
					cur.execute(sql_create,val)
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
		d=['','','']
		return render_template('admin.html',data="0",d=d)


@app.route('/print_delivery_ad_m',methods=['POST'])
def print_delivery_ad_m(): # WORKING ONE
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

	try:
		conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM main_shop WHERE entry_code={enc} """
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print(dataa[0][7])
		sql_create = f"""SELECT dc_code FROM admin_codes"""
		curr.execute(sql_create)
		code = curr.fetchall()
	except Exception as err:
		flash('error')
		return redirect(url_for('database_open'))
    
	desc=[]
	qt=[]
	
	code = int(code[0][0])
	
	for i in range(0,len(dataa)):
		
		desc.append(str(dataa[i][7]+"-"+dataa[i][8]+"-"+dataa[i][9]+"-"+dataa[i][10]))
		qt.append(dataa[i][11])
		rm.append(str(dataa[i][18]))
		
		if(dataa[i][14]!='None'):
			desc.append(dataa[i][14])
			qt.append(dataa[i][15])
		
	data.append(str(operator))
	return render_template("delivery_challan.html",data=data,desc=desc,qt=qt,rm=rm,code=code)


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
		conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
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
			sql_create = f"""SELECT order_code from ORDER_CODES where operator_name = '{operator_name}'"""
			curr.execute(sql_create)
			dat = curr.fetchall()
			print(dat)
			dat = int(dat[0][0])
			print(f'dat{dat}')
			sql_create = f"""SELECT datee from ORDER_CODES where operator_name = '{operator_name}' and datee = '{dt}' """
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


@app.route('/print_retail',methods=['POST'])
def print_retail():
	data=[]
	e = datetime.datetime.now()
	dt = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}') #0
	data.append(dt[:16])
	
	
	cn = change_case(str(request.form.get('c_name'))) #1
	data.append(cn)

	enc = str(request.form.get('enc'))
	data.append(str(request.form.get('mobile'))) #2
	data.append(str(request.form.get('cgst'))) #3
	data.append(str(request.form.get('sgst'))) #4  

	try:
		conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM main_shop WHERE entry_code={enc} """
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print(dataa[0][7])
		sql_create = f"""SELECT retail_code FROM admin_codes"""
		curr.execute(sql_create)
		code = curr.fetchall()
	except Exception as err:
		flash('error')
		return redirect(url_for('database_open'))
    
	desc=[]
	qt=[]
	rt=[]
	amt=[]
	sb=[]
	code = int(code[0][0])
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
	return render_template("retail_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb,code=code)

@app.route('/print_challan',methods=['POST'])
def print_challan():
	data=[]
	e = datetime.datetime.now()
	dt = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}') #0
	data.append(dt[:16])
	
	cn = change_case(str(request.form.get('c_name'))) #1
	data.append(cn)

	enc = str(request.form.get('enc'))
	data.append(str(request.form.get('mobile'))) #2
	data.append(str(request.form.get('cgst'))) #3
	data.append(str(request.form.get('sgst'))) #4  

	try:
		conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM main_shop WHERE entry_code={enc} """
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print(dataa[0][7])
		sql_create = f"""SELECT tax_code FROM admin_codes"""
		curr.execute(sql_create)
		code = curr.fetchall()
	except Exception as err:
		flash('error')
		return redirect(url_for('database_open'))	
    
	desc=[]
	qt=[]
	rt=[]
	amt=[]
	sb=[]
	code = int(code[0][0])
	print(f'code:{code}')
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
	sr=0
	if(len(desc)>8):
		sr=8
	else:
		sr=len(desc)
	
	try:
				conn =  mysql.connector.connect(host='13.240.20.12',user='root',passwd='1902',database='sys')
				curr = conn.cursor()
				sql_create = f"""SELECT GST_NO FROM GST_RECORDS WHERE COMPANY_NAME LIKE '{cn}' """
				curr.execute(sql_create)
				dataa = curr.fetchall()
				print(dataa[0][0])
				print("hehehehe")
				data.append(str(dataa[0][0])) #10
				
				curr.close()
			
				return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb,sr=sr,code=code)
				
				
	except Exception as err:
				dataa=""
				print(f"nooo:{err}")	
				
				data.append(str(dataa))
				return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb,sr=sr,code=code)
	
	
	return render_template("tax_invoice.html",data=data,desc=desc,qt=qt,rt=rt,amt=amt,sb=sb,sr=sr,code=code)



@app.route('/increment_odc',methods=['POST'])
def increment_odc():
	try:
		e = datetime.datetime.now()
		dt = str(f'{e.day}/{e.month}/{e.year}')
		#dt = '31/10/2020'
		conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
		curr = conn.cursor()
		sql_create = f"""SELECT * FROM order_codes where datee like '{dt}%' and  operator_name = '{operator_name}'"""
		curr.execute(sql_create)
		dataa = curr.fetchall()
		print('hello----------------------')
		print(len(dataa))
		if len(dataa) == 0:
			dat=1
			dat=str(dat)
			sql_create = f"""UPDATE ORDER_CODES SET order_code='{dat}',datee='{dt}' where operator_name = '{operator_name}' """
			curr.execute(sql_create)
			conn.commit()
		else:
			sql_create = f"""SELECT order_code from ORDER_CODES where operator_name = '{operator_name}'"""
			curr.execute(sql_create)
			dat = curr.fetchall()
			print(dat)
			dat = int(dat[0][0])
			print(f'dat{dat}')
			dat+=1
			dat=str(dat)
			sql_create = f"""UPDATE ORDER_CODES SET order_code='{dat}' where operator_name = '{operator_name}' """
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
		if session['logged_in']==True:
			try:
				conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
				curr = conn.cursor()
				sql_create = """SELECT * FROM SECOND_SHOP order by entry_code + 0 DESC"""
				curr.execute(sql_create)
				dataa = curr.fetchall()
				print(dataa)
				
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
		con =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
		flash('Operator Database Connected')
		#messagebox.showinfo("DATABASE CONNECTED!", "DATABASE CONNECTED!")
	except Exception as err:
		#messagebox.showerror("Error", "DATABASE NOT CONNECTED!")
		flash('Operator Database Not Connected')	
	

	if not session.get('logged_in'):
		return render_template('operator_login.html')
	else:
		flash('Welcome '+str(operator_name)+"!")
		return redirect(url_for('special_operator'))
	#return render_template("operator_login.html")	
@app.route('/operator',methods=['POST'])
def operator():
	operators={'yogesh':'yogesh','operator2':'operator2','operator2':'operator2'}
	global operator_name
	operator_name = "yogesh"
	
	if operator_name in operators and  request.form['password'] == operators[operator_name]:
		session['logged_in'] = True
		flash('Welcome '+str(operator_name)+"!")
		d=['','','']
		return render_template("operator.html",data="0",d=d)
	else:
		flash('wrong password!')
		return render_template('operator_login.html')
	#return render_template("admin.html")

global CONN_INFO_o 
CONN_INFO_o = {
    'host': 'LAPTOP-8M81CMJL',
    'port': 3306,
    'user': 'operator1',
    'psw': 'operator1',
    'service': 'XE'
}

global CONN_STR_o 
CONN_STR_o = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO_o)

global operator_name
operator_name = "yogesh"

@app.route('/add_job_operator',methods=['POST','GET'])
def adding_job_operator():
	try:
		if session['logged_in']==True and request.method == "POST":
				print("HEREERE")
				try:
					conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
					e = datetime.datetime.now()
					date_time = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}:{e.second}')
					
					cur = conn.cursor()
					#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
					
					people = str(operator_name)

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
					cur.execute(sql_create,(enc,date_time,people,cn,dn,mobile,descrip,sz,ty,cl,dup,qt,add_service,add_qty,remark))
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
			conn =  mysql.connector.connect(host='13.240.20.12',user='operator1',passwd='operator1',database='sys')
			e = datetime.datetime.now()
			date_time = str(f'{e.day}/{e.month}/{e.year}:{e.hour}:{e.minute}:{e.second}')
			cur = conn.cursor()
			#{cn},{dn},{sz},{ty},{cl},{qt},{rt},{am}
			print("hello")
			people = operator_name
			
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
		
		
			sql_create = """INSERT INTO SECOND_SHOP VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
			#:date_time,:people,:cn,:dn,:mobile,:descrip,:sz,:ty,:cl,:qt,:rt,:am,:add_service,:add_size,:add_qty,:add_rate,:add_amt,:subtotal
			#{'date_time':date_time,'people':people,'cn':cn,'dn':dn,'mobile':mobile,'descrip':descrip,'sz':sz,'ty':ty,'cl':cl,'qt':qt,'rt':rt,'am':am,'add_service':add_service,'add_size':add_size,'add_qty':add_qty,'add_rate':add_rate,'add_amt':add_amt,'subtotal':subtotal}
			cur.execute(sql_create,(enc,date_time,people,cn,dn,mobile,descrip,sz,ty,cl,dup,qt,add_service,add_qty,remark))
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
	
