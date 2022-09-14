from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
from . import PoolDict
import uuid
import os

def FinalProductInterface(request):
    try:
        result = request.session['ADMIN']
        return render(request, "FinalProductInterface.html", {'result': result})
    except Exception as e:
        return render(request, "AdminLogin.html")

def FinalProductSubmit(request):
    try:
       categoryid=request.POST['categoryid']
       subcategoryid=request.POST['subcategoryid']
       productid=request.POST['productid']
       finalproductname=request.POST['finalproductname']
       size=request.POST['size']
       sizeunit=request.POST['sizeunit']
       weight=request.POST['weight']
       weightunit=request.POST['weightunit']
       color=request.POST['color']
       price=request.POST['price']
       stock=request.POST['stock']

       finalproductpicture=request.FILES['finalproductpicture']
       filename = str(uuid.uuid4()) + finalproductpicture.name[finalproductpicture.name.rfind('.'):]

       q="insert into finalproducts(categoryid, subcategoryid, productid, finalproductname, size, size_unit, weight, weight_unit, color, price, stock, picture)values({},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(categoryid, subcategoryid, productid, finalproductname, size, sizeunit, weight, weightunit, color, price, stock, filename)
       db,cmd=Pool.ConnectionPool()
       cmd.execute(q)
       db.commit()

       F=open("C:/Users/Dell/MaterialManagement/assets/"+filename,"wb")
       for chunk in finalproductpicture.chunks():
          F.write(chunk)
       F.close()

       db.close()
       return render(request, "FinalProductInterface.html", {'msg':'Record Submitted Successfully!'})

    except Exception as e:
        print("Error:",e)
        return render(request, "FinalProductInterface.html", {'msg':'Failed To Submit Record!'})

def GetFinalProductsJSON(request):
   try:
      db, cmd = Pool.ConnectionPool()
      productid = request.GET['productid']
      q = "select * from finalproducts where productid={}".format(productid)
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
      q = "select F.*, (select C.categoryname from categories C where C.categoryid=F.categoryid), (select S.subcategoryname from subcategories S where S.subcategoryid=F.subcategoryid), (select P.productname from products P where P.productid=F.productid) from finalproducts F"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllFinalProducts.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllFinalProducts.html", {'rows': []})

def DisplayAllEmp(request):
   try:
      result = request.session['EMPLOYEE']
      db, cmd = Pool.ConnectionPool()
      q = "select F.*, (select C.categoryname from categories C where C.categoryid=F.categoryid), (select S.subcategoryname from subcategories S where S.subcategoryid=F.subcategoryid), (select P.productname from products P where P.productid=F.productid) from finalproducts F"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllFinalProductsEmp.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllFinalProductsEmp.html", {'rows': []})

def DisplayById(request):
   fpid = request.GET["fpid"]
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select * from finalproducts where finalproductid={}".format(fpid)
      cmd.execute(q)
      row = cmd.fetchone()
      db.close()
      return render(request, "DisplayFinalProductById.html", {'row': row})
   except Exception as e:
      return render(request, "DisplayFinalProductById.html", {'row': []})

def DisplayByIdJSON(request):
   finalproductid = request.GET["finalproductid"]
   try:
      db, cmd = PoolDict.ConnectionPool()
      q = "select * from finalproducts where finalproductid={}".format(finalproductid)
      cmd.execute(q)
      row = cmd.fetchone()
      db.close()
      return JsonResponse(row, safe=False)
   except Exception as e:
       return JsonResponse([], safe=False)

def DisplayUpdatedStock(request):
    return render(request, "ListProductsEmployee.html")

def DisplayAllFinalProductJSON(request):
    pattern = request.GET['pattern']
    try:
        dbe, cmd = PoolDict.ConnectionPool()
        q = "select FP.*,(select C.categoryname from categories C where C.categoryid = FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid), (select P.productname from products P where P.productid = FP.productid) from finalproducts FP where finalproductname like '%{}%'".format(pattern)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def UpdateFinalProductRecord(request):
   btn = request.GET['btn']
   fpid = request.GET["fpid"]
   if(btn=="Edit"):
       categoryid = request.GET['categoryid']
       subcategoryid = request.GET['subcategoryid']
       productid = request.GET['productid']
       finalproductname = request.GET['finalproductname']
       size = request.GET['size']
       size_unit = request.GET['sizeunit']
       weight = request.GET['weight']
       weight_unit = request.GET['weightunit']
       color = request.GET['color']
       price = request.GET['price']
       stock = request.GET['stock']
       try:
         db, cmd = Pool.ConnectionPool()
         q = "update finalproducts set categoryid={}, subcategoryid={}, productid={}, finalproductname='{}',size='{}', size_unit='{}', weight='{}', weight_unit='{}', color='{}', price='{}', stock='{}' where finalproductid={}".format(categoryid, subcategoryid, productid, finalproductname, size, size_unit, weight, weight_unit, color, price, stock, fpid)
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
         q="delete from finalproducts where finalproductid={}".format(fpid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         print("Error:", e)
         return DisplayAll(request)

def EditFinalProductPicture(request):
   try:
      fpid = request.GET["fpid"]
      finalproductname = request.GET['finalproductname']
      picture = request.GET['picture']
      row=[fpid,finalproductname,picture]
      return render(request, "EditFinalProductPicture.html", {'row': row})
   except Exception as e:
      return render(request, "EditFinalProductPicture.html", {'row': []})


def SaveEditPicture(request):
   try:
      fpid = request.POST['fpid']
      oldpicture = request.POST['oldpicture']
      picture = request.FILES['picture']
      filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
      q = "update finalproducts set picture='{}' where finalproductid={}".format(filename, fpid)
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