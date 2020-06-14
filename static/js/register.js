$('#pass2').blur(function () {
    $('#ok').hide();
    $('#fault').hide();
    $('#continue').attr('disabled',false);
    if ($('#pass2').val()==$('#pass').val()){
        $('#ok').show();
    }
    else {
        $('#fault').show();
        $('#continue').attr('disabled',true);
    }
});

var isEmail = function (val) {
    var pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    var domains= ["qq.com","163.com","vip.163.com","263.net","yeah.net","sohu.com","sina.cn","sina.com","eyou.com","gmail.com","hotmail.com","std.uestc.edu.cn","uestc.edu.cn"];
    if(pattern.test(val)) {
        var domain = val.substring(val.indexOf("@")+1);
        for(var i = 0; i< domains.length; i++) {
            if(domain == domains[i]) {
                return true;
            }
        }
    }
    return false;
};

$('#email').blur(function () {
    $('#ok2').hide();
    $('#fault2').hide();
    $('#continue').attr('disabled',false);
    if (isEmail($('#email').val())){
        $('#ok2').show();
    }
    else {
        $('#fault2').show();
        $('#continue').attr('disabled',true);
    }
});


$('#continue').click(function () {
    var Udata={
        data: JSON.stringify({
            "username":$('#username').val(),
            "password":$('#pass').val(),
            "email":$('#email').val()
        })
    };

    $.ajax({
        url:'/register',
        type:'post',
        datatype:'json',
        data:JSON.stringify(
            {
            username:$('#username').val(),
            password:$('#pass').val(),
            email:$('#email').val()
        }
        ),
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        contentType: "application/json; charset=utf-8",
        success:function (data) {
            $('#userform').hide();
            console.log(data);
            $.get('/static/js/info.html',function (data2) {
                var render = template.compile(data2);
                var newinfo = render(data);
                console.log(newinfo);
                $('#form').append(newinfo);
                console.log('yes');
            });
        },
        error:function (err) {
            console.log(err)
        }
    })

});