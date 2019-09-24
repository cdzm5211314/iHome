function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 页面加载完成后执行
$(document).ready(function () {
    $("#form-avatar").submit(function (e) {
        // 阻止页面表单的默认行为
        e.preventDefault();
        // 引用插件jquery.form.min.js对表单进行异步提交
        $(this).ajaxSubmit({
            url: "/api/v1.0/users/avatar",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "0"){
                    //上传成功
                    var avatarUrl= resp.data.avatar_url;
                    $("#user-avatar").attr("src",avatarUrl);
                }else{
                    alert(resp.errmsg)
                }
            }
        })

    })

});