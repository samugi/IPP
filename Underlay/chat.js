var progressValue = 0;
var raidFreeze = false;
var malus = new Array();
malus["ic"] = "Inverted commands";


function progressBarTick(){
	
	if(!raidFreeze){
	
		progressValue += 100/TARGET_COMMAND_RECEIVED;
		
		$("#myBar").width(progressValue + '%');
		
		if(progressValue == 100){
			progressValue = 0;
			raidFreeze = true;
			$.get( "http://localhost:8080/setraid", function( data ) {
				console.log(data);
				$("#progress-raid-text").html("Raid telegram in progress!");
			});
			waitRaid();
		}
	}
}

function waitRaid(){
	setTimeout(function(){ 
		raidFreeze = false; 
		$("#myBar").width(progressValue + '%');
		$("#progress-raid-text").html("Raid bar loading...");
	}, 5*ONE_MINUTE);
}

function setBonusMalus(data){
	
	if(data.raidWinner == 'youtube'){
		$('#b-malus .malus').html("Current malus: "+malus[data.bm]);
		$('#y-malus .malus').html("Current malus: "+malus[data.bm]);
	}else if(data.raidWinner == 'mixer'){
		$('#r-malus .malus').html("Current malus: "+malus[data.bm]);
		$('#y-malus .malus').html("Current malus: "+malus[data.bm]);
	}else if(data.raidWinner == 'twitch'){
		$('#r-malus .malus').html("Current malus: "+malus[data.bm]);
		$('#b-malus .malus').html("Current malus: "+malus[data.bm]);
	}
	
	setTimeout(function(){
		$('#b-malus .malus').html(" ");
		$('#r-malus .malus').html(" ");
		$('#y-malus .malus').html(" ");
	}, data.duration);
	
}

$(function(){
	var socket = io.connect('http://localhost:3000')
	
	var red_event_list = $("#r-event-list")
	var blue_event_list = $("#b-event-list")
	var yellow_event_list = $("#y-event-list")
	
	
	socket.on("new_command_red", (data) => {
		progressBarTick();
		console.log(data)
		red_event_list.prepend("<li class='event-element'>"+"<span class='from'>"+data.username+"</span><span class='tag'>"+data.command+"</span>"+"</li>");
		if($("#r-event-list .event-element").length > 5)
			$("#r-event-list .event-element")[5].remove();
	})
	
	socket.on("new_command_blue", (data) => {
		progressBarTick();
		console.log(data)
		blue_event_list.prepend("<li class='event-element'>"+"<span class='from'>"+data.username+"</span><span class='tag'>"+data.command+"</span>"+"</li>");
		if($("#b-event-list .event-element").length > 5)
			$("#b-event-list .event-element")[5].remove();
	})
	
	socket.on("new_command_yellow", (data) => {
		progressBarTick();
		console.log(data)
		yellow_event_list.prepend("<li class='event-element'>"+"<span class='from'>"+data.username+"</span><span class='tag'>"+data.command+"</span>"+"</li>");
		if($("#y-event-list .event-element").length > 5)
			$("#y-event-list .event-element")[5].remove();
	})
	
	socket.on("send_bm", (data) => {
		setBonusMalus(data);
		console.log(data);
	})
	
});