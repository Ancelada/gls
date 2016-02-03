socket_connect();

function socket_connect(){
	socket = new SockJS('http://192.168.1.78:8989/orders');

	socket.onmessage = function(msg){
		$('.order_added').addClass('order_locked');
		/*window['ws_order_' + msg.data.type][msg.data.data];*/
	}

	socket.onclose = function(e){
		setTimeout(socket_connect, 5000);
	}
}

function ws_order_lock(msg){
	if(msg.action == 'highlight'){
		$('.order_added').addClass('order_locked');
	} else {
		$('.order_else').addClass('order_hidden');
	}
}