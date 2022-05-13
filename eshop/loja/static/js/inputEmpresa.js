
$("#inputEmpresa").hide();
$(document).on('change', '#isVendedor', function() {   
    alert()
    if($('#isVendedor').is(":checked"))   
            $("#inputEmpresa").show();
        else
            $("#inputEmpresa").hide();
    });

$('#inputEmpresa').validate({ // initialize the plugin
    rules: {
        empresa: {
          lettersonly: true,
          required:true,
          minlength:5
      },
   
    },
    submitHandler: function (form) { 
        alert('Parabéns! Tornaste-te vendedor'); 
        return true; 
    }
});

jQuery.validator.addMethod("lettersonly", function(value, element) {
  return this.optional(element) || /^[a-z ]+$/i.test(value);
}, "Letters only please"); 
