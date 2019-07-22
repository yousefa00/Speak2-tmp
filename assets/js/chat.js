var api = new Mesibo();
let accessToken = "1hr8j5udwb4oye1gsbm3s7g41oalvnuudj984z4m50txiasu9b06g3ed1ikgnspe"
api.setAppName("console");
api.setListener(new MesiboListener());
api.setCredentials(accessToken);
api.start();

function MesiboListener() {
}

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
