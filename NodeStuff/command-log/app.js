const express = require('express')
const app = express()

app.set('view engine', 'ejs')
app.use(express.static('public'))
app.get('/', (req, res) => {
	res.render('index')
})

server = app.listen(3000)

const io = require("socket.io")(server)

io.on('connection', (socket) => {
		console.log('New user connected')
		socket.on('new_command_red', (data) => {
			console.log("new message from:" + data.username);
			io.sockets.emit('new_command_red', {command: data.command, username: data.username});
		})
		socket.on('new_command_blue', (data) => {
			console.log("new message from:" + data.username);
			io.sockets.emit('new_command_blue', {command: data.command, username: data.username});
		})
		socket.on('new_command_yellow', (data) => {
			console.log("new message from:" + data.username);
			io.sockets.emit('new_command_yellow', {command: data.command, username: data.username});
		})
})
