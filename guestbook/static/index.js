$(document).ready(function(){
    $('#loginBtn').on('click', function(){
        usermailval = $('#usermailVal').val()
        passwordval = $('#passwordVal').val()
        $.post('login', {
            usermail: usermailval,
            password: passwordval
        }).done(function(data){
            alert(data)
        })
    })

    $('#registBtn').on('click', function(){
        usermailval = $('#registUsermailVal').val()
        passwordval1 = $('#passwordVal1').val()
        passwordval2 = $('#passwordVal2').val()
        $.post('register', {
            usermail: usermailval,
            password1: passwordval1,
            password2: passwordval2
        }).done(function(data){
            alert(data)
        })
    })
})