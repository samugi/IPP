const express = require('express');
const app = express();
var request = require('request');

var adjectives = require('./adjectives');
var nouns = require('./nouns');

var platforms = ['twitch','youtube','mixer'];
var ONE_SECOND = 1000;
var ONE_MINUTE = ONE_SECOND*60;
var ONE_HOUR = ONE_MINUTE*60;
var minUsers = 6;
var maxUsers = 10;
var usersAlive = 0;
var minTimeCommands = 4000;

var numUsers = parseInt(Math.random() * (maxUsers - minUsers) + minUsers);
	
console.log("NUMUSERS" + numUsers);
console.log("USERSALIVE" + usersAlive);
if(usersAlive < numUsers){
	var usersAliveTemp = usersAlive;
	for(var i = 0; i < numUsers - usersAliveTemp; i++){
		userGenerator();
	}
}

setInterval(function(){
	
	numUsers = parseInt(Math.random() * (maxUsers - minUsers) + minUsers);

	if(usersAlive < numUsers){
		var usersAliveTemp = usersAlive;
		for(var i = 0; i < numUsers - usersAliveTemp; i++){
			userGenerator();
		}
	}
	
},ONE_MINUTE*5);


function userGenerator(){
	usersAlive++;
	var nickname = nicknameGenerator();
	var platform = platforms[parseInt(Math.random()*3)];
	var lifeTime = Math.random()*(ONE_HOUR/2) + ONE_SECOND*10;
	var pollingInterval = Math.random()*ONE_SECOND*10+ minTimeCommands;
	var personality = getPersonality();
	
	var idUser = setInterval(function(){
		
		if(parseInt(Math.random()*100) > 98){
			personality = getPersonality();
		}
		
		var command = personality();		
		var joyCommand = commandGenerator(platform,command);
		
		sendCommandByFakeUser(command, nickname, platform, joyCommand);
	},pollingInterval);
	
	setTimeout(function(){
		usersAlive--;
		clearInterval(idUser);
	}, lifeTime);
	
}


function nicknameGenerator(){
	
	var nickname = "";
	
	var decisator = parseInt(Math.random()*10);
	if(decisator == 0){
		nickname = capitalizeFirstLetter(adjectives.adjectives[parseInt(Math.random()*adjectives.adjectives.length)]) + capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]) + (parseInt(Math.random()*99));
	}else if(decisator == 1){
		nickname = "x" + capitalizeFirstLetter(adjectives.adjectives[parseInt(Math.random()*adjectives.adjectives.length)]) + capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]) + "x";
	}else if(decisator == 2){
		nickname = capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]) + (parseInt(Math.random()*99));
	}else if(decisator == 3){
		nickname = "The" + capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]) + "Of" + capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]);
	}else if(decisator == 4){
		var index = parseInt(Math.random()*adjectives.adjectives.length);
		nickname = capitalizeFirstLetter(adjectives.adjectives[index].substring(parseInt(Math.random()*adjectives.adjectives[index].length-1))) + capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]);
	}else if(decisator == 5){
		var index = parseInt(Math.random()*adjectives.adjectives.length);
		var index2 = parseInt(Math.random()*nouns.nouns.length);
		nickname = capitalizeFirstLetter(adjectives.adjectives[index].substring(parseInt(Math.random()*adjectives.adjectives[index].length-1))) + capitalizeFirstLetter(nouns.nouns[index2].substring(parseInt(Math.random()*nouns.nouns[index2].length-1))) + (parseInt(Math.random()*99));
	}else if(decisator == 6){
		nickname = "_" + adjectives.adjectives[parseInt(Math.random()*adjectives.adjectives.length)].toUpperCase() + capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]) + (parseInt(Math.random()*99));
	}else if(decisator == 7){
		nickname = "_" + adjectives.adjectives[parseInt(Math.random()*adjectives.adjectives.length)].toUpperCase() + "_" + adjectives.adjectives[parseInt(Math.random()*adjectives.adjectives.length)].toUpperCase() + capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]) + (parseInt(Math.random()*99));
	}else if(decisator == 8){
		var index = parseInt(Math.random()*adjectives.adjectives.length);
		var index2 = parseInt(Math.random()*nouns.nouns.length);
		nickname = capitalizeFirstLetter(adjectives.adjectives[index].substring(parseInt(Math.random()*adjectives.adjectives[index].length-1))) + capitalizeFirstLetter(nouns.nouns[index2].substring(parseInt(Math.random()*nouns.nouns[index2].length-1))) + (parseInt(Math.random()*9999));
	}else if(decisator == 9){
		nickname = adjectives.adjectives[parseInt(Math.random()*adjectives.adjectives.length)].toUpperCase() + capitalizeFirstLetter(nouns.nouns[parseInt(Math.random()*nouns.nouns.length)]) + (parseInt(Math.random()*99));
	}
	
	return nickname;
	
}

function commandGenerator(platform,command){
	
	if(platform == 'mixer'){
	
		if(command == "A") return '1'
		if(command == "B") return '2'
		if(command == "UP") return '3'
		if(command == "DOWN") return '4'
		if(command == "LEFT") return '5'
		if(command == "RIGHT") return '6'
		if(command == "START") return '7'
		if(command == "SELECT") return '8'
	
	}else if(platform == 'youtube'){

		if(command == "A") return 'a'
		if(command == "B") return 'z'
		if(command == "UP") return 'i'
		if(command == "DOWN") return 'k'
		if(command == "LEFT") return 'j'
		if(command == "RIGHT") return 'l'
		if(command == "START") return 'p'
		if(command == "SELECT") return '.'

	}else if(platform == 'twitch'){

		if(command == "A") return 's'
		if(command == "B") return 'x'
		if(command == "UP") return 'f'
		if(command == "DOWN") return 'v'
		if(command == "LEFT") return 'c'
		if(command == "RIGHT") return 'b'
		if(command == "START") return 'h'
		if(command == "SELECT") return 'n'
	
	}
	return "ghe sboro";
}

function getPersonality(){
	
	var personalityDecisator = parseInt(Math.random()*100);
	
	var normalPersonality = function(){
		var commandDecisator = parseInt(Math.random()*100);
		if(commandDecisator < 3){
			command = "SELECT";
		}else if(commandDecisator < 8){
			command = "START";
		}else if(commandDecisator < 40){
			command = "A";
		}else if(commandDecisator < 52){
			command = "B";
		}else if(commandDecisator < 64){
			command = "UP";
		}else if(commandDecisator < 76){
			command = "LEFT";
		}else if(commandDecisator < 88){
			command = "RIGHT";
		}else if(commandDecisator <= 100){
			command = "DOWN";
		}
		return command;
	}
	
	var fighter = function(){
		var commandDecisator = parseInt(Math.random()*100);
		if(commandDecisator < 50){
			command = "A";
		}else if(commandDecisator < 70){
			command = "UP";
		}else if(commandDecisator < 90){
			command = "DOWN";
		}else if(commandDecisator < 95){
			command = "RIGHT";
		}else if(commandDecisator <= 100){
			command = "LEFT";
		}
		return command;
	}
	
	var travelerA = function(){
		
		var commandDecisator = parseInt(Math.random()*100);
	
		if(commandDecisator < 60){
			command = "LEFT";
		}else if(commandDecisator < 80){
			command = "RIGHT";
		}else if(commandDecisator < 90){
			command = "DOWN";
		}else if(commandDecisator < 100){
			command = "UP";
		}	
		
		return command;
	}
	
	var travelerB = function(){
		
		var commandDecisator = parseInt(Math.random()*100);
	
		if(commandDecisator < 60){
			command = "RIGHT";
		}else if(commandDecisator < 80){
			command = "LEFT";
		}else if(commandDecisator < 90){
			command = "DOWN";
		}else if(commandDecisator < 100){
			command = "UP";
		}	
		
		return command;
	}
	
	var travelerC = function(){
		
		var commandDecisator = parseInt(Math.random()*100);
	
		if(commandDecisator < 60){
			command = "DOWN";
		}else if(commandDecisator < 80){
			command = "RIGHT";
		}else if(commandDecisator < 90){
			command = "LEFT";
		}else if(commandDecisator < 100){
			command = "UP";
		}	
		
		return command;
	}
	
	var travelerD = function(){
		
		var commandDecisator = parseInt(Math.random()*100);
	
		if(commandDecisator < 60){
			command = "UP";
		}else if(commandDecisator < 80){
			command = "RIGHT";
		}else if(commandDecisator < 90){
			command = "DOWN";
		}else if(commandDecisator < 100){
			command = "LEFT";
		}	
		
		return command;
	}
	
	var speaker = function(){
		var commandDecisator = parseInt(Math.random()*100);
		if(commandDecisator < 40){
			command = "A";
		}else if(commandDecisator < 80){
			command = "B";
		}else if(commandDecisator < 90){
			command = "UP";
		}else if(commandDecisator < 100){
			command = "DOWN";
		}
		return command;
	}
	
	if(personalityDecisator < 25){
		return normalPersonality;
	}else if(personalityDecisator < 50){
		return speaker;
	}else if(personalityDecisator < 75){
		return fighter;
	}else if(personalityDecisator < 100){
		var travelDecisator =  parseInt(Math.random()*10);
		if(travelDecisator < 25){
			return travelerA;
		}else if(travelDecisator < 50){
			return travelerB;
		}else if(travelDecisator < 75){
			return travelerC;
		}else if(travelDecisator < 100){
			return travelerD;
		}
	}
	
	return normalPersonality;
	
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function sendCommandByFakeUser(command, user, platform, joyCommand){
	console.log(command+'&user='+user+'&platform='+platform+'&joycommand='+joyCommand);
	request.get('http://localhost:8080/send-command?command='+command+'&user='+user+'&platform='+platform+'&joycommand='+joyCommand,
		function (error, response, body) {
			if (!error && response.statusCode == 200) {
				console.log(body);
			}
	});

}