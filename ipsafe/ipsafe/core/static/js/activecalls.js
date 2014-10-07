/*

	Reload active calls

*/

function ReloadActiveCalls() { 
	$.get('/chamadasativas/?json', function(data) {
		tbody = $("#activecalls").find('tbody');
		tbody.html('');
		$.each(data, function(i, item) {
				tbody.append(
					'<tr><td>'+item.calldate+
					'</td><td>'+item.duration+
					'</td><td>'+item.origin+
					'</td><td>'+item.destination+
					'</td></tr>'
				);
				console.log('aiojaoi');
		});
	});
};


$(document).ready(function() {
	ReloadActiveCalls();
	setInterval("ReloadActiveCalls()", 5000); // 5 seconds
});



