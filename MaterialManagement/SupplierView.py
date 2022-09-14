from django.shortcuts import render
from django.http import JsonResponse
from . import Pool

def SupplierInterface(request):
   try:
      result = request.session['ADMIN']
      return render(request, "SupplierInterface.html", {'result': result})
   except Exception as e:
      return render(request, "AdminLogin.html")

def SupplierSubmit(request):
    try:
       suppliername = request.GET['suppliername']
       firmname = request.GET['firmname']
       contactno = request.GET['contactno']
       emailid = request.GET['emailid']
       address = request.GET['address']
       state = request.GET['state']
       city = request.GET['city']

       q="insert into supplier(suppliername, firmname, contactno, emailid, address, state, city)values('{}','{}','{}','{}','{}','{}','{}')".format(suppliername, firmname, contactno, emailid, address, state, city)
       db,cmd=Pool.ConnectionPool()
       cmd.execute(q)
       db.commit()
       db.close()
       return render(request, "SupplierInterface.html", {'msg':'Record Submitted Successfully!'})

    except Exception as e:
        print("Error:",e)
        return render(request, "SupplierInterface.html", {'msg':'Failed To Submit Record!'})

def GetSupplierJSON(request):
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select * from supplier"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return JsonResponse(rows, safe=False)
   except Exception as e:
      return JsonResponse([], safe=False)

def DisplayAll(request):
   try:
      result = request.session['ADMIN']
      db, cmd = Pool.ConnectionPool()
      q = "select E.*, (select C.cityname from cities C where C.cityid=E.city), (select S.statename from states S where S.stateid=E.state) from supplier E"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllSuppliers.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllSuppliers.html", {'rows': []})