let accessToken = "1hr8j5udwb4oye1gsbm3s7g41oalvnuudj984z4m50txiasu9b06g3ed1ikgnspe"
var api = new Mesibo();
api.setAppName("console");
api.setListener(new MesiboListener());
api.setCredentials(accessToken);
api.start();

let button = document.querySelector('#button');
var userMessage = document.querySelector('#chatText').value;
var adminUser = "13129612665";

function printText() {
	console.log(userMessage);
}

button.addEventListener('click', ()=>{
	printText();
  sendTextMessage(adminUser, userMessage);
})

function MesiboListener() {
  MesiboListener.prototype.Mesibo_OnConnectionStatus = function(status, value) {
  	console.log("TestNotify.prototype.Mesibo_OnConnectionStatus: "  + status);
  }

  MesiboListener.prototype.Mesibo_OnMessageStatus = function(m) {
  	console.log("TestNotify.prototype.Mesibo_OnMessageStatus: from "
  			+ m.peer + " status: " + m.status);
  }

  MesiboListener.prototype.Mesibo_OnMessage = function(m, data) {
  	console.log("TestNotify.prototype.Mesibo_OnMessage: from "  + m.peer);
  }
}

function sendTextMessage(to, message) {
	var p = {};
       	p.peer = to;
	// var id = parseInt(Math.random()*10000);
  var id = 76903;
	api.sendMessage(p, id, message);
}
