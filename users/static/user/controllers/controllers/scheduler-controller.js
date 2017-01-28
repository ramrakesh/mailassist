app.controller('schedulerController', ['$scope','$location','$mdSidenav','$mdDialog', function($scope,$location,$mdSidenav,$mdDialog){

	$scope.dailyRem = function(ev){
  		$.ajax({
			url: 'api/user/scheduler/daily-reminder',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				Materialize.toast('Scheduler Running!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.upRem = function(ev){
  		$.ajax({
			url: 'api/user/scheduler/upcoming-reminder',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				Materialize.toast('Scheduler Running!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.missRem = function(ev){
  		$.ajax({
			url: 'api/user/scheduler/missed-reminder',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				Materialize.toast('Scheduler Running!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.deadRem = function(ev){
  		$.ajax({
			url: 'api/user/scheduler/deadline-reminder',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				Materialize.toast('Scheduler Running!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

}]);