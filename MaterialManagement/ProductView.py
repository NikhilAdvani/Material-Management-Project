from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
import uuid
import os

def ProductInterface(request):
   try:
      result = request.session['ADMIN']
      return render(request, "ProductInterface.html", {'result':result})
   except Exception as e:
      return render(request, "AdminLogin.html")

def ProductSubmit(request):
    try:
       categoryid=request.POST['categoryid']
       subcategoryid=request.POST['subcategoryid']
       productname=request.POST['productname']
       description = request.POST['description']
       gst = request.POST['gst']

       productpicture=request.FILES['productpicture']
       filename = str(uuid.uuid4()) + productpicture.name[productpicture.name.rfind('.'):]

       q="insert into products(categoryid, subcategoryid, productname, description, gst, picture)values({},{},'{}','{}','{}','{}')".format(categoryid, subcategoryid, productname, description, gst, filename)
       db,cmd=Pool.ConnectionPool()
       cmd.execute(q)
       db.commit()

       F=open("C:/Users/Dell/MaterialManagement/assets/"+filename,"wb")
       for chunk in productpicture.chunks():
          F.write(chunk)
       F.close()

       db.close()
       return render(request, "ProductInterface.html", {'msg':'Record Submitted Successfully!'})

    except Exception as e:
        print("Error:",e)
        return render(request, "ProductInterface.html", {'msg':'Failed To Submit Record!'})

def GetProductsJSON(request):
   try:
      db, cmd = Pool.ConnectionPool()
      subcategoryid = request.GET['subcategoryid']
      q = "select * from products where subcategoryid={}".format(subcategoryid)
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
      q = "select P.*, (select C.categoryname from categories C where C.categoryid=P.categoryid), (select S.subcategoryname from subcategories S where S.subcategoryid=P.subcategoryid) from products P"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllProducts.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllProducts.html", {'rows': []})

def DisplayAllEmp(request):
   try:
      result = request.session['EMPLOYEE']
      db, cmd = Pool.ConnectionPool()
      q = "select P.*, (select C.categoryname from categories C where C.categoryid=P.categoryid), (select S.subcategoryname from subcategories S where S.subcategoryid=P.subcategoryid) from products P"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllProductsEmp.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllProductsEmp.html", {'rows': []})

def DisplayById(request):
   pid = request.GET["pid"]
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select * from products where productid={}".format(pid)
      cmd.execute(q)
      row = cmd.fetchone()
      db.close()
      return render(request, "DisplayProductById.html", {'row': row})
   except Exception as e:
      return render(request, "DisplayProductById.html", {'row': []})

def UpdateProductRecord(request):
   btn = request.GET['btn']
   pid = request.GET["pid"]
   if(btn=="Edit"):
      categoryid = request.GET['categoryid']
      subcategoryid = request.GET['subcategoryid']
      productname = request.GET['productname']
      description = request.GET['description']
      gst = request.GET['gst']
      try:
         db, cmd = Pool.ConnectionPool()
         q = "update products set categoryid={}, subcategoryid={}, productname='{}', description='{}', gst='{}' where productid={}".format(categoryid, subcategoryid, productname, description, gst, pid)
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
         q="delete from products where productid={}".format(pid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         return DisplayAll(request)

def EditProductPicture(request):
   try:
      pid = request.GET["pid"]
      productname = request.GET['productname']
      picture = request.GET['picture']
      row=[pid,productname,picture]
      return render(request, "EditProductPicture.html", {'row': row})
   except Exception as e:
      return render(request, "EditProductPicture.html", {'row': []})


def SaveEditPicture(request):
   try:
      pid = request.POST['pid']
      oldpicture = request.POST['oldpicture']
      picture = request.FILES['picture']
      filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
      q = "update products set picture='{}' where productid={}".format(filename, pid)
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