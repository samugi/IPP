$(function(){
	var socket = io.connect('http://localhost:3000')
	
	var red_event_list = $("#r-event-list")
	var blue_event_list = $("#b-event-list")
	var yellow_event_list = $("#y-event-list")
	
	
	socket.on("new_command_red", (data) => {
		console.log(data)
		red_event_list.prepend("<li class='event-element'>"+"<span class='from'>"+data.username+"</span><span class='tag'>"+data.command+"</span>"+"</li>");
		if($("#r-event-list .event-element").length > 5)
			$("#r-event-list .event-element")[5].remove();
	})
	
	socket.on("new_command_blue", (data) => {
		console.log(data)
		blue_event_list.prepend("<li class='event-element'>"+"<span class='from'>"+data.username+"</span><span class='tag'>"+data.command+"</span>"+"</li>");
		if($("#b-event-list .event-element").length > 5)
			$("#b-event-list .event-element")[5].remove();
	})
	
	socket.on("new_command_yellow", (data) => {
		console.log(data)
		yellow_event_list.prepend("<li class='event-element'>"+"<span class='from'>"+data.username+"</span><span class='tag'>"+data.command+"</span>"+"</li>");
		if($("#y-event-list .event-element").length > 5)
			$("#y-event-list .event-element")[5].remove();
	})
});