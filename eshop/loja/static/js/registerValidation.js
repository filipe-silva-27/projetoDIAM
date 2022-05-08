$('#registerForm').validate({ // initialize the plugin
    rules: {
      username: {
          required:true,
          minlength:6
      },
      email: {
            required: true,
            email: true
        },
        psw: {
            required: true,
            minlength: 8
        },
        pswrepeat: {
          equalTo: '#psw'
        },
    },
    submitHandler: function (form) { // for demo
        alert('valid form submitted'); // for demo
        return true; // for demo
    }
});