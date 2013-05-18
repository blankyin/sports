var datasource;

$(document).ready(function () { 
	var proxy = new wijhttpproxy({
   		url: "http://127.0.0.1:1234/video/xijia",
   		dataType: "json",
   		data: {
      		featureClass: "P",
      		style: "full",
      		// maxRows: 20,
      		name_startsWith: '',
      		page: 1
   		},
   		key: 'videos'
	});

	var myReader = new wijarrayreader([{
        name: 'round',
        mapping: function (item) {
            return '第' + item.round + '轮';
        }
    },{
        name: 'title',
        mapping: function (item) {
        	var content;
        	content = '<a target="_blank" href=' + item.url + '>' 
        			// + '<img width="100" height="60" src=' + item.image + '></img> ' 
        			+ item.title + '</a>';
            return content;
        }
    }, {
        name: 'time',
        mapping: function (item) {
            return item.time;
        }
    }, {
        name: 'gmt_create',
        mapping: function (item) {
            return item.gmt_create;
        }
    }]);       

	datasource = new wijdatasource({
   		reader: myReader,
   		proxy: proxy,
   		loaded: function (data){
	        // read items.
	        var items = data.items;
	    }
	});

	$("#video").wijgrid({ 
		allowColMoving: true,
		allowColSizing: true,
		// allowVirtualScrolling: true,
        allowSorting: true, 
        allowPaging: true, 
        pageSize: 20, 
        // showRowHeader: true,
        // pagerSettings:{mode: "nextPrevious", position: "topAndBottom"},
        data: datasource,
		ensureControl: true,
		columns: [
			{ headerText: "场次" },
			{ headerText: "标题" },
			{ headerText: "视频时长" },
			{ headerText: "创建时间" },
		]
    }); 

    datasource.load();
}); 

function loadFilteredData() {
    // datasource.proxy.options.data.name_startsWith = $('#filterInput').val();
    // datasource.load();
}