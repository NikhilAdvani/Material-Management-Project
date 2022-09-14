$(document).ready(function(){
 var d = new Date()
 var cd = (d.getFullYear())+"-"+(d.getMonth()+1)+"-"+(d.getDate())
 $('#dateofissue').val(cd)


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

 $('#finalproductid').change(function(){
 $.getJSON("/displayfinalproductbyidjson",{ajax:true, finalproductid:$('#finalproductid').val()},function(data){
    $('#currentstock').html(data.stock)
 })
 })

 $.getJSON("/getemployeejson",{ajax:true},function(data){
  $.each(data,function(index,item){
    $('#demandemployeeid').append($('<option>').text(item[0]+", "+item[1]+" "+item[2]).val(item[0]))
    })
 })

 $('#qtyissue').keyup(function(){
   if(parseInt($('#currentstock').html())>=parseInt($('#qtyissue').val()))
   {
     $('#btnsubmit').attr('disabled', false)
   }
   else
   { $('#btnsubmit').attr('disabled', true) }
 })

$('#btnsubmit').click(function () {
        $.getJSON("/displayallissuejson", { fromdate: $('#fromdate').val(),todate: $('#todate').val() }, function (data) {
            var htm = "<table class='table'><tr><th>Id</th><th>Category Name</th><th>Subcategory Name</th><th>Product Name</th><th>FinalProduct Name</th><th>Demand <br> Employee Name</th><th>Issue Date</th><th>Quantity Issued</th><th>Remark</th></tr>"
            $.each(data, function (index, item) {
              htm += "<tr><th scope='row'>"+item.issueid+"</th><td>"+item.categoryname+"</td><td>"+item.subcategoryname+"</td><td>"+item.productname+"</td><td>"+item.finalproductname+"</td><td>"+item.dfname+" "+item.dlname+"</td><td>"+item.dateissue+"</td><td>"+item.qtyissue+"</td><td>"+item.remark+"</td></tr>"
            })
            htm+= "</table>"
            $('#result').html(htm)
        })
    })

 })