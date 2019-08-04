$(document).ready(function() {
    
    $('form').on('submit', function(event) {
      $.ajax({
         data : {
            matricule : $('#matricule').val(),
            nom: $('#nom').val(),
            prenom: $('#prenom').val(),
            naissance: $('#naissance').val(),
                },
            type : 'POST',
            url : '/process'
           })
       .done(function(data) {
         $('#output').text(data.output).show();
         
     });
     event.preventDefault();
     });
     
});
