var pemail;

$('.alter').click(function () {
    var pid=$(this).parent().prevAll('.pid').html();
    var pname=$(this).parent().prevAll('.pname').html();
    var pgender=$(this).parent().prevAll('.pgender').html();
    var pbirth=$(this).parent().prevAll('.pbirth').html();
    var ptel=$(this).parent().prevAll('.ptel').html();
    pemail=$(this).parent().prevAll('.pemail').html();
    var pgra=$(this).parent().prevAll('.pgraduate').html();
    $('#stdid').val(pid);
    $('#stdname').val(pname);
    $('#gender').val(pgender);
    $('#stdbirth').val(pbirth);
    $('#stdtel').val(ptel);
    $('#stdemail').val(pemail);
    $('#graduate').val(pgra);
    return pemail;
});
$('#altersubmit').click(function () {
    var id=$('#stdid').val();
    var nname=$('#stdname').val();
    var ngender=$('#gender').val();
    var nbirth=$('#stdbirth').val();
    var ntel=$('#stdtel').val();
    var nemail=$('#stdemail').val();
    var ngra=$('#graduate').val();
    $.ajax({
        url:'/admin/alterS',
        type:'post',
        datatype:'json',
        data:JSON.stringify(
            {
            id: id,
            nname: nname,
            ngender: ngender,
            nbirthday: nbirth,
            ntel: ntel,
            nemail: nemail,
            ngra: ngra,
            pemail: pemail
            }
        ),
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        contentType: "application/json; charset=utf-8",
        success:function (data) {
            alert("修改成功");
            console.log(data);
            window.location.reload();
        },
        error:function (err) {
            console.log(err);
            alert("修改失败，请稍候再试");
            window.location.reload();
        }
    })
});

$('.deleteStd').click(function () {
    var id=$(this).parent().prevAll('.pid').html();
    pemail=$(this).parent().prevAll('.pemail').html();
    $.ajax({
        url:'/admin/delS',
        type:'post',
        datatype:'json',
        data:JSON.stringify(
            {
            id: id,
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
