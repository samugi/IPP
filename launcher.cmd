REM start the backend application that receives the commands from the server and emits the key presses to the emulators
ECHO starting app.js
start cmd.exe /c node Backend\command-log\app.js
REM start the Server that is going to listen for the incoming commands from the platforms
ECHO starting server
start cmd.exe /c node Backend\node-service\server.js
