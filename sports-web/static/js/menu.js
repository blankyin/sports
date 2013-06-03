$(document).ready(function () { 
	$("#flyoutmenu").wijmenu({
      	showDelay: 100,
      	// select : function(e, data){
      	// 	// alert(1)
      	// }
    }); 

    $("#flyoutmenu").removeClass("ui-helper-hidden-accessible"); 

    // 选中当前菜单
    url = window.location.href;
	var menuList = $(".wijmo-wijmenu-link")
	for ( var i = 0; i < menuList.length; i++){
		var menu = menuList[i]
		if (url == menu.href){
			menu.classList.add("ui-state-focus");
		}
	}
}); 

