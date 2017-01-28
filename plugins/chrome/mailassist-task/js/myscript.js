var host = 'https://mailassist.herokuapp.com/'
var hostUser = host + 'user/'

var setNot = function(){
	var url = hostUser + 'api/user/profile-info';   		
	$.ajax({
		url: url,
		type: 'GET',
		dataType: 'json',
		success: function(data){
			email = data['email'];
			notifTime = data['timeNot'];
			notif = data['deskNot'];
			data = {
				notif: notif,
				notifTime: notifTime,
				email: email
			}
			chrome.runtime.sendMessage({type: "set-notification", data: data});
		},
		error: function(error){
			
		}
	});
};

document.addEventListener("set-notification", function(data) {
    setNot();
})

document.addEventListener("del-notification", function(data) {
    chrome.runtime.sendMessage({type: "del-notification"});
})