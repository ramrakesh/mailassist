app.controller('mailAssistController', ['$scope','$location','$mdSidenav','$mdDialog', function($scope,$location,$mdSidenav,$mdDialog){

	$scope.host = 'https://mailassist.herokuapp.com/'
	$scope.hostUser = $scope.host + 'user/'

	$scope.noSession = false;
	$scope.session = false;
	$scope.loading = true;
	$scope.loadingMsgs = false;
	$scope.msgsDone = false;
	$scope.threadID = '';
	$scope.name = 'User';
	$scope.email = 'someone@example.com';
	$scope.error = '';
	$scope.saveRemError = false;
	$scope.remSugNo = 0;
	$scope.loadingEditRem = false;
	$scope.loadingAddNew = false;
	$scope.loadingSaveRem = false;
	$scope.loadingEnNot = false;
	$scope.parseFail = false;
	$scope.enNotError = '';

	$scope.messages = [];
	$scope.msgsNo = 0;

	$scope.newRemForm = {
		mid: "",
		rem: "",
		date: ""
	};

	$scope.editRemForm = {
		mid: "",
		id: "",
		rem: "",
		date: ""
	};

	$scope.editRemView = {
		mid: "",
		rem: "",
		date: ""
	};

	$scope.enNot = {
		en: false,
		not: "Kindly acknowledge us the status of your query",
		email: "",
		date: ""
	};
	var currentDate = new Date();
	var dayFin=currentDate.setDate(currentDate.getDate() + 1);
	var monthFin = currentDate.getMonth() + 1
	var yearFin = currentDate.getFullYear()
	//document.write("<b>" + dayFin + "-" + monthFin + "-" + yearFin + "</b>")
	$scope.date_textFin = dayFin + "-" + monthFin + "-" + yearFin;

	var date = new Date();
	var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
	
	$scope.date_text = date.getDate() + "-" + months[date.getMonth()] + "-" + date.getFullYear();

	$scope.conDate = function(dateStr){
		return dateStr.split('-')[0] + ' ' + months[Number(dateStr.split('-')[1]) - 1] + ', ' + dateStr.split('-')[2]
	};

	Array.prototype.contains = function(v) {
    	for(var i = 0; i < this.length; i++) {
        	if(this[i] === v) return true;
    	}
    	return false;
	}

	var checkDate = function(date){
		var pattern =/^([0-9]{2})-([0-9]{2})-([0-9]{4})$/;
		if(!pattern.test(date)) return false;
		else{
			var oddMonths = [1,3,5,7,8,10,12];
			var evenMonths = [4,6,9,11];
			var feb = [28,29];
			if((Number(date.split('-')[2])%4 == 0) && Number(date.split('-')[1] == 2) && (Number(date.split('-')[0]) < 0 || Number(date.split('-')[0]) > 29)) return false;
			else if((Number(date.split('-')[2])%4 != 0) && Number(date.split('-')[1] == 2) && (Number(date.split('-')[0]) < 0 || Number(date.split('-')[0]) > 28)) return false;
			else if(evenMonths.contains(Number(date.split('-')[1])) && (Number(date.split('-')[0]) < 0 || Number(date.split('-')[0]) > 30)) return false;
			else if(oddMonths.contains(Number(date.split('-')[1])) && (Number(date.split('-')[0]) < 0 || Number(date.split('-')[0]) > 31)) return false;
			else if(Number(date.split('-')[1]) > 12) return false;
		}
		return true;
	};

	$scope.saveRems = function(){
		$scope.loadingSaveRem = true;
		$scope.saveRemError = 'Saving your reminders...';
		$('#modal3').openModal();
		var flag = false;
		var i = 0;
		var saveRemInp = [];
		var threadID = '';
		for(var i = 0; i<$scope.messages.length; i++){
			for(var j = 0; j<$scope.messages[i]['remSugNo']; j++){
				threadID = $scope.messages[i]['threadID'];
				saveRemInp.push({
					rem: $scope.messages[i]['remSugs'][j]['rem'],
					date: $scope.messages[i]['remSugs'][j]['date'],
					sender: $scope.messages[i]['sender'],
					subject: $scope.messages[i]['subject'],
					content: $scope.messages[i]['content'],
					threadID: $scope.messages[i]['threadID']
				});
			}
		}
		while(i<saveRemInp.length){
			if(saveRemInp[i].date == ''){
				flag = true;
				//saveRemInp[i].date=$scope.date_textFin;
			}else{
				saveRemInp[i].date = saveRemInp[i].date.split('-')[0] + '-' + saveRemInp[i].date.split('-')[1] + '-' + saveRemInp[i].date.split('-')[2];
			}
			i = i+1;
		}
		if(flag){
			$scope.loadingSaveRem = false;
			$scope.saveRemError = 'All Reminders must have a date.';
		}if(!checkNotValid()){
			$scope.loadingSaveRem = false;
			$scope.saveRemError = 'Please provide valid Notification Details.';
		}else{
			var url = $scope.hostUser + 'plugin/api/plugin/message/save-rems';
			var jObject={};
			jObject = JSON.stringify(saveRemInp);
			$.ajax({
				url: url,
				type: 'POST',
				dataType: 'json',
				data:{
					rems: jObject,
					notDetEn: $scope.enNot.en,
					notDetNot: $scope.enNot.not,
					notDetDate: $scope.enNot.date,
					notDetEmail: $scope.enNot.email,
					threadID: threadID
				},
				success: function(data){
					if(data['done']){
						$scope.$apply(function() {
							$scope.loadingSaveRem = false;
							$scope.saveRemError = 'All Reminders are saved.';
						});
					}else{
						$scope.$apply(function() {
							$scope.loadingSaveRem = false;
							$scope.saveRemError = data['error'];
						});
					}					
				},
				error: function(error){
					alert("Some Error Occurred. Please Refresh");
				}
			});
		}
	};

	var getProfile = function(){
  		var url = $scope.hostUser + 'api/user/profile-info';   		
	  	$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			success: function(data){
				$scope.$apply(function() {
					$scope.name = data['name'];
					$scope.email = data['email'];
				});
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
  	};

	$scope.toggleMail = function(message_id){
		for(var i = 0; i<$scope.msgsNo; i++){
			if($scope.messages[i]['message_id'] == message_id){
				$scope.messages[i]['small'] = !$scope.messages[i]['small'];		
			}				
		}
	};

	var updateRemSugNo = function(){
		var count = 0;
		for(var i = 0; i<$scope.msgsNo; i++){
			count = count + Number($scope.messages[i]['remSugNo']);			
		}
		$scope.remSugNo = count;
	};

	$scope.checkSysRemNo = function(message_id){
		var count = 0;
		for(var i = 0; i<$scope.msgsNo; i++){
			for(var j = 0; j<$scope.messages[i]['remSugNo']; j++){
				if($scope.messages[i]['remSugs'][j]['type'] == 'system'){
					count = count + 1;
				}
			}		
		}
		if(count == 0) return false;
		else return true;
	};

	$scope.checkUserRemNo = function(message_id){
		var count = 0;
		for(var i = 0; i<$scope.msgsNo; i++){
			for(var j = 0; j<$scope.messages[i]['remSugNo']; j++){
				if($scope.messages[i]['remSugs'][j]['type'] == 'user'){
					count = count + 1;
				}
			}			
		}
		if(count == 0) return false;
		else return true;
	};


	var getRemVals = function(message_id, rem_id){
		for(var i = 0; i<$scope.msgsNo; i++){
			if($scope.messages[i]['message_id'] == message_id){
				for(var j = 0; j<$scope.messages[i]['remSugs'].length; j++){
					if($scope.messages[i]['remSugs'][j]['id'] == rem_id){
						$scope.editRemView.rem = $scope.messages[i]['remSugs'][j]['rem'];
						$scope.editRemView.date = $scope.messages[i]['remSugs'][j]['date'];
						$scope.editRemForm.rem = $scope.messages[i]['remSugs'][j]['rem'];
						$scope.editRemForm.date = $scope.messages[i]['remSugs'][j]['date'];
					}
				}
			}
		}	
	};

	$scope.editRem = function(message_id, rem_id){
		$scope.editRemForm.id = rem_id;
		$scope.editRemForm.mid = message_id;
		getRemVals(message_id, rem_id);
		$scope.editRemError = '';
		$('#modal2').openModal();
	};

	$scope.editnewRem = function(){
		$scope.loadingEditRem = true;
		$scope.editRemError = '';
		if($scope.editRemForm.rem == '' || $scope.editRemForm.date == ''){
			$scope.loadingEditRem = false;
			$scope.editRemError = 'Please fill out both the fields';
		}else if(!checkDate($scope.editRemForm.date)){
			$scope.loadingEditRem = false;
			$scope.editRemError = 'Incorrect Date Format (Correct Format: DD-MM-YYYY)';
		}else{
			$scope.loadingEditRem = false;
			for(var i = 0; i<$scope.msgsNo; i++){
				if($scope.messages[i]['message_id'] == $scope.editRemForm.mid){
					for(var j = 0; j<$scope.messages[i]['remSugs'].length; j++){
						if($scope.messages[i]['remSugs'][j]['id'] == $scope.editRemForm.id){
							$scope.messages[i]['remSugs'][j]['rem'] = $scope.editRemForm.rem;
							$scope.messages[i]['remSugs'][j]['date'] = $scope.editRemForm.date;
						}
					}
				}
			}
			updateRemSugNo();
			$('#modal2').closeModal();
		}
	};

	$scope.addRem = function(message_id){
		$scope.newRemForm.mid = message_id;
		$scope.newRemForm.rem = "";
		$scope.newRemForm.date = "";
		$scope.newRemError = '';
		$('#modal1').openModal();
	};

	$scope.addnewRem = function(){
		$scope.loadingAddNew = true;
		$scope.newRemError = '';
		if($scope.newRemForm.rem == '' || $scope.newRemForm.date == ''){
			$scope.loadingAddNew = false;
			$scope.newRemError = 'Please fill out both the fields';
		}else if(!checkDate($scope.newRemForm.date)){
			$scope.loadingAddNew = false;
			$scope.newRemError = 'Incorrect Date Format (Correct Format: DD-MM-YYYY)';
		}else{
			$scope.loadingAddNew = false;
			for(var i = 0; i<$scope.msgsNo; i++){
				if($scope.messages[i]['message_id'] == $scope.newRemForm.mid){
					var newID = 0;
					if($scope.messages[i]['remSugNo'] == 0) 
						newID = 1;
					else
						newID = $scope.messages[i]['remSugs'][$scope.messages[i]['remSugs'].length - 1]['id'] + 1;
					$scope.messages[i]['remSugs'].push({id:newID,rem:$scope.newRemForm.rem,date:$scope.newRemForm.date,type:'user',notif:'Notification Message'});
					$scope.messages[i]['remSugNo'] = $scope.messages[i]['remSugs'].length;
				}
			}
			updateRemSugNo();
			$('#modal1').closeModal();
		}
	};

	var checkEmail = function(email){
		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    	return re.test(email);
	};

	var checkNotValid = function(){
		if($scope.enNot.en == true){
			if($scope.enNot.not == '' || $scope.enNot.email == '' || $scope.enNot.date == ''){
				return false;
			}else if(!checkDate($scope.enNot.date)){
				return false;
			}else if(!checkEmail($scope.enNot.email)){
				return false;
			}else{
				return true;
			}
		}else{
			return true;
		}
		
	};

	$scope.enNotSub = function(){
		$scope.loadingEnNot = true;
		$scope.enNotError = '';
		$scope.enNot.en = false;
		if($scope.enNot.not == '' || $scope.enNot.email == '' || $scope.enNot.date == ''){
			$scope.loadingEnNot = false;
			$scope.enNotError = 'Please fill out all the fields';
		}else if(!checkDate($scope.enNot.date)){
			$scope.loadingEnNot = false;
			$scope.enNotError = 'Incorrect Date Format (Correct Format: DD-MM-YYYY)';
		}else if(!checkEmail($scope.enNot.email)){
			$scope.loadingEnNot = false;
			$scope.enNotError = 'Incorrect Email Format';
		}else{
			$scope.loadingEnNot = false;
			$scope.enNotError = 'Notification Enabled';
			$scope.enNot.en = true;
		}
	};

	$scope.delMessage = function(message_id){
		for(var i = 0; i<$scope.messages.length; i++){
			if($scope.messages[i]['message_id'] == message_id){
				$scope.messages.splice(i,1);
			}
		}
		$scope.msgsNo = $scope.messages.length;
		updateRemSugNo();
	};

	$scope.delRem = function(message_id, rem_id){
		for(var i = 0; i<$scope.msgsNo; i++){
			if($scope.messages[i]['message_id'] == message_id){
				for(var j = 0; j<$scope.messages[i]['remSugs'].length; j++){
					if($scope.messages[i]['remSugs'][j]['id'] == rem_id)
						$scope.messages[i]['remSugs'].splice(j,1);
				}
				$scope.messages[i]['remSugNo'] = $scope.messages[i]['remSugs'].length;						
			}				
		}
		updateRemSugNo();
	};

	$scope.delAllRems = function(message_id){
		for(var i = 0; i<$scope.msgsNo; i++){
			if($scope.messages[i]['message_id'] == message_id){
				$scope.messages[i]['remSugs'] = [];
				$scope.messages[i]['remSugNo'] = 0;
				$scope.messages[i]['remSug'] = true;		
			}				
		}
		updateRemSugNo();
	};

	$scope.delUserRems = function(message_id){
		for(var i = 0; i<$scope.msgsNo; i++){
			if($scope.messages[i]['message_id'] == message_id){
				for(var j = 0; j<$scope.messages[i]['remSugs'].length; j++){
					if($scope.messages[i]['remSugs'][j]['type'] == 'user'){
						$scope.messages[i]['remSugs'].splice(j,1);
						j = j - 1;
					}
				}
				$scope.messages[i]['remSugNo'] = $scope.messages[i]['remSugs'].length;						
			}				
		}
		updateRemSugNo();
	};

	$scope.delSysRems = function(message_id){
		for(var i = 0; i<$scope.msgsNo; i++){
			if($scope.messages[i]['message_id'] == message_id){
				for(var j = 0; j<$scope.messages[i]['remSugs'].length; j++){
					if($scope.messages[i]['remSugs'][j]['type'] == 'system'){
						$scope.messages[i]['remSugs'].splice(j,1);
						j = j - 1;
					}
				}
				$scope.messages[i]['remSugNo'] = $scope.messages[i]['remSugs'].length;						
			}				
		}
		updateRemSugNo();
	};

	var updateRems = function(message_id, rems){
		$scope.$apply(function() {
			for(var i = 0; i<$scope.msgsNo; i++){
				if($scope.messages[i]['message_id'] == message_id){
					$scope.messages[i]['remSugs'] = rems;
					$scope.messages[i]['remSugNo'] = rems.length;
					$scope.messages[i]['remSug'] = true;
					$scope.messages[i]['showRemsLoading'] = false;		
					$scope.messages[i]['showRemsBut'] = true;		
				}				
			}
		});
		updateRemSugNo();
	};

	$scope.getRemsForMessage = function(message_id){
		for(var i = 0; i<$scope.msgsNo; i++){
			if($scope.messages[i]['message_id'] == message_id){
				$scope.messages[i]['showRemsLoading'] = true;	
				$scope.messages[i]['remSug'] = false;	
				$scope.messages[i]['showRemsBut'] = false;		
			}				
		}
		var subject = '';
		var content = '';
		var sender = '';
		var cleanContent = '';
 		for(var i = 0; i<$scope.msgsNo; i++){
 			if(message_id == $scope.messages[i]['message_id'])
			{
				subject = $scope.messages[i]['subject'];
				content = $scope.messages[i]['content'];
				sender = $scope.messages[i]['sender'];
				cleanContent = $scope.messages[i]['cleanContent'];
			}
		}
 		var url = $scope.hostUser + 'plugin/api/plugin/message/check-text';  		
	  	$.ajax({
			url: url,
			type: 'POST',
			dataType: 'json',
			data : {
				message : content,
				sender: sender,
				subject: subject,
				cleanContent: cleanContent
			},
			success: function(data){
				updateRems(message_id,data['rems']);
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
	};

	var getReminders = function(){
		for(var i = 0; i<$scope.msgsNo; i++){
			var message_id = $scope.messages[i]['message_id'];
			var subject = $scope.messages[i]['subject'];
			var content = $scope.messages[i]['content'];
			var sender = $scope.messages[i]['sender'];
			// getRemsForMessage(message_id,subject,content,sender);
		}

	};

  	var updateMessageList = function(data){  		
		$scope.$apply(function() {
			$scope.loadingMsgs = false;
			$scope.msgsDone = true;
			$scope.messages = data['messages'];
			$scope.msgsNo = $scope.messages.length;
		});
		// getReminders();
		for(var i = 0; i<$scope.msgsNo; i++){
			$scope.messages[i]['showRemsLoading'] = false;					
			$scope.messages[i]['showRemsBut'] = false;					
		}
  	};

  	var updateMessageListParseFail = function(){  		
		$scope.$apply(function() {
			$scope.loadingMsgs = false;
			$scope.parseFail= true;
		});
  	};

  	function strip(html){
	   var tmp = document.createElement("DIV");
	   tmp.innerHTML = html;
	   return tmp.textContent || tmp.innerText || "";
	}

	$scope.checkMsgLength = function(content){
		var resp = content;
  		if(resp.length > 150)
  			return true;
  		return false;
	};

  	$scope.showMsgContent = function(content){
  		var resp = content;
  		if(resp.length > 150)
  			resp = resp.substring(0,150) + '...';
  		return strip(resp);
  	};

  	$scope.readPage = function(){
		$scope.loadingMsgs = true;
  		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
			var threadVals = tabs[0]['url'].split('/');
			$scope.threadID = threadVals[threadVals.length-1];
			// console.log($scope.threadID);
			var url = $scope.hostUser + 'plugin/api/plugin/message/get-message-list';
			$.ajax({
				url: url,
				type: 'POST',
				dataType: 'json',
				data : {
					threadID : $scope.threadID
				},
				success: function(data){
					updateMessageList(data);
				},
				error: function(error){
					updateMessageListParseFail();
				}
			});
		});
  	};

	var updateContent = function(data){
		$scope.$apply(function() {
  			$scope.loading = false;
			if(data['session']){
				$scope.noSession = false;
				$scope.session = true;
				getProfile();
				$scope.readPage();
				
			}
			else{
				$scope.noSession = true;
				$scope.session = false;
			}
		});		
	};

	var start = function(){
 		var url = $scope.host + 'plugin/api/plugin/check-session';  		
	  	$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			success: function(data){
				updateContent(data);
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
	};

	start();

	$scope.openHome = function(){
  		var url = $scope.hostUser + '#/';
  		chrome.tabs.create({ url: url });
  	};

  	$scope.viewRems = function(){
  		var url = $scope.hostUser + '#/reminders';
  		chrome.tabs.create({ url: url });
  	};

  	$scope.manageTasks = function(){
  		var url = $scope.hostUser + '#/';
  		chrome.tabs.create({ url: url  });
  	};

  	$scope.loginPage = function(){
  		var url = $scope.host + '#/';
  		chrome.tabs.create({ url: url  });
  	};

}]);