var gai=$('.changeable');

$('#updateinfo').click(function () {
    gai.removeAttr('readonly');
    gai.attr('class','form-control is-valid');
    $('#up').css('display','block');
});

$('#up').click(function () {
    $.ajax({
        url:'/update',
        type:'post',
        datatype:'json',
        data:JSON.stringify(
            {
            id:$('#inputStdid').val(),
            birthday:$('#inputBirth').val(),
            tel:$('#inputTel').val()
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
            gai.setAttribute('readonly');
            $('#up').hide();
        },
        error:function (err) {
            console.log(err);
            alert("修改失败，请稍候再试");
            window.location.reload();
        }
    })
});