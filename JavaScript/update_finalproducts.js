$(document).ready(function(){
 $.getJSON("/getfinalproductsjson",{ajax:true, productid:$('#productid').val()},function(data){
  $('#finalproductid').empty()
  $('#finalproductid').append($('<option>').text('-Final Product-'))
  $.each(data,function(index,item){
    $('#finalproductid').append($('<option>').text(item[4]).val(item[3]))
  })
 })
})