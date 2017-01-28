app.controller('sentController', ['$scope','$location','$mdSidenav','$mdDialog', function($scope,$location,$mdSidenav,$mdDialog){

	$scope.sInd = 1;
	$scope.eInd = 0;
	$scope.no_of_msg = 0;
	$scope.total = 0;
	$scope.allmails = false;
	$scope.sel = false;
	$scope.loading = true;
	$scope.mails_present = false;
	$scope.no_mails = false;
	$scope.next_but = true;
	$scope.prev_but = false;
	
	$scope.messagesMain = [];

	$scope.messages = [];

	var anyMailSelected = function(){
		for(var i = 0; i<$scope.messages.length; i++){
			if($scope.messages[i].selected){
				return true;
			}
		}
		return false;
	};

	$scope.selAll = function(){
		$scope.allmails = true;
		for(var i = 0; i<$scope.messages.length; i++){
			$scope.messages[i].selected = true;
		}
	};

	$scope.deSelAll = function(){
		$scope.allmails = false;
		$scope.sel = false;
		for(var i = 0; i<$scope.messages.length; i++){
			$scope.messages[i].selected = false;
		}
	};

	$scope.starMail = function(id){
		for(var i = 0; i<$scope.messages.length; i++){
			if($scope.messages[i].id === id){
				$scope.messages[i].starred = true;
			}
		}
	};

	$scope.deStarMail = function(id){
		for(var i = 0; i<$scope.messages.length; i++){
			if($scope.messages[i].id === id){
				$scope.messages[i].starred = false;
			}
		}
	};

	$scope.impMail = function(id){
		for(var i = 0; i<$scope.messages.length; i++){
			if($scope.messages[i].id === id){
				$scope.messages[i].important = true;
			}
		}
	};

	$scope.deImpMail = function(id){
		for(var i = 0; i<$scope.messages.length; i++){
			if($scope.messages[i].id === id){
				$scope.messages[i].important = false;
			}
		}
	};

	$scope.selectMail = function(id){
		for(var i = 0; i<$scope.messages.length; i++){
			if($scope.messages[i].id === id){
				$scope.messages[i].selected = true;
				$scope.sel = true;
			}
		}
	};

	$scope.deSelectMail = function(id){
		for(var i = 0; i<$scope.messages.length; i++){
			if($scope.messages[i].id === id){
				$scope.messages[i].selected = false;
				if(!anyMailSelected()) $scope.deSelAll();
			}
		}
	};

	$scope.openMail = function(id){
		$location.url('/mails/view/'+id);
	};

	var updateInboxInfoStart = function(data){
		$scope.$apply(function() {
  			$scope.loading = false;
			$scope.total = data['mails'].length;
			$scope.sInd = 1;
			$scope.eInd = data['no_of_msg'];
			$scope.no_of_msg = data['no_of_msg'];
			$scope.messagesMain = data['mails'];
			if ($scope.total == 0){
				$scope.mails_present = false;
				$scope.no_mails = true;				
				if($scope.total <= $scope.no_of_msg){
					$scope.prev_but = false;
					$scope.next_but = false;
				}
			}else{
				$scope.mails_present = true;
				$scope.no_mails = false;
			}
		});
		$scope.startShowMails();
	};

	var start = function(){
		var for_type = 'sent';	
	  	$.ajax({
			url: 'api/user/mails/info',
			type: 'POST',
			dataType: 'json',
			data:{
				for: for_type
			},
			success: function(data){
				updateInboxInfoStart(data);
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
  	};

  	var updateMessages = function(index,data){
  		$scope.$apply(function() {
	  		$scope.messages[index]['starred'] = data['starred'];
	  		$scope.messages[index]['important'] = data['important'];
	  		$scope.messages[index]['time'] = data['time'];
	  		$scope.messages[index]['subject'] = data['subject'];
	  		$scope.messages[index]['files_attch'] = data['files_attch'];
	  		$scope.messages[index]['to'] = data['to'];
	  	});
  	};

  	var showMailHelper = function(index, mailID){
  		var for_type = 'sent';	
	  	$.ajax({
			url: 'api/user/mails/get',
			type: 'POST',
			dataType: 'json',
			data:{
				for: for_type,
				mailID: mailID
			},
			success: function(data){
				updateMessages(index, data);
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
  	};

  	$scope.showMails = function(){
  		$scope.messages = [];
  		var ind = 0;
  		for(var i = ($scope.sInd - 1); i < $scope.eInd; i++){
  			var mailID = $scope.messagesMain[i]['id'];
  			$scope.messages[ind] = {
  				id: mailID,
  				selected: false,
				starred: false,
				important: false,
				time: "",
				subject: "",
				files_attch: false,
				to: ""
  			};
  			showMailHelper(ind,mailID);
  			ind = ind + 1;
  		}
  	};

  	$scope.startShowMails = function(){
  		$scope.showMails();
  	};

  	$scope.next = function(){
  		$scope.prev_but = true;
  		$scope.next_but = true;
  		if($scope.eInd + $scope.no_of_msg > $scope.total){
  			$scope.next_but = false;
  			$scope.sInd = $scope.sInd + $scope.no_of_msg;
  			$scope.eInd = $scope.total;
  		}else{						
  			$scope.sInd = $scope.sInd + $scope.no_of_msg;
  			$scope.eInd = $scope.eInd + $scope.no_of_msg;
  		}
  		$scope.showMails();
  	};

  	$scope.prev = function(){
  		$scope.prev_but = true;
  		$scope.next_but = true;
  		if($scope.sInd - $scope.no_of_msg == 1){
  			$scope.prev_but = false;
  			$scope.sInd = 1;
  			$scope.eInd = $scope.no_of_msg;
  		}else if($scope.eInd == $scope.total){						
  			$scope.sInd = $scope.sInd - $scope.no_of_msg;
  			$scope.eInd = $scope.sInd + $scope.no_of_msg - 1;
  		}else{
  			$scope.sInd = $scope.sInd - $scope.no_of_msg;
  			$scope.eInd = $scope.eInd - $scope.no_of_msg;
  		}
  		$scope.showMails();
  	};

  	$scope.refresh = function(){
  		$scope.loading = true;
  		$scope.no_mails = false;
  		$scope.mails_present = false;
  		start();
  	};

  	start();


}]);