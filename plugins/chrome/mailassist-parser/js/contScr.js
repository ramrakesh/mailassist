function strip(html){
   var tmp = document.createElement("DIV");
   tmp.innerHTML = html;
   return tmp.textContent || tmp.innerText || "";
}

chrome.runtime.onMessage.addListener(
  	function(request, sender, sendResponse) {
    	console.log(sender.tab ? "from a content script:" + sender.tab.url : "from the extension");
    	if (request.type == "get-message"){    		
			var inbox = document.querySelectorAll("div[class='a3s aXjCH m"+request.id+"']");
    		var sndMsg = inbox[0].innerHTML;
    		console.log(inbox[0].innerHTML);
    		console.log(strip(sndMsg));
      		sendResponse({message: strip(sndMsg)});
    	}
});

// var replyDiv = null;
// var loadReplyDiv = true;
// var reply = null;
// var frwd = null;
// var textField = null;
// var sendBut = null;
// var locationParam = '';

// function getReplyDiv() {
// 	replyDiv = document.querySelectorAll("div[class='nr tMHS5d']");
//     if(replyDiv.length != 0){
//     	loadReplyDiv = false;
//     	replyDiv = replyDiv[0];
//     }
// }

// var sendMessageSendBut = function(){
// 	alert(textField);
// }

// var replyEnabled = function(){
// 	console.log('Clicked Reply or Forward');
// 	sendBut = replyDiv.querySelectorAll("div[role=textbox]");
// 	textField = replyDiv.querySelectorAll("input");
// 	console.log(sendBut);
// 	console.log(textField);
// 	// sendBut.click(sendMessageSendBut);
// }

// function searchRepFrw(){
// 	var reply = replyDiv.querySelectorAll("span[class=ams]")[0];
// 	var frwd = replyDiv.querySelectorAll("span[class=ams]")[1];
// 	console.log(reply);
// 	console.log(frwd);
// 	console.log('Got it');
// 	reply.onclick = replyEnabled;
// 	reply.onclick = replyEnabled;
// }

// function searchRepFrwStart(){
// 	if(location.href != locationParam){
// 		setTimeout(function(){
// 			locationParam = location.href;
// 			getReplyDiv()
// 			searchRepFrw();
// 		}, 5000);
// 	}
// }

// function startSearch(){
// 	// var startSearchReplyDiv = setInterval(getReplyDiv, 1000);
// 	setTimeout(function(){
// 		// clearInterval(startSearchReplyDiv);
// 		var startSearchReplyDivNew = setInterval(searchRepFrwStart, 1000);
// 	}, 5000);	
// }

// $(document).ready(function(){
// 	startSearch();
// });