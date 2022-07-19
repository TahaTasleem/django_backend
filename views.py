from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.db import connections
# Create your views here.
from django.shortcuts import render
from django.apps import apps
import cx_Oracle

from .forms import DeptForm,VisitForm


def connection():
    h = '140.1.20.16' #Your host name/ip
    p = '1576' #Your port number
    sid = 'TEST' #Your sid
    u = 'HPMLVMS' #Your login user name
    pw = 'HPMLVMS202207' #Your login password
    d = cx_Oracle.makedsn(h, p, sid=sid)
    conn = cx_Oracle.connect(user=u, password=pw, dsn=d)
    return conn


def list(request):
    depts = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Department")
    for row in cursor.fetchall():
        depts.append({"id": row[0], "name": row[1]})
    conn.close()
    return render(request, 'abc.html', {'depts':depts})
  

def adddept(request):
    if request.method == 'GET':
        return render(request, 'adddept.html', {'dept':{}})
    if request.method == 'POST':
        form = DeptForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get("id")
            name = form.cleaned_data.get("name")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Department VALUES (:id, :name)", [id, name])
        conn.commit()
        conn.close()
        return redirect('list')

def addvisitor(request):
    if request.method == 'GET':
        return render(request, 'visitorlist.html', {'visit':{}})
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            # id=request.POST['id']
            # name=request.POST['name']
            # organization_name=request.POST['organization_name']
            # purpose= request.POST['purpose']
            # cnic = request.POST['cnic']
            # contact_no=request.POST['contact_no']
            # employee_id=request.POST['employee_id']
            # department_id=request.POST['department_id']
            id1 = form.cleaned_data.get("id1")
            name1 = form.cleaned_data.get("name1")
            organization_name=form.cleaned_data.get("organization_name")
            purpose=form.cleaned_data.get("purpose")
            cnic=form.cleaned_data.get("cnic")
            contact_no=form.cleaned_data.get("contact_no")
            employee_id= form.cleaned_data.get("employee_id")
            department_id=form.cleaned_data.get("department_id")
        conn = connection()
        cursor = conn.cursor()
        sql="INSERT INTO Visit(id,name,organization_name,purpose,cnic,contact_no,employee_id,department_id) VALUES(:id1, :name1,:organization_name,:purpose,:cnic,:contact_no, :employee_id, :department_id )"
        # sql="INSERT INTO Visit(id,name,organization_name,purpose,cnic,contact_no,employee_id,department_id) VALUES(:id1, :name1, :organization_name, :purpose, :cnic, :contact_no, :employee_id, :department_id )"
        cursor.execute(sql, [id1,name1,organization_name,purpose,cnic,contact_no,employee_id,department_id])
        conn.commit()
        conn.close()
        return redirect('list')

def updatedept(request, id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Department WHERE id = :id", [id])
        row = cursor.fetchone()
        cr.append({"id": row[0], "name": row[1]})
        conn.close()
        return render(request, 'adddept.html', {'dept':cr[0]})
    if request.method == 'POST':
        form = DeptForm(request.POST)
        if form.is_valid():
            name = str(form.cleaned_data.get("name"))
            cursor.execute("UPDATE Department SET name = :name WHERE id = :id", [name, id])
            conn.commit()
        conn.close()
        return redirect('list')

def deletedept(request, id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Department WHERE id = :id", [id])
    conn.commit()
    conn.close()
    return redirect('list')