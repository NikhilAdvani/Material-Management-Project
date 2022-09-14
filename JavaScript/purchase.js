$(document).ready(function(){
 $.getJSON("/getcategoriesjson",{ajax:true},function(data){
  $.each(data,function(index,item){
    $('#categoryid').append($('<option>').text(item[1]).val(item[0]))
    })
 })

$('#categoryid').change(function(){
 $.getJSON("/getsubcategoriesjson",{ajax:true, categoryid:$('#categoryid').val()},function(data){
  $('#subcategoryid').empty()
  $('#subcategoryid').append($('<option>').text('-Sub-Category-'))
  $.each(data,function(index,item){
    $('#subcategoryid').append($('<option>').text(item[2]).val(item[1]))
  })
 })
 })

 $('#subcategoryid').change(function(){
 $.getJSON("/getproductsjson",{ajax:true, subcategoryid:$('#subcategoryid').val()},function(data){
  $('#productid').empty()
  $('#productid').append($('<option>').text('-Product-'))
  $.each(data,function(index,item){
    $('#productid').append($('<option>').text(item[3]).val(item[2]))
  })
 })
 })

 $('#productid').change(function(){
 $.getJSON("/getfinalproductsjson",{ajax:true, productid:$('#productid').val()},function(data){
  $('#finalproductid').empty()
  $('#finalproductid').append($('<option>').text('-Product-'))
  $.each(data,function(index,item){
    $('#finalproductid').append($('<option>').text(item[4]).val(item[3]))
  })
 })
 })

 $.getJSON("/getsupplierjson",{ajax:true},function(data){
  $.each(data,function(index,item){
    $('#supplierid').append($('<option>').text(item[2]+","+item[1]).val(item[0]))
    })
 })

 $('#btnsubmit').click(function () {
        $.getJSON("/displayallpurchasejson", { fromdate: $('#fromdate').val(),todate: $('#todate').val() }, function (data) {
            var htm = "<table class='table'><tr><th>Id</th><th>Category Name</th><th>Subcategory Name</th><th>Product Name</th><th>FinalProduct Name</th><th>Purchase Date</th><th>Supplier Name</th><th>Stock</th><th>Price</th></tr>"
            $.each(data, function (index, item) {
              htm += "<tr><th scope='row'>"+item.transactionid+"</th><td>"+item.categoryname+"</td><td>"+item.subcategoryname+"</td><td>"+item.productname+"</td><td>"+item.finalproductname+"</td><td>"+item.dateofpurchase+"</td><td>"+item.suppliername+"</td><td>"+item.stock+"</td><td>"+item.amount+"</td></tr>"
            })
            htm+= "</table>"
            $('#result').html(htm)
        })
    })

 })