/*
* 切换学生和管理员用户的表格显示
*/

$('#showadm').click(function () {
    $('#showadm').parent().addClass("active");
    $('#showstd').parent().removeClass("active");
    $('#useradm').show();
    $('#userstd').hide();
    $('#searchResult').hide();
});

$('#showstd').click(function () {
    $('#showstd').parent().addClass("active");
    $('#showadm').parent().removeClass("active");
    $('#useradm').hide();
    $('#userstd').show();
    $('#searchResult').hide();
});


/*
* 前端验证确认密码和邮箱格式有效性
* */

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
    if (isEmail($('#useremail').val())) {
        $('#useremail').addClass("is-valid");
    } else {
        $('#useremail').addClass("is-invalid");
        $('#addsubmit').attr('disabled', true);
    }
});

//模态框提交
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

//单行删除
var delclick= function () {
        var pemail=$(event.target).parent().prevAll('.uemail').html();
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
};

//搜索框
$('#searchU').click(function () {
    $.ajax({
        url:'/admin/searchU',
        type:'post',
        datatype:'json',
        data:JSON.stringify(
            {
            username: $('#searchText').val()
            }
        ),
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        contentType: "application/json; charset=utf-8",
        success:function (data) {
            $('#searchRows').html('');
            $('#useradm').hide();
            $('#userstd').hide();
            $('#searchResult').show();
            console.log(data);
            if (data==''){
                alert("对不起，没有该用户");
                window.location.reload();
            }
            for (var i = 0; i < data.length; i++) {
                data1 = JSON.stringify(data[i]);
                data2 = JSON.parse(data1);
                $.get('/static/js/searchResult.html',function (data3) {
                    render = template.compile(data3);
                    newRow = render(data2);
                    console.log(newRow);
                    $('#searchRows').append(newRow);
                    console.log('yes');
                });
            }

        },
        error:function (err) {
            console.log(err);
            alert("对不起，查找失败，请稍后再试");
            window.location.reload();
        }
    })
});