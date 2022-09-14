$(document).ready(function () {

  $('#pattern').keyup(function() {
      $.getJSON("/displayallfinalproductsjson", {pattern: $('#pattern').val()}, function (data) {
         var htm="<table class='table'><thead><tr><th>Id</th><th>Product Name</th><th>Stock</th><th>Price</th></tr></thead><tbody>"

          $.each(data, function (index, item) {
              htm+="<tr><th scope='row'>"+item.finalproductid+"</th><td>"+item.finalproductname+"</td><td>"+item.stock+"</td><td>"+item.price+"</td></tr>"
          })
         htm+="</tbody></table>"
         $('#result').html(htm)
      })
  })

})