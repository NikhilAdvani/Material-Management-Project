"""MaterialManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import EmployeeView
from . import StateCityView
from . import CategoryView
from . import SubCategoryView
from . import ProductView
from . import FinalProductView
from . import PurchaseView
from . import SupplierView
from . import AdminView
from . import IssueView

urlpatterns = [
    path('admin/', admin.site.urls),

    #Admin
    path('adminlogin/', AdminView.AdminLogin),
    path('admindashboard/', AdminView.AdminDashboard),
    path('checkadminlogin', AdminView.CheckAdminLogin),
    path('adminlogout/', AdminView.AdminLogout),

    #Employee
    path('employeedashboard/', EmployeeView.EmployeeDashboard),
    path('employeelogin/', EmployeeView.EmployeeLogin),
    path('checkemployeelogin', EmployeeView.CheckEmployeeLogin),
    path('employeelogout/', EmployeeView.EmployeeLogout),
    path('employeeinterface/', EmployeeView.EmployeeInterface),
    path('employeesubmit', EmployeeView.EmployeeSubmit),
    path('displayallemployee/', EmployeeView.DisplayAll),
    path('displayemployeebyid/', EmployeeView.DisplayById),
    path('updaterecord/', EmployeeView.UpdateRecord),
    path('editemployeepicture/', EmployeeView.EditEmployeePicture),
    path('saveeditpicture', EmployeeView.SaveEditPicture),
    path('getemployeejson/', EmployeeView.GetEmployeeJSON),

    #StateCity
    path('fetchallstates/', StateCityView.FetchAllStates),
    path('fetchallcities/', StateCityView.FetchAllCities),

    #Supplier
    path('supplierinterface/', SupplierView.SupplierInterface),
    path('suppliersubmit/', SupplierView.SupplierSubmit),
    path('displayallsupplier/', SupplierView.DisplayAll),
    path('getsupplierjson/', SupplierView.GetSupplierJSON),

    #Category
    path('categoryinterface/', CategoryView.CategoryInterface),
    path('categorysubmit', CategoryView.CategorySubmit),
    path('displayallcategory/', CategoryView.DisplayAll),
    path('displaycategorybyid/', CategoryView.DisplayById),
    path('getcategoriesjson/', CategoryView.GetCategoriesJSON),
    path('updatecategoryrecord/', CategoryView.UpdateCategoryRecord),
    path('editcategoryicon/', CategoryView.EditCategoryIcon),
    path('saveeditcategoryicon', CategoryView.SaveEditIcon),

    #SubCategory
    path('subcategoryinterface/', SubCategoryView.SubCategoryInterface),
    path('subcategorysubmit', SubCategoryView.SubCategorySubmit),
    path('displayallsubcategory/', SubCategoryView.DisplayAll),
    path('displaysubcategorybyid/', SubCategoryView.DisplayById),
    path('getsubcategoriesjson/', SubCategoryView.GetSubCategoriesJSON),
    path('updatesubcategoryrecord/', SubCategoryView.UpdateSubCategoryRecord),
    path('editsubcategoryicon/', SubCategoryView.EditSubCategoryIcon),
    path('saveeditsubcategoryicon', SubCategoryView.SaveEditIcon),

    #Product
    path('productinterface/', ProductView.ProductInterface),
    path('productsubmit', ProductView.ProductSubmit),
    path('displayallproducts/', ProductView.DisplayAll),
    path('displayproductbyid/', ProductView.DisplayById),
    path('getproductsjson/', ProductView.GetProductsJSON),
    path('updateproductrecord/', ProductView.UpdateProductRecord),
    path('editproductpicture/', ProductView.EditProductPicture),
    path('saveeditproductpicture', ProductView.SaveEditPicture),
    path('displayallproductsemp', ProductView.DisplayAllEmp),

    #FinalProduct
    path('finalproductinterface/', FinalProductView.FinalProductInterface),
    path('finalproductsubmit', FinalProductView.FinalProductSubmit),
    path('displayallfinalproducts/', FinalProductView.DisplayAll),
    path('displayallfinalproductsemp/', FinalProductView.DisplayAllEmp),
    path('displayfinalproductbyid/', FinalProductView.DisplayById),
    path('displayfinalproductbyidjson/', FinalProductView.DisplayByIdJSON),
    path('displayallfinalproductsjson/', FinalProductView.DisplayAllFinalProductJSON),
    path('displayupdatedstock/', FinalProductView.DisplayUpdatedStock),
    path('getfinalproductsjson/', FinalProductView.GetFinalProductsJSON),
    path('updatefinalproductrecord/', FinalProductView.UpdateFinalProductRecord),
    path('editfinalproductpicture/', FinalProductView.EditFinalProductPicture),
    path('saveeditfinalproductpicture', FinalProductView.SaveEditPicture),

    #Purchase
    path('purchaseinterface/', PurchaseView.PurchaseInterface),
    path('purchaseinterfaceemp/', PurchaseView.PurchaseInterfaceEmp),
    path('purchasesubmit/', PurchaseView.PurchaseSubmit),
    path('displayallpurchase/', PurchaseView.DisplayAll),
    path('displayallpurchaseemp/', PurchaseView.DisplayAllEmp),
    path('displayallpurchasejson/', PurchaseView.DisplayAllPurchaseJSON),
    path('displaypurchasebyid/', PurchaseView.DisplayById),
    path('getpurchasesjson/', PurchaseView.GetPurchasesJSON),
    path('updatepurchaserecord/', PurchaseView.UpdatePurchaseRecord),
    path('purchasereport/', PurchaseView.PurchaseReport),
    path('displayallpurchasejson/', PurchaseView.DisplayAllPurchaseJSON),

    #Issue
    path('issueinterface/', IssueView.IssueInterface),
    path('issuesubmit/', IssueView.IssueSubmit),
    path('displayallissue/', IssueView.DisplayAll),
    path('updateissuerecord/', IssueView.UpdateIssueRecord),
    path('issuereport/', IssueView.IssueReport),
    path('displayallissuejson/', IssueView.DisplayAllIssueJSON),

]
