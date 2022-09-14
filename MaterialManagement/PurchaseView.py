from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
from . import PoolDict
import uuid
import os

def PurchaseInterface(request):
   try:
      result = request.session['ADMIN']
      return render(request, "PurchaseInterface.html", {'result':result})
   except Exception as e:
      return render(request, "AdminLogin.html")

def PurchaseInterfaceEmp(request):
   try:
      result = request.session['EMPLOYEE']
      return render(request, "PurchaseInterfaceEmp.html", {'result':result})
   except Exception as e:
      return render(request, "EmployeeLogin.html")


def DisplayAllPurchaseJSON(request):
   fromdate = request.GET['fromdate']
   todate = request.GET['todate']
   try:
      dbe, cmd = PoolDict.ConnectionPool()
      q = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid) as categoryname,(select S.subcategoryname from subcategories S where S.subcategoryid = PP.subcategoryid) as subcategoryname, (select P.productname from products P where P.productid = PP.productid) as productname, (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid) as finalproductname, (select S.suppliername from supplier S where S.supplierid = PP.supplierid) as suppliername from purchase PP where dateofpurchase between '{}' and '{}'".format(
         fromdate, todate)
      cmd.execute(q)
      rows = cmd.fetchall()
      dbe.close()
      return JsonResponse(rows, safe=False)
   except Exception as e:
      print(e)
      return JsonResponse([], safe=False)

def PurchaseReport(request):
   try:
      result = request.session['EMPLOYEE']
      return render(request, "PurchaseReport.html", {'result': result})
   except Exception as e:
      return render(request, 'EmployeeLogin.html')

def PurchaseSubmit(request):
    try:
       employeeid = request.GET['employeeid']
       categoryid=request.GET['categoryid']
       subcategoryid=request.GET['subcategoryid']
       productid=request.GET['productid']
       finalproductid=request.GET['finalproductid']
       supplierid=request.GET['supplierid']
       dateofpurchase = request.GET['dateofpurchase']
       stock = request.GET['stock']
       amount = request.GET['amount']

       q = "insert into purchase(employeeid, categoryid, subcategoryid, productid, finalproductid, supplierid, dateofpurchase, stock, amount)values({},{},{},{},{},{},'{}','{}','{}')".format(employeeid, categoryid, subcategoryid, productid, finalproductid, supplierid, dateofpurchase, stock, amount)
       db,cmd=Pool.ConnectionPool()
       cmd.execute(q)
       #Update Stock
       q = "update finalproducts set price=((price+{})/2), stock=stock+{} where finalproductid={}".format(amount, stock, finalproductid)
       cmd.execute(q)
       db.commit()
       db.close()
       return render(request, "PurchaseInterfaceEmp.html", {'msg':'Record Submitted Successfully!'})

    except Exception as e:
        print("Error:",e)
        return render(request, "PurchaseInterfaceEmp.html", {'msg':'Failed To Submit Record!'})

def GetPurchasesJSON(request):
   try:
      db, cmd = Pool.ConnectionPool()
      supplierid = request.GET['supplierid']
      q = "select * from purchase where supplierid={}".format(supplierid)
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return JsonResponse(rows, safe=False)
   except Exception as e:
      return JsonResponse([], safe=False)


def DisplayAll(request):
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select R.*, (select E.firstname from employee E where E.employeeid=R.employeeid),(select E.lastname from employee E where E.employeeid=R.employeeid), (select Q.firmname from supplier Q where Q.supplierid=R.supplierid), (select C.categoryname from categories C where C.categoryid=R.categoryid), (select S.subcategoryname from subcategories S where S.subcategoryid=R.subcategoryid), (select P.productname from products P where P.productid=R.productid), (select F.finalproductname from finalproducts F where F.finalproductid=R.finalproductid) from purchase R"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllPurchase.html", {'rows': rows})
   except Exception as e:
      return render(request, "DisplayAllPurchase.html", {'rows': []})

def DisplayAllEmp(request):
   try:
      result = request.session['EMPLOYEE']
      db, cmd = Pool.ConnectionPool()
      q = "select R.*, (select E.firstname from employee E where E.employeeid=R.employeeid),(select E.lastname from employee E where E.employeeid=R.employeeid), (select Q.firmname from supplier Q where Q.supplierid=R.supplierid), (select C.categoryname from categories C where C.categoryid=R.categoryid), (select S.subcategoryname from subcategories S where S.subcategoryid=R.subcategoryid), (select P.productname from products P where P.productid=R.productid), (select F.finalproductname from finalproducts F where F.finalproductid=R.finalproductid) from purchase R"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllPurchaseEmp.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllPurchaseEmp.html", {'rows': []})

def DisplayById(request):
   transactionid = request.GET["transactionid"]
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select * from purchase where transactionid={}".format(transactionid)
      cmd.execute(q)
      row = cmd.fetchone()
      db.close()
      return render(request, "DisplayPurchaseById.html", {'row': row})
   except Exception as e:
      return render(request, "DisplayPurchaseById.html", {'row': []})

def UpdatePurchaseRecord(request):
   btn = request.GET['btn']
   transactionid = request.GET["transactionid"]
   if(btn=="Edit"):
      employeeid = request.GET['employeeid']
      categoryid = request.GET['categoryid']
      subcategoryid = request.GET['subcategoryid']
      productid = request.GET['productid']
      finalproductid = request.GET['finalproductid']
      supplierid = request.GET['supplierid']
      dateofpurchase = request.GET['dateofpurchase']
      stock = request.GET['stock']
      amount = request.GET['amount']
      try:
         db, cmd = Pool.ConnectionPool()
         q = "update purchase set employeeid={}, categoryid={}, subcategoryid={}, productid={}, finalproductid={}, supplierid={}, dateofpurchase='{}', stock='{}', amount='{}' where transactionid={}".format(employeeid, categoryid, subcategoryid, productid, finalproductid, supplierid, dateofpurchase, stock, amount, transactionid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         print("Error:",e)
         return DisplayAll(request)
   elif(btn=="Delete"):
      try:
         db, cmd = Pool.ConnectionPool()
         q="delete from purchase where transactionid={}".format(transactionid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         return DisplayAll(request)