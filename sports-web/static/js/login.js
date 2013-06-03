$(document).ready(function () {

	if($('#login_form').length > 0){
		// 表单验证
		$('#login_form').validate({
		    rules: {
		    	username: {
		        	required: true,
		        	minlength: 4
		      	},
		      	password: {
		        	required: true
		      	}
		    },
		    messages: {
		    	username: {
		        	required: ' 请输入账号 ',  // if this field was left blank this message will appear
	         		minlength: ' 请至少输入4个字符 ! '
		      	},
		      	password: {
		        	required: ' 请输入密码 '  // if this field was left blank this message will appear
		      	}
		    },
			highlight: function(element) {
				$(element).closest('.control-group').removeClass('success').addClass('error');
			},
			success: function(element) {
				element.text('OK!').addClass('valid').closest('.control-group').removeClass('error').addClass('success');
			}
		});
	}
});