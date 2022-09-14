$(document).ready(function(){

 $.getJSON("/getsubcategoriesjson",{ajax:true, categoryid:$('#categoryid').val()},function(data){
  $('#subcategoryname').empty()
  $('#subcategoryname').append($('<option>').text('-Sub-Category-'))
  $.each(data,function(index,item){
    $('#subcategoryname').append($('<option>').text(item[2]).val(item[1]))
  })
 })
})