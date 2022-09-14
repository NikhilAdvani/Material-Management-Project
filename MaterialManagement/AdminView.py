from django.shortcuts import render
from . import PoolDict

def AdminLogin(request):
    try:
        result = request.session['ADMIN']
        return render(request, "AdminDashboard.html", {'result': result})
    except Exception as e:
        return render(request,'AdminLogin.html')

def AdminDashboard(request):
   try:
      result = request.session['ADMIN']
      return render(request, "AdminDashboard.html", {'result': result})
   except Exception as e:
      return render(request, 'AdminLogin.html')

def AdminLogout(request):
    del request.session['ADMIN']
    return render(request, "AdminLogin.html")

def CheckAdminLogin(request):
    try:
     emailid=request.POST['emailid']
     password = request.POST['password']

     db, cmd = PoolDict.ConnectionPool()
     q="select * from admins where emailid='{}' and password='{}'".format(emailid,password)
     cmd.execute(q)
     result=cmd.fetchone()
     print(result)
     if(result):
         request.session['ADMIN'] = result
         return render(request, "AdminDashboard.html", {'result': result})
     else:
         return render(request, "AdminLogin.html", {'result': result, 'msg':"Invalid emailid/password"})
     db.close()

    except Exception as e:
      print("Error:",e)
      return render(request, "AdminLogin.html", {'result': {},'msg':'Server Error'})