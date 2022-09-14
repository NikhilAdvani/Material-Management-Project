from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
from . import PoolDict

def IssueInterface(request):
   try:
      result = request.session['EMPLOYEE']
      return render(request, "IssueInterface.html", {'result':result})
   except Exception as e:
      return render(request, "EmployeeLogin.html")


def IssueSubmit(request):
    try:
       employeeid = request.GET['employeeid']
       demandemployeeid = request.GET['demandemployeeid']
       categoryid=request.GET['categoryid']
       subcategoryid=request.GET['subcategoryid']
       productid=request.GET['productid']
       finalproductid=request.GET['finalproductid']
       dateofissue = request.GET['dateofissue']
       qtyissue = request.GET['qtyissue']
       remark = request.GET['remark']

       q="insert into issue(employeeid, demand_employeeid, categoryid, subcategoryid, productid, finalproductid, dateofissue, qtyissue, remark)values({},{},{},{},{},{},'{}',{},'{}')".format(employeeid, demandemployeeid, categoryid, subcategoryid, productid, finalproductid, dateofissue, qtyissue, remark)
       db,cmd=Pool.ConnectionPool()
       cmd.execute(q)

       #Update Stock
       q = "update finalproducts set stock=stock-{} where finalproductid={}".format(qtyissue, finalproductid)
       cmd.execute(q)

       db.commit()
       db.close()
       return render(request, "IssueInterface.html", {'msg':'Record Submitted Successfully!'})

    except Exception as e:
        print("Error:",e)
        return render(request, "IssueInterface.html", {'msg':'Failed To Submit Record!'})


def DisplayAll(request):
   try:
      result = request.session['EMPLOYEE']
      db, cmd = Pool.ConnectionPool()
      q = "select R.*, (select E.firstname from employee E where E.employeeid=R.employeeid),(select E.lastname from employee E where E.employeeid=R.employeeid), (select E.firstname from employee E where E.employeeid=R.demand_employeeid),(select E.lastname from employee E where E.employeeid=R.demand_employeeid), (select C.categoryname from categories C where C.categoryid=R.categoryid), (select S.subcategoryname from subcategories S where S.subcategoryid=R.subcategoryid), (select P.productname from products P where P.productid=R.productid), (select F.finalproductname from finalproducts F where F.finalproductid=R.finalproductid) from issue R"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllIssue.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllIssue.html", {'rows': []})


def UpdateIssueRecord(request):
   btn = request.GET['btn']
   issueid = request.GET["issueid"]
   if(btn=="Edit"):
      employeeid = request.GET['employeeid']
      demandemployeeid = request.GET['demandemployeeid']
      categoryid = request.GET['categoryid']
      subcategoryid = request.GET['subcategoryid']
      productid = request.GET['productid']
      finalproductid = request.GET['finalproductid']
      dateofissue = request.GET['dateofissue']
      qtyissue = request.GET['qtyissue']
      remark = request.GET['remark']
      try:
         db, cmd = Pool.ConnectionPool()
         q = "update issue set employeeid = {}, demand_employeeid = {}, categoryid = {}, subcategoryid = {}, productid = {}, finalproductid = {}, dateofissue = '{}', qtyissue = {}, remark = '{}' where issueid = {}".format(employeeid, demandemployeeid, categoryid, subcategoryid, productid, finalproductid, dateofissue, qtyissue, remark, issueid)
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
         q="delete from issue where issueid={}".format(issueid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         return DisplayAll(request)

def IssueReport(request):
   try:
      result = request.session['EMPLOYEE']
      return render(request, "IssueReport.html", {'result': result})
   except Exception as e:
      return render(request, 'EmployeeLogin.html')


def DisplayAllIssueJSON(request):
   fromdate = request.GET['fromdate']
   todate = request.GET['todate']
   try:
      dbe, cmd = PoolDict.ConnectionPool()
      # q = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid) as categoryname,(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid) as subcategoryname, (select P.productname from products P where P.productid = PP.productid) as productname, (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid) as finalproductname, (select S.suppliername from supplier S where S.supplierid = PP.supplierid) as suppliername from purchase PP where datepurchase between '{}' and '{}'".format(fromdate,todate)
      q = "select IP.*,(select C.categoryname from categories C where C.categoryid = IP.categoryid) as categoryname,(select S.subcategoryname from subcategories S where S.subcategoryid = IP.subcategoryid) as subcategoryname, (select P.productname from products P where P.productid = IP.productid) as productname, (select FP.finalproductname from finalproducts FP where FP.finalproductid = IP.finalproductid) as finalproductname, (select E.firstname from employee E where E.employeeid = IP.demand_employeeid) as dfname, (select E.lastname from employee E where E.employeeid = IP.demand_employeeid) as dlname,(select E.firstname from employee E where E.employeeid = IP.employeeid) as fname, (select E.lastname from employee E where E.employeeid = IP.employeeid) as lname from issue IP where dateofissue between '{}' and '{}'".format(
         fromdate, todate)
      cmd.execute(q)
      rows = cmd.fetchall()
      dbe.close()
      return JsonResponse(rows, safe=False)
   except Exception as e:
      print(e)
      return JsonResponse([], safe=False)
