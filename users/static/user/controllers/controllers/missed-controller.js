app.controller('missedReminderController', ['$scope','$location','$mdSidenav','$mdDialog','$mdPanel', function($scope,$location,$mdSidenav,$mdDialog,$mdPanel){

	$scope.addRemTemp = false;
	$scope.addRemError = "";
	$scope.addRemErrorP = false;
	$scope.addRemLoading = false;

	$scope.taskShow = {
		task: '',
		content: '',
		subject: '',
		sender: '',
		link: '',
		date: '',
		notif: ''
	};

	var date = new Date();
	var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
	var days = ['Sunday','Monday','Tuesday','Wednesday','Thusrday','Friday','Saturday'];
	
	$scope.dates = [];

	$scope.getDay = function(dateStr){
		var match1 = Number(dateStr.split('-')[2]) + "-" + Number(dateStr.split('-')[1]) + "-" + dateStr.split('-')[0];
		var match2 = date.getDate() + "-" + (Number(date.getMonth()) + 1) + "-" + date.getFullYear();
		var JSDay = new Date(dateStr.split('-')[0] + "-" + dateStr.split('-')[1] + "-" + dateStr.split('-')[2]);
		var curday = days[JSDay.getDay()];
		if(match1 == match2) return 'Today';
		else if(Number(dateStr.split('-')[2]) == ((Number(date.getDate()) - 1))) return 'Yesterday';
		return curday;
	};

	$scope.conDate = function(date){
		return date.split('-')[2] + " " + months[date.split('-')[1]-1] + ", " + date.split('-')[0];
	};

	function strip(html){
	   var tmp = document.createElement("DIV");
	   tmp.innerHTML = html;
	   return tmp.textContent || tmp.innerText || "";
	}

  	var showMsgContent = function(content){
  		var resp = content;
  		if(resp.length > 150)
  			resp = resp.substring(0,150) + '...';
  		return strip(resp);
  	};

	$scope.dropDownIdGen = function(date){
		return 'dropdown-'+date;
	}
	$scope.tasks = [];

	var updateTasks = function(data){
		$scope.$apply(function() {
  			$scope.loading = false;
			if(data.length == 0){
				$scope.no_task = true;
				$scope.tasks_present = false;
			}
			else{
				$scope.tasks = data;
				$scope.tasks_present = true;
				$scope.no_task = false;
			}
		});		
  		getDates();
	};

	$scope.newRem = {
		rem: '',
		date: ''
	};

	var refreshTemp = function(){
		$scope.loading = true;
		$scope.no_task = false;
		$scope.tasks_present = false;
	};

	var refreshForm = function(){
		$scope.newRem.rem = '';
		$scope.newRem.date = '';
	};

	Array.prototype.contains = function(v) {
    	for(var i = 0; i < this.length; i++) {
        	if(this[i] === v) return true;
    	}
    	return false;
	}

	Array.prototype.unique = function() {
	    var arr = [];
	    for(var i = 0; i < this.length; i++) {
	        if(!arr.contains(this[i].date)) {
	            arr.push(this[i].date);
	        }
	    }
	    return arr; 
	}

	var getDates = function(){
		$scope.dates = $scope.tasks.unique();
	};

  	$scope.checkAll = function(ev,date,date_text) {
		var confirm = $mdDialog.confirm()
      	.title('Mark all tasks on '+date_text+' as Completed?')
      	.ariaLabel('Would you like to mark all tasks on '+date_text+' as Completed?')
      	.targetEvent(ev)
      	.ok('Yes!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		$.ajax({
				url: 'api/user/missed/check/all',
				type: 'POST',
				dataType: 'json',
				data: {
					date: date
				},
				success: function(data){
					updateTasks(data['tasks']);
					Materialize.toast('All Tasks on '+date_text+' are Completed Now!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});
    	}, function() {
    	});
  	};

  	$scope.unCheckAll = function(ev,date,date_text) {
		var confirm = $mdDialog.confirm()
      	.title('Mark all tasks on '+date_text+' as Pending?')
      	.ariaLabel('Would you like to mark all tasks on '+date_text+' as Pending?')
      	.targetEvent(ev)
      	.ok('Yes!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		$.ajax({
				url: 'api/user/missed/uncheck/all',
				type: 'POST',
				dataType: 'json',
				data: {
					date: date
				},
				success: function(data){
					updateTasks(data['tasks']);
					Materialize.toast('All Tasks on '+date_text+' are Pending Now!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});
    	}, function() {
    	});
  	};

  	$scope.dismissAll = function(ev,date,date_text) {
		var confirm = $mdDialog.confirm()
      	.title('Would you like to dismiss all the tasks on '+date_text+'?')
      	.ariaLabel('Would you like to dismiss all the tasks on '+date_text+'?')
      	.targetEvent(ev)
      	.ok('Yes!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		$.ajax({
				url: 'api/user/missed/del/all',
				type: 'POST',
				dataType: 'json',
				data: {
					date: date
				},
				success: function(data){
					updateTasks(data['tasks']);
					Materialize.toast('All Tasks on '+date_text+' are Dismissed!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});
    	}, function() {
    	});
  	};

  	$scope.validForm = function(){
  		if($scope.newRem.rem == '' || $scope.newRem.date == ''){
  			return false;
  		}
  		return true;
  	};

  	var makedate = function(date){
  		var monthD = {
  			'January': '1',
  			'February': '2',
  			'March': '3',
  			'April': '4',
  			'May': '5',
  			'June': '6',
  			'July': '7',
  			'August': '8',
  			'September': '9',
  			'October': '10',
  			'November': '11',
  			'December': '12'
  		}
  		var y = date.split(', ')[1];
  		var md = date.split(', ')[0]
  		var m = monthD[md.split(' ')[1]];
  		var d = md.split(' ')[0];
  		return y + '-' + m + '-' + d;
  	};

  	$scope.dismissTask = function(ev,id){
  		var confirm = $mdDialog.confirm()
        .title('Would you like to dismiss this Reminder?')
        .ariaLabel('Would you like to dismiss this Reminder?')
        .targetEvent(ev)
        .ok('Yes!')
        .cancel('Cancel');
    	$mdDialog.show(confirm).then(function() {
      		$.ajax({
				url: 'api/user/missed/del',
				type: 'POST',
				dataType: 'json',
				data: {
					id: id
				},
				success: function(data){
					updateTasks(data['tasks']);
					Materialize.toast('Reminder Dismissed!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});
    	}, function() {
    	});
  	};

  	$scope.checkRem = function(id){
  		$.ajax({
			url: 'api/user/missed/check',
			type: 'POST',
			dataType: 'json',
			data: {
				id: id
			},
			success: function(data){
				updateTasks(data['tasks']);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.unCheckRem = function(id){
  		$.ajax({
			url: 'api/user/missed/uncheck',
			type: 'POST',
			dataType: 'json',
			data: {
				id: id
			},
			success: function(data){
				updateTasks(data['tasks']);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.viewTask = function(id){
  		for(var i = 0; i<$scope.tasks.length; i++){
			if($scope.tasks[i]['id'] == id){
				$scope.taskShow.task = $scope.tasks[i]['task'];
				$scope.taskShow.notif = $scope.tasks[i]['notif'];					
				$scope.taskShow.content = showMsgContent($scope.tasks[i]['content']);
				if($scope.tasks[i]['subject'] != '')					
					$scope.taskShow.subject = $scope.tasks[i]['subject'];
				else					
					$scope.taskShow.subject = 'No Subject';
				$scope.taskShow.sender = $scope.tasks[i]['sender'];					
				$scope.taskShow.date = $scope.conDate($scope.tasks[i]['date']);
				$scope.taskShow.link = '';
				switch($scope.tasks[i]['mailer']){
					case 'gmail':
						$scope.taskShow.link = 'https://mail.google.com/mail/u/0/#inbox/'+$scope.tasks[i]['threadID'];
						break;
				}					
			}				
		}
		$('#modal1').openModal();
  	};

  	var start = function(){  		
	  	$.ajax({
			url: 'api/user/missed',
			type: 'GET',
			dataType: 'json',
			success: function(data){
				updateTasks(data['tasks']);
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
  	};

	$scope.openRemConsole = function(){
		$scope.addRemTemp = true;
	};

	$scope.closeRemConsole = function(){
		$scope.addRemTemp = false;
	};

  	refreshTemp();
  	start();

}]);