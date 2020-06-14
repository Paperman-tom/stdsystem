$('#showadm').click(function () {
    $('#showadm').parent().addClass("active");
    $('#showstd').parent().removeClass("active");
    $('#useradm').show();
    $('#userstd').hide();
});
$('#showstd').click(function () {
    $('#showstd').parent().addClass("active");
    $('#showadm').parent().removeClass("active");
    $('#useradm').hide();
    $('#userstd').show();
});

$('#againpw').blur(function () {
    $('#againpw').removeClass("is-valid");
    $('#againpw').removeClass("is-invalid");
    $('#addsubmit').attr('disabled',false);
    if ($('#againpw').val()==$('#npassword').val()){
        $('#againpw').addClass("is-valid");
    }
    else {
        $('#againpw').addClass("is-invalid");
        $('#addsubmit').attr('disabled',true);
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

$('#useremail').blur(function () {
    $('#useremail').removeClass("is-valid");
    $('#useremail').removeClass("is-invalid");
    $('#addsubmit').attr('disabled', false);
    if (isEmail($('#email').val())) {
        $('#useremail').addClass("is-valid");
    } else {
        $('#useremail').addClass("is-invalid");
        $('#addsubmit').attr('disabled', true);
    }
});

$('#addsubmit').click(function () {
    $.ajax({
        url:'/admin/addADM',
        type:'post',
        datatype:'json',
        data:JSON.stringify(
            {
            username: $('#nusername').val(),
            password: $('#npassword').val(),
            email: $('#useremail').val(),
            }
        ),
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        contentType: "application/json; charset=utf-8",
        success:function (data) {
            alert("新增成功");
            console.log(data);
            window.location.reload();
        },
        error:function (err) {
            console.log(err);
            alert("新增失败，请稍候再试");
            window.location.reload();
        }
    })
});

$('.deleteUser').click(function () {
    var pemail=$(this).parent().prevAll('.uemail').html();
    $.ajax({
        url:'/admin/delU',
        type:'post',
        datatype:'json',
        data:JSON.stringify(
            {
            pemail: pemail
            }
        ),
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        contentType: "application/json; charset=utf-8",
        success:function (data) {
            alert("删除成功");
            console.log(data);
            window.location.reload();
        },
        error:function (err) {
            console.log(err);
            alert("删除失败，请稍候再试");
            window.location.reload();
        }
    })
});