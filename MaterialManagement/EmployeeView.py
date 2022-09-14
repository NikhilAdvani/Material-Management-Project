from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
from . import PoolDict
from . import SendSms
from . import EmailService
import uuid
import random
import os

def EmployeeDashboard(request):
   try:
      result = request.session['EMPLOYEE']
      return render(request, "EmployeeDashboard.html", {'result': result})
   except Exception as e:
      return render(request, 'EmployeeLogin.html')

def EmployeeLogin(request):
   try:
      result = request.session['EMPLOYEE']
      return render(request, "EmployeeDashboard.html", {'result': result})
   except Exception as e:
      return render(request, 'EmployeeLogin.html')


def CheckEmployeeLogin(request):
   try:
      email = request.POST['emailid']
      password = request.POST['password']

      db, cmd = PoolDict.ConnectionPool()
      q = "select * from employee where email='{}' and password='{}'".format(email, password)
      print(q)
      cmd.execute(q)
      result = cmd.fetchone()
      print(result)
      if (result):
         request.session['EMPLOYEE'] = result
         return render(request, "EmployeeDashboard.html", {'result': result})
      else:
         return render(request, "EmployeeLogin.html", {'result': result, 'msg': "Invalid emailid/password"})
      db.close()

   except Exception as e:
      print("Error:", e)
      return render(request, "EmployeeLogin.html", {'result': {}, 'msg': 'Server Error'})


def EmployeeLogout(request):
   del request.session['EMPLOYEE']
   return render(request, "EmployeeLogin.html")

def EmployeeInterface(request):
   try:
      result = request.session['ADMIN']
      return render(request, "EmployeeInterface.html", {'result': result})
   except Exception as e:
      return render(request, "AdminLogin.html")

def GetEmployeeJSON(request):
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select * from employee"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return JsonResponse(rows, safe=False)
   except Exception as e:
      return JsonResponse([], safe=False)

def EmployeeSubmit(request):
    try:
       firstname=request.POST['firstname']
       lastname = request.POST['lastname']
       gender = request.POST['gender']
       birthdate = request.POST['birthdate']
       paddress = request.POST['paddress']
       state = request.POST['state']
       city = request.POST['city']
       caddress = request.POST['caddress']
       emailaddress = request.POST['emailaddress']
       mobilenumber = request.POST['mobilenumber']
       designation=request.POST['designation']

       picture=request.FILES['picture']
       filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
       password = "".join(random.sample(['1', 'a', '4', 'x', '6', '66', '#', '@'], k=7))

       q="insert into employee(firstname, lastname, gender, dob, paddress, stateid, cityid, caddress, email, mobileno, designation, picture, password)values('{}','{}','{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}')".format(firstname, lastname, gender, birthdate, paddress, state, city, caddress, emailaddress, mobilenumber, designation, filename, password)
       db,cmd=Pool.ConnectionPool()
       cmd.execute(q)
       db.commit()

       F=open("C:/Users/Dell/MaterialManagement/assets/"+filename,"wb")
       for chunk in picture.chunks():
          F.write(chunk)
       F.close()

       db.close()
       #SendSms.SendMessage("Hi! {}, your password is {}".format(firstname, password), mobilenumber)
       #EmailService.SendMail(emailaddress, "Hi {}!, your password is {}".format(firstname, password))
       EmailService.SendHTMLMail(emailaddress, "Hi {}!, your password is {}".format(firstname, password))
       return render(request, "EmployeeInterface.html", {'msg':'Record Submitted Successfully!'})

    except Exception as e:
        print("Error:", e)
        return render(request, "EmployeeInterface.html", {'msg':'Failed To Submit Record!'})

def DisplayAll(request):
   try:
      result = request.session['ADMIN']
      db, cmd = Pool.ConnectionPool()
      q = "select E.*, (select C.cityname from cities C where C.cityid=E.cityid), (select S.statename from states S where S.stateid=E.stateid) from employee E"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllEmployee.html", {'rows': rows,'result': result})
   except Exception as e:
      return render(request, "DisplayAllEmployee.html", {'rows': []})

def DisplayById(request):
   empid = request.GET["empid"]
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select E.*, (select C.cityname from cities C where C.cityid=E.cityid), (select S.statename from states S where S.stateid=E.stateid) from employee E where employeeid={}".format(empid)
      cmd.execute(q)
      row = cmd.fetchone()
      db.close()
      return render(request, "DisplayEmployeeById.html", {'row': row})
   except Exception as e:
      return render(request, "DisplayEmployeeById.html", {'row': []})

def UpdateRecord(request):
   btn = request.GET['btn']
   empid = request.GET["empid"]
   if(btn=="Edit"):
      firstname = request.GET['firstname']
      lastname = request.GET['lastname']
      gender = request.GET['gender']
      birthdate = request.GET['birthdate']
      paddress = request.GET['paddress']
      state = request.GET['state']
      city = request.GET['city']
      caddress = request.GET['caddress']
      emailaddress = request.GET['emailaddress']
      mobilenumber = request.GET['mobilenumber']
      designation = request.GET['designation']
      try:
         db, cmd = Pool.ConnectionPool()
         q = "update employee set firstname='{}', lastname='{}', gender='{}', dob='{}', paddress='{}', stateid={}, cityid={}, caddress='{}', email='{}', mobileno='{}', designation='{}' where employeeid={}".format(firstname, lastname, gender, birthdate, paddress, state, city, caddress, emailaddress, mobilenumber, designation, empid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         return DisplayAll(request)
   elif(btn=="Delete"):
      try:
         db, cmd = Pool.ConnectionPool()
         q="delete from employee where employeeid={}".format(empid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         return DisplayAll(request)

def EditEmployeePicture(request):
   try:
      empid = request.GET["empid"]
      firstname = request.GET['firstname']
      lastname = request.GET['lastname']
      picture = request.GET['picture']
      row=[empid,firstname,lastname,picture]
      return render(request, "EditEmployeePicture.html", {'row': row})
   except Exception as e:
      return render(request, "EditEmployeePicture.html", {'row': []})


def SaveEditPicture(request):
   try:
      empid = request.POST['empid']
      oldpicture = request.POST['oldpicture']
      picture = request.FILES['picture']
      filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
      q = "update employee set picture='{}' where employeeid={}".format(filename, empid)
      print(q)
      db, cmd = Pool.ConnectionPool()
      cmd.execute(q)
      db.commit()
      F = open("C:/Users/Dell/MaterialManagement/assets/"+filename,"wb")
      for chunk in picture.chunks():
         F.write(chunk)
      F.close()
      db.close()
      os.remove('C:/Users/Dell/MaterialManagement/assets/' + oldpicture)
      return DisplayAll(request)
   except Exception as e:
      return DisplayAll(request)



