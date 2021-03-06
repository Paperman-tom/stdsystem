//显示全部学生名单
$('#showstds').click(function () {
    $('.stdtable').show();
    $('#searchResult').hide();
});


var pemail;

var alterclick=function () {
    var pid=$(event.target).parent().prevAll('.pid').html();
    var pname=$(event.target).parent().prevAll('.pname').html();
    var pgender=$(event.target).parent().prevAll('.pgender').html();
    var pbirth=$(event.target).parent().prevAll('.pbirth').html();
    var ptel=$(event.target).parent().prevAll('.ptel').html();
    pemail=$(event.target).parent().prevAll('.pemail').html();
    var pgra=$(event.target).parent().prevAll('.pgraduate').html();
    $('#stdid').val(pid);
    $('#stdname').val(pname);
    $('#gender').val(pgender);
    $('#stdbirth').val(pbirth);
    $('#stdtel').val(ptel);
    $('#stdemail').val(pemail);
    $('#graduate').val(pgra);
    return pemail;
};

//模态框提交 ajax
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

var delclick=function () {
    var id=$(event.target).parent().prevAll('.pid').html();
    pemail=$(event.target).parent().prevAll('.pemail').html();
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
};

//先编译一个渲染函数
var render;
$.get('/static/js/searchReS.html',function (data3) {
    render = template.compile(data3);
});
//搜索框
$('#searchS').click(function () {
    $.ajax({
        url:'/admin/searchS', //指定请求的url
        type:'post', //请求类型为POST
        datatype:'json', //数据格式为json
        data:JSON.stringify( //发送的数据
            {
            key: $('#searchKey').val(),
            kw: $('#searchText').val()
            }
        ),
        headers: { //请求头
            "Content-Type": "application/json;charset=utf-8"
        },
        contentType: "application/json; charset=utf-8", //需要的响应格式
        success:function (data) { //请求成功后的回调函数
            $('#searchRows').html('');
            $('.stdtable').hide();
            $('#searchResult').show();
            console.log(data);
            if (data=='None'||data==''){
                alert("对不起，没有该用户");
                window.location.reload();
            }
            //插入查询结果注意两层解析数据
            for (var i = 0; i < data.length; i++) {
                data1 = JSON.stringify(data[i]);
                data2 = JSON.parse(data1);
                data2['birthday']=(new Date(data2['birthday'])).toLocaleDateString().replace(/\//g,"-");
                newRow = render(data2); //使用art-template编译的渲染函数渲染数据
                console.log(newRow);
                $('#searchRows').append(newRow);
                console.log('yes');
            }
        },
        error:function (err) { //请求错误的回调函数
            console.log(err);
            alert("对不起，查找失败，请稍后再试");
            window.location.reload();
        }
    })
});