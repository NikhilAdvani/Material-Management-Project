from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
import uuid
import os

def CategoryInterface(request):
   try:
      result = request.session['ADMIN']
      return render(request, "CategoryInterface.html", {'result': result})
   except Exception as e:
      return render(request, "AdminLogin.html")

def CategorySubmit(request):
    try:
       categoryname=request.POST['categoryname']
       icon=request.FILES['icon']
       filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]

       q="insert into categories(categoryname, categoryicon)values('{}','{}')".format(categoryname, filename)
       db,cmd=Pool.ConnectionPool()
       cmd.execute(q)
       db.commit()

       F=open("C:/Users/Dell/MaterialManagement/assets/"+filename,"wb")
       for chunk in icon.chunks():
          F.write(chunk)
       F.close()

       db.close()
       return render(request, "CategoryInterface.html", {'msg':'Record Submitted Successfully!'})

    except Exception as e:
        print("Error:",e)
        return render(request, "CategoryInterface.html", {'msg':'Failed To Submit Record!'})


def DisplayAll(request):
   try:
      result = request.session['ADMIN']
      db, cmd = Pool.ConnectionPool()
      q = "select * from categories"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return render(request, "DisplayAllCategory.html", {'rows': rows, 'result': result})
   except Exception as e:
      return render(request, "DisplayAllCategory.html", {'rows': []})

def GetCategoriesJSON(request):
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select * from categories"
      cmd.execute(q)
      rows = cmd.fetchall()
      db.close()
      return JsonResponse(rows, safe=False)
   except Exception as e:
      return JsonResponse([], safe=False)

def DisplayById(request):
   catid = request.GET["catid"]
   try:
      db, cmd = Pool.ConnectionPool()
      q = "select * from categories where categoryid={}".format(catid)
      cmd.execute(q)
      row = cmd.fetchone()
      db.close()
      return render(request, "DisplayCategoryById.html", {'row': row})
   except Exception as e:
      return render(request, "DisplayCategoryById.html", {'row': []})

def UpdateCategoryRecord(request):
   btn = request.GET['btn']
   catid = request.GET['catid']
   if(btn=="Edit"):
      categoryname = request.GET['categoryname']
      try:
         db, cmd = Pool.ConnectionPool()
         q = "update categories set categoryname='{}' where categoryid={}".format(categoryname, catid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         return DisplayAll(request)
   elif(btn=="Delete"):
      try:
         db, cmd = Pool.ConnectionPool()
         q="delete from categories where categoryid={}".format(catid)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAll(request)
      except Exception as e:
         return DisplayAll(request)

def EditCategoryIcon(request):
   try:
      catid = request.GET["catid"]
      categoryname = request.GET['categoryname']
      icon = request.GET['icon']
      row=[catid,categoryname,icon]
      return render(request, "EditCategoryIcon.html", {'row': row})
   except Exception as e:
      return render(request, "EditCategoryIcon.html", {'row': []})


def SaveEditIcon(request):
   try:
      catid = request.POST['catid']
      oldicon = request.POST['oldicon']
      icon = request.FILES['icon']
      filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
      q = "update categories set categoryicon='{}' where categoryid={}".format(filename, catid)
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