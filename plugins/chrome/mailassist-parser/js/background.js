// chrome.runtime.onMessage.addListener(function(response, sender, sendResponse){
// 	alert(response);
// });

// Handle requests for passwords
chrome.runtime.onMessage.addListener(function(request) {
    if (request.type === 'get-message') {
        
    }
});