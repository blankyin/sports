
$(document).ready(function () {
    var username = getCookie('username');
    var password = getCookie('password');

	// 登录
    // $("#btn-login").click(function(e){
    // 	var username = $("#username");
    // 	var password = $("#password");

    // 	if(username.val().length == 0){
    //         return username.attr("placeholder", "用户名不能为空").focus();
    //     }

    // 	if(password.val().length == 0){
    //         return password.attr("placeholder", "密码不能为空").focus();
    //     }

    // 	$("#login-form").submit();
    // });
});

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) { 
                c_end = document.cookie.length;
            }
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}