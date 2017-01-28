var options = {
	type: "basic", 
	title: "MailAsssit", 
	message: "Click here to check your tasks for today",
	icon: "../img/mailassist-logo.png"
}

chrome.notifications.create(options, callback);

function callback(){

};