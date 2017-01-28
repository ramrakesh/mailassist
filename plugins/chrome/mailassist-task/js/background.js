var host = 'https://mailassist.herokuapp.com/'
var hostUser = host + 'user/'
var notifTime = null;
var email = null;
var notif = false;
var flag = false;
var timeOutInterval = null;
var timeOutTimeLim = null;

var NotificationRun = function(){
	// console.log('In NotificationRun');
	// console.log(notif);
	if(notif){
		var options = {
			type: "basic", 
			title: "MailAsssit", 
			message: "Click here to check your tasks for today",
			iconUrl: "../img/mailassist-logo.png"
		};
		chrome.notifications.create(options, function(){
			console.log("Notification Done!");
		});
		chrome.notifications.onClicked.addListener(function(){
			window.open("https://mailassist.herokuapp.com/user","__blank");
		});
		// if (Notification.permission !== "granted")
	 //    	Notification.requestPermission();
	 //  	else {
	 //    	var notification = new Notification('MailAssist Tasks', {
	 //      		icon: 'http://localhost:8000/static/core/img/logo/mailassist-logo-dark.png',
	 //      		body: "Click here to check your tasks for today",
	 //    	});
	 //    	notification.onclick = function () {
	      		      
	 //    	};
	 //  	}
	}
};

var checkTimeOut = function(){
	console.log('In checkTimeOut');
	var date = new Date();
	var timeNotHr = notifTime.split(":")[0]
	var timeNotMm = notifTime.split(":")[1]
	var notTime = new Date(date.getFullYear(),(date.getMonth()),date.getDate(),timeNotHr,timeNotMm);
	var timeDiff = notTime.getTime() - (new Date()).getTime();
	if(timeDiff < 0) timeDiff = timeDiff + 24 * 60 * 60 * 1000;
	console.log(notTime);
	console.log(notTime.getTime());
	console.log((new Date()));
	console.log((new Date()).getTime());
	console.log(timeDiff);
	timeOutTimeLim = setTimeout(NotificationRun, timeDiff);
};

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if(request.type == "set-notification"){
		// console.log("set-notification");
		notif = true;
		email = request.data.email;
		notif = request.data.notif;
		notifTime = request.data.notifTime;		
		var oneDay = 1000*60*60*24;
		if (Notification.permission !== "granted")
    		Notification.requestPermission();
		checkTimeOut();
		timeOutInterval = setInterval(checkTimeOut, oneDay);
	}
	else if(request.type == "del-notification"){
		// console.log("del-notification");
		notif = false;
		clearTimeout(timeOutTimeLim);
		clearInterval(timeOutInterval);
	}  		
});