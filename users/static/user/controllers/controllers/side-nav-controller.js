app.controller('sideNavController', ['$scope','$location','$mdSidenav','$mdDialog', function($scope,$location,$mdSidenav,$mdDialog){

	$scope.name = '';
	$scope.email = '';
	$scope.picture = false;
	$scope.pictureURL = '';

	var resetTabs = function(){
		$scope.inbox = false;
		$scope.sent = false;
		$scope.index = false;
		$scope.reminders = false;
		$scope.preferences = false;
		$scope.keywords = false;
		$scope.missed = false;
	};

	$scope.changePage = function(page){
		switch(page){
			case '':
				resetTabs();
				break;
			case 'index':
				resetTabs();
				$scope.index = true;
				$location.url('/');
				break;
			case 'inbox':
				resetTabs();
				$scope.inbox = true;
				$location.url('/inbox');
				break;
			case 'sent':
				resetTabs();
				$scope.sent = true;
				$location.url('/sent');
				break;
			case 'reminders':
				resetTabs();
				$scope.reminders = true;
				$location.url('/reminders');
				break;
			case 'preferences':
				resetTabs();
				$scope.preferences = true;
				$location.url('/preferences');
				break;
			case 'keywords':
				resetTabs();
				$scope.keywords = true;
				$location.url('/keywords');
				break;
			case 'history':
				resetTabs();
				$scope.missed = true;
				$location.url('/history');
				break;
			case 'compose':
				resetTabs();
				$location.url('/compose');
				break;
			default:
				resetTabs();
		}
	};

	var checkURL = function(){
		var url = $location.url();
		var path = url.split('/')[1];
		switch(path){
			case '':
				$scope.changePage('index');
				break;
			case 'inbox':
				$scope.changePage('inbox');
				break;
			case 'sent':
				$scope.changePage('sent');
				break;
			case 'reminders':
				$scope.changePage('reminders');
				break;
			case 'preferences':
				$scope.changePage('preferences');
				break;
			case 'keywords':
				$scope.changePage('keywords');
				break;
			case 'history':
				$scope.changePage('history');
				break;
			case 'compose':
				$scope.changePage('compose');
				break;
			default:
				resetTabs();
		}
	};

	checkURL();

	$.ajax({
		url: 'api/user/profile-info',
		type: 'GET',
		dataType: 'json',
		success: function(data){
			$scope.name = data['name'];
			$scope.email = data['email'];
			if (data['picture'] == '' || data['picture'] == null)
				$scope.picture = false;
			else{
				$scope.picture = true;
				$scope.pictureURL = data['picture'];
			}
		},
		error: function(error){
			alert("Some Error Occurred. Please Refresh");
		}
	});

}]);