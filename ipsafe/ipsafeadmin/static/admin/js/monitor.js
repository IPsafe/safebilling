 $(document).ready(function(){
 
   	var socket = io.connect('http://' + document.domain + ':3000');
     
	socket.on("connect", function(){
		//$("body").append("connected</br>");
		console.log('conected');
		//socket.emit('add', 'Mensagemmmm');
	})
	socket.on("disconnect", function(){
		console.log('disconected');
	})

	socket.on("add", function(data){
	//	AddActiveCall(data);
		msg = JSON.parse(data);
		tbody = $("#activecalls").find('tbody');
		tbody.append(
				'<tr id='+msg.Unique_Id+'><td>'+msg.Event_Date_Local+
				'</td><td id="duration">'+'-'+
				'</td><td>'+msg.Caller_Caller_Id_Number+
				'</td><td>'+msg.Caller_Destination_Number+
				'</td><td id="status">'+msg.Channel_Call_State+
				'</td></tr>'
			);
		console.log(msg);

	})	

	socket.on("del", function(data){
		msg = JSON.parse(data);
		var element = document.getElementById(msg.Unique_Id);
		element.parentNode.removeChild(element);
		console.log(msg);

	})	

	socket.on("mod", function(data){
		msg = JSON.parse(data);
		var element = document.getElementById(msg.Unique_Id);
		element.cells[4].innerHTML = msg.Channel_Call_State;
                element.cells[1].innerHTML = '00:00:00';
		console.log(msg);

	})	

	//timer for duration
	

});





function AddActiveCall(data) { 
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
	});
};



$(document).ready(function(){

    var duration_calc = setInterval(function () {

        $('[id="duration"]').each(function() {
            content = $(this).html()
            if (content == '-') return;

            if (content == 0 || content == '0') {
                var time = new Date();
                time.setHours(0,0,0,0);
                $(this).html(time.getHours() + ':' + time.getMinutes() + ':' + time.getSeconds());       

            }
            else {
                var time = new Date();
                console.log(content);

                content_splitted = content.split(":");
                time.setHours(content_splitted[0], content_splitted[1], parseInt(content_splitted[2])+1, 0);
                console.log(time);

        // Add leading zeros
        if (time.getHours() < 10) hours = '0' + time.getHours();
        else hours = time.getHours();

        if (time.getMinutes() < 10) min = '0' + time.getMinutes();
        else min = time.getMinutes();

        if (time.getSeconds() < 10) sec = '0' + time.getSeconds();
        else sec = time.getSeconds();

        $(this).html(hours + ':' + min + ':' + sec);

    }

    $(this).html();
});

}, 1000);


});
