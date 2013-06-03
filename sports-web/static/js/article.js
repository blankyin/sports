
$(document).ready(function () {

	if($('#article_form').length > 0){
		// 文章表单验证
		$('#article_form').validate({
		    rules: {
		    	article_title: {
		        	required: true,
		        	minlength: 2
		      	}
		    },
		    messages: {
		    	article_title: {
		        	required: ' 请输入文章标题 ',  // if this field was left blank this message will appear
	         		minlength: ' 请至少输入2个字符 ! '
		      	}
		    },
			highlight: function(element) {
				$(element).closest('.control-group').removeClass('success').addClass('error');
			},
			success: function(element) {
				element.text('OK!').addClass('valid').closest('.control-group').removeClass('error').addClass('success');
			}
		});

		// 文章内容验证（jquery.validate.js无法处理textarea）
		$('#add_article_button').click(function() {
			if ( $('#article_content').val() == '' ) {
				$('#article_content').closest('.control-group').removeClass('success').addClass('error');
				$('#article_content_error').show()
				return false;
			} else {
				$('#article_form').submit()
			}
	 
		});
	}


	// 类别表单验证
	if($('#category_form').length > 0){
		$('#category_form').validate({
		    rules: {
		    	category_name: {
		        	required: true
		      	}
		    },
		    messages: {
		    	category_name: {
		        	required: ' 请输入类别名称 '
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


// 删除文章
function delArticle(article_id){
	var ajax = $.ajax( {    
        url:'/article/del_article',// 跳转到 action    
        data:{
            article_id : article_id
        },    
        type:'post',    
        dataType:'json',    
        success:function(data) {    
            if(data.msg =="true" ){      
                alert("删除成功！");    
                window.location.reload();
            }else{    
                alert("删除失败！");    
            }    
         },    
         error : function() {     
              alert("删除失败！");    
         }    
    });  
}


// 删除文章分类
function delCategory(category_id){
	var ajax = $.ajax( {    
        url:'/article/del_category',// 跳转到 action    
        data:{
            category_id : category_id
        },    
        type:'post',    
        dataType:'json',    
        success:function(data) {    
            if(data.msg =="true" ){      
                alert("删除成功！");    
                window.location.reload();
            }else{    
                alert("删除失败！");    
            }    
         },    
         error : function() {     
              alert("删除失败！");    
         }    
    });  
}