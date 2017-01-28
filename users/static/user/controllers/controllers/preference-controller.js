app.controller('preferenceController', ['$scope','$location','$mdSidenav','$mdDialog','$mdPanel', function($scope,$location,$mdSidenav,$mdDialog,$mdPanel){

	$scope.appNot = true;
	$scope.smsNot = false;
	$scope.deskNot = true;
	$scope.timeNot = '08:45 AM';
	$scope.mob = '9559100337';
	$scope.mobVer = true;
	$scope.emailNo = 100;
	$scope.timePer = 10;
	$scope.timePerTextVal = '';
	$scope.timeNotEdit = false;
	$scope.emailNoEdit = false;
	$scope.timePerEdit = false;
	$scope.timeModify = {
		hh: 08,
		mm: 45,
		tm: 'AM'
	};
	$scope.emailNoModify = {val:100};
	$scope.timePerModify = {val:7};
	$scope.loading = true;
	$scope.addRemTemp = false;
	$scope.addRemError = "";
	$scope.addRemErrorP = false;
	$scope.loading = true;
	$scope.addRemLoading = false;

	var timeEditValuesUpdate = function(){
		$scope.timeModify.hh = Number($scope.timeNot.split(':')[0]);
		$scope.timeModify.mm = Number($scope.timeNot.split(':')[1].split(' ')[0]);
		$scope.timeModify.tm = $scope.timeNot.split(':')[1].split(' ')[1];
	};

	var timeValuesUpdate = function(){
		$scope.$apply(function() {
			$scope.timeNot = $scope.timeModify.hh + ':' + $scope.timeModify.mm + ' ' + $scope.timeModify.tm;
			$scope.timeNotEdit = false;
			if($scope.deskNot) $scope.deskNot = false;
			else $scope.deskNot = true;	
		});
		$('#update-ton').closeModal();
	};

	var emailNoUpdate = function(){
		$scope.$apply(function() {
			$scope.emailNo = $scope.emailNoModify.val;
		});
		$('#update-ene').closeModal();
	};

	var phoneNoUpdate = function(phone){
		$scope.$apply(function() {
			$scope.mob = phone;
			$scope.mobVer = false;
		});
	};

	var updatePhoneFinal = function(){
		$scope.$apply(function() {
			$scope.mobVer = true;
		});
	};

	$scope.timePerText = function(tp){
		switch(tp){
			case 1:
				return 'Last 1 day';
				break;
			case 7:
				return 'Last 1 week';
				break;
			case 14:
				return 'Last 2 weeks';
				break;
			case 30:
				return 'Last 1 month';
				break;
		}
	};

	var timePerUpdate = function(){
		$scope.$apply(function() {
			$scope.timePer = $scope.timePerModify.val;
			$scope.timePerTextVal = $scope.timePerText(Number($scope.timePerModify.val));
		});
		$('#update-tpe').closeModal();
	};

	$scope.timeNotToggle = function(){
		if($scope.timeNotEdit) {
			$scope.timeNotEdit = false;
			$('#update-ton').closeModal();
		}
		else{
			$scope.timeNotEdit = true;
			$('#update-ton').openModal();
		}
	};

	$scope.emailNoToggle = function(){
		if($scope.emailNoEdit){
			$scope.emailNoEdit = false;
			$('#update-ene').closeModal();
		}
		else{
			$scope.emailNoEdit = true;
			$('#update-ene').openModal();
		}
	};

	$scope.timePerToggle = function(){
		if($scope.timePerEdit){
			$scope.timePerEdit = false;
			$('#update-tpe').closeModal();
		}
		else{
			$scope.timePerEdit = true;
			$('#update-tpe').openModal();
		}
	};

	$scope.appNotToggle = function(){
		$.ajax({
			url: 'api/user/settings/appNot/toggle',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				Materialize.toast('Setting Saved!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	};

	$scope.smsNotToggle = function(){
		$.ajax({
			url: 'api/user/settings/smsNot/toggle',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				Materialize.toast('Setting Saved!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	};

	$scope.browserNotToggle = function(){
		$.ajax({
			url: 'api/user/settings/browserNot/toggle',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				var event = document.createEvent('Event');
				if($scope.deskNot){
					event.initEvent('set-notification');
				}
        		else
        			event.initEvent('del-notification');
        		document.dispatchEvent(event);
				Materialize.toast('Setting Saved!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	};

	$scope.updateTime = function(){
		$.ajax({
			url: 'api/user/settings/update-time-of-notification',
			type: 'POST',
			dataType: 'json',
			data : {
				time: $scope.timeModify.hh + ':' + $scope.timeModify.mm + ' ' + $scope.timeModify.tm
			},
			success: function(data){
				timeValuesUpdate();
				$scope.browserNotToggle();
				Materialize.toast('Time of Notification Changed!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	};

	$scope.updateEmailNo = function(){
		$.ajax({
			url: 'api/user/settings/update-number-of-email',
			type: 'POST',
			dataType: 'json',
			data : {
				val: $scope.emailNoModify.val
			},
			success: function(data){
				emailNoUpdate();
				Materialize.toast('Number of Emails Changed!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	};

	$scope.updateTimePer = function(){
		$.ajax({
			url: 'api/user/settings/update-time-period',
			type: 'POST',
			dataType: 'json',
			data : {
				val: $scope.timePerModify.val
			},
			success: function(data){
				timePerUpdate();
				Materialize.toast('Time Period Changed!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	};

	function phonenumber(inputtxt){  
  		var phoneno = /^\d{10}$/;  
  		if(inputtxt.match(phoneno)){  
      		return true;  
        }else{  
        	return false;  
        }  
	};

	$scope.invalidCode = function(errorText){
		var confirm = $mdDialog.prompt()
      	.title('Invalid verification code')
      	.textContent(errorText)
      	.placeholder('Verification Code')
      	.ariaLabel('Verification Code')
      	.initialValue('')
      	.ok('Submit!')
      	.cancel('Cancel');

		$mdDialog.show(confirm).then(function(result) {
    		$scope.sendVerCode(result);
    	}, function() {
    	});
	};

	$scope.sendVerCode = function(result){
		$.ajax({
			url: 'api/user/settings/update-phone-verification',
			type: 'POST',
			dataType: 'json',
			data : {
				code: result
			},
			success: function(data){
				if(data.done){
					Materialize.toast('Mob Number Updated!', 4000);
					updatePhoneFinal();
				}else{
					$scope.invalidCode(data.error);
				}
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	};

	$scope.verificationPhone = function(){
		var confirm = $mdDialog.prompt()
      	.title('Phone Number verification')
      	.textContent('Please enter verification code we have sent you on your phone number')
      	.placeholder('Verification Code')
      	.ariaLabel('Verification Code')
      	.initialValue('')
      	.ok('Submit!')
      	.cancel('Cancel');

		$mdDialog.show(confirm).then(function(result) {
    		$scope.sendVerCode(result);
    	}, function() {
    	});
	};

	$scope.validPhone = function(phone){
		$.ajax({
			url: 'api/user/settings/update-phone',
			type: 'POST',
			dataType: 'json',
			data : {
				phone: phone
			},
			success: function(data){
				phoneNoUpdate(phone);
				$scope.verificationPhone();
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	}

	$scope.verificationPhoneNew = function(){
		$scope.validPhone($scope.mob);
	};

	$scope.invalidPhone = function(){
		var confirm = $mdDialog.prompt()
      	.title('Invalid Phone Number')
      	.textContent('Please enter a valid Phone Number (XXXXXXXXXX)')
      	.placeholder('Phone')
      	.ariaLabel('Phone')
      	.initialValue('')
      	.ok('Add Phone!')
      	.cancel('Cancel');

		$mdDialog.show(confirm).then(function(result) {
    		if(!phonenumber(result)){
    			$scope.invalidPhone();
    		}else{
    			$scope.validPhone(result);
    		}
    	}, function() {
    	});
	}

	$scope.addPhone = function(ev){
		var confirm = $mdDialog.prompt()
      	.title('Please Provide Phone Number')
      	.textContent('After you update your phone Number, we will send you a verification code through SMS for verification.')
      	.placeholder('Phone')
      	.ariaLabel('Phone')
      	.initialValue('')
      	.targetEvent(ev)
      	.ok('Add Phone!')
      	.cancel('Cancel');

		$mdDialog.show(confirm).then(function(result) {
    		if(!phonenumber(result)){
    			$scope.invalidPhone();
    		}else{
    			$scope.validPhone(result);
    		}
    	}, function() {
    	});
	};

	var start = function(){
		$.ajax({
			url: 'api/user/settings/get',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				$scope.$apply(function() {
					$scope.loading = false;
					$scope.appNot = data.appNot;
					$scope.smsNot = data.smsNot;
					$scope.deskNot = data.deskNot;
					$scope.timeNot = data.timeNot;
					$scope.mob = data.mob;
					$scope.mobVer = data.mobVer;
					$scope.emailNo = data.emailNo;
					$scope.timePer = data.timePer;
					$scope.timePerTextVal = $scope.timePerText($scope.timePer);
					$scope.emailNoModify.val = data.emailNo;
					$scope.timePerModify.val = data.timePer;
					timeEditValuesUpdate();
				});
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
	};

	start();

}]);