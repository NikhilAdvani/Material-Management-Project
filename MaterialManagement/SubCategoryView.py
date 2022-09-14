from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
import uuid
import os

def SubCategoryInterface(request):
   try:
      result = request.session['ADMIN']
      return render(request, "SubCategoryInterface.html", {'result': result})
   except Exception as e:
      return render(request, "AdminLogin.html")

def SubCategorySubmit(request):
    try:
       categoryid=request.POST['categoryid']
       subcategoryname=request.POST['subcategoryname']
       description = request.POST['description']

       icon2=request.FILES['icon2']
       filename = str(uuid.uuid4()) + icon2.name[icon2.name.rfind('.'):]

       q="insert into subcategories(categoryid, subcategoryname, description, icon)values({},'{}','{}','{}')".format(categoryid, subcategoryname, description, filename)
       db,cmd=Pool.ConnectionPool()
       cmd.execute(q)
       db.commit()

       F=open("C:/Users/Dell/MaterialManagement/assets/"+filename,"wb")
       for chunk in icon2.chunks():
          F.write(chunk)
       F.close()

       db.close()
       return render(request, "SubCategoryInterface.html", {'msg':'Record Submitted Successfully!'})

    except Exception as e:
        return render(request, "SubCategoryInterface.html", {'msg':'Failed To Submit Record!'})


def DisplayAll(request):
   try:
      result = request.session['ADMIN']
      db, cmd = Pool.ConnectionPool()
      q = "select S.*, (select C.categoryname from categories C where C.categoryid=S.categoryid) from subcategories S"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllSubCategory.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllSubCategory.html", {'rows': []})

def GetSubCategoriesJSON(request):
   try:
      db, cmd = Pool.ConnectionPool()
      categoryid = request.GET['categoryid']
      q = "select * from subcategories where categoryid={}".format(categoryid)
      print(q)
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return JsonResponse(rows, safe=False)
   except Exception as e:
      return JsonResponse([], safe=False)


def DisplayById(request):
   scatid = request.GET["scatid"]
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select * from subcategories where subcategoryid={}".format(scatid)
      cmd.execute(q)
      row = cmd.fetchone()
      db.close()
      return render(request, "DisplaySubCategoryById.html", {'row': row})
   except Exception as e:
      return render(request, "DisplaySubCategoryById.html", {'row': []})

def UpdateSubCategoryRecord(request):
   btn = request.GET['btn']
   scatid = request.GET['scatid']
   if(btn=="Edit"):
      categoryid = request.GET['categoryid']
      subcategoryname = request.GET['subcategoryname']
      description = request.GET['description']
      try:
         db, cmd = Pool.ConnectionPool()
         q = "update subcategories set categoryid={}, subcategoryname='{}', description='{}' where subcategoryid={}".format(categoryid, subcategoryname, description, scatid)
         print(q)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         print(e)
         return DisplayAll(request)
   elif(btn=="Delete"):
      try:
         db, cmd = Pool.ConnectionPool()
         q="delete from subcategories where subcategoryid={}".format(scatid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         return DisplayAll(request)

def EditSubCategoryIcon(request):
   try:
      scatid = request.GET["scatid"]
      subcategoryname = request.GET['subcategoryname']
      icon = request.GET['icon']
      row=[scatid,subcategoryname,icon]
      return render(request, "EditSubCategoryIcon.html", {'row': row})
   except Exception as e:
      return render(request, "EditSubCategoryIcon.html", {'row': []})


def SaveEditIcon(request):
   try:
      scatid = request.POST['scatid']
      oldicon = request.POST['oldicon']
      icon = request.FILES['icon']
      filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
      q = "update subcategories set icon='{}' where subcategoryid={}".format(filename, scatid)
      print(q)
      db, cmd = Pool.ConnectionPool()
      cmd.execute(q)
      db.commit()
      F = open("C:/Users/Dell/MaterialManagement/assets/"+filename,"wb")
      for chunk in icon.chunks():
         F.write(chunk)
      F.close()
      db.close()
      os.remove('C:/Users/Dell/MaterialManagement/assets/' + oldicon)
      return DisplayAll(request)
   except Exception as e:
      return DisplayAll(request)