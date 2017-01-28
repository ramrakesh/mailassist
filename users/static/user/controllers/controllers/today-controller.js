app.controller('todayController', ['$scope','$location','$mdSidenav','$mdDialog', function($scope,$location,$mdSidenav,$mdDialog){

	$scope.tasks = [];
	$scope.task_nos = '';

	$scope.taskShow = {
		task: '',
		content: '',
		subject: '',
		sender: '',
		link: '',
		notif: ''
	};

	var date = new Date();
	var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
	
	$scope.date_text = date.getDate() + "-" + months[date.getMonth()] + "-" + date.getFullYear();

	$scope.getDay = function(){
		return months[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear();
	};

	$scope.save = function(){	
		var doc = new jsPDF('p', 'pt', 'letter');

		var elementHandler = {
  			'#ignorePDF': function (element, renderer) {
    			return true;
  			}
		};

		var source = source = $('#taskList')[0];

		margins = {
            top: 15,
            bottom: 15,
            left: 40,
            width: 522
        };

        doc.fromHTML(
        	source, 
        	margins.left, 
        	margins.top, 
        	{
      		'width': margins.width,
      		'elementHandlers': elementHandler
      		},
      		function (dispose) {
      			doc.save("Tasks_" + $scope.date_text + ".pdf");
      		}, 
      		margins
      	);
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

	var getPendingTaskNo = function(tasks){
		count = 0;
		for(var i = 0; i < tasks.length; i++){
			if(tasks[i].status == 'pending') count = count + 1;
		}
		return count;
	};

	var updateTasks = function(data){
		$scope.$apply(function() {
  			$scope.loading = false;
			if(data.length == 0){
				$scope.no_task = true;
				$scope.tasks_present = false;
			}
			else{
				$scope.tasks = data;
				$scope.task_nos = getPendingTaskNo(data);
				$scope.tasks_present = true;
				$scope.no_task = false;
			}
		});		
	};

	var refreshTemp = function(){
		$scope.loading = true;
		$scope.no_task = false;
		$scope.tasks_present = false;
	};

	$scope.addTaskHelper = function(result){
		$.ajax({
			url: 'api/user/tasks/add',
			type: 'POST',
			dataType: 'json',
			data: {
				task: result
			},
			success: function(data){
				if(data['done']){
					updateTasks(data['tasks']);
					Materialize.toast('Task Added!', 4000);
				}
				else
					Materialize.toast(data['error'], 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
	};

	$scope.addTaskInvalid = function() {
    	var confirm = $mdDialog.prompt()
      	.title('Add new task...')
      	.textContent('Task field must be filled')
      	.placeholder('Task')
      	.ariaLabel('Task')
      	.initialValue('')
      	.ok('Add Task!')
      	.cancel('Cancel');

    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.addTaskInvalid();
    		else $scope.addTaskHelper(result);	
    	}, function() {
    	});
  	};

	$scope.addTask = function(ev) {
    	var confirm = $mdDialog.prompt()
      	.title('Add new task...')
      	.textContent('')
      	.placeholder('Task')
      	.ariaLabel('Task')
      	.initialValue('')
      	.targetEvent(ev)
      	.ok('Add Task!')
      	.cancel('Cancel');

    	$mdDialog.show(confirm).then(function(result) {
    		console.log();
    		if(!result || result == '') $scope.addTaskInvalid();
    		else $scope.addTaskHelper(result);
    	}, function() {
    	});
  	};

  	$scope.editTaskHelper = function(id,result) {
    	$.ajax({
			url: 'api/user/tasks/edit',
			type: 'POST',
			dataType: 'json',
			data: {
				id: id,
				task: result
			},
			success: function(data){
				if(data['done']){
					updateTasks(data['tasks']);
					Materialize.toast('Task Updated!', 4000);
				}
				else
					Materialize.toast(data['error'], 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.editTaskInvalid = function(id) {
    	var confirm = $mdDialog.prompt()
      	.title('Edit task...')
      	.textContent('Task field must be filled')
      	.placeholder('Task')
      	.ariaLabel('Task')
      	.initialValue('')
      	.ok('Update!')
      	.cancel('Cancel');

    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.editTaskInvalid(id);
    		else $scope.editTaskHelper(id,result);
    	}, function() {
    	});
  	};

  	$scope.editTask = function(ev,id,task) {
    	var confirm = $mdDialog.prompt()
      	.title('Edit task...')
      	.textContent('Current Task: '+ task)
      	.placeholder('Task')
      	.ariaLabel('Task')
      	.initialValue(task)
      	.targetEvent(ev)
      	.ok('Update!')
      	.cancel('Cancel');

    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.editTaskInvalid(id);
    		else $scope.editTaskHelper(id,result);;
    	}, function() {
    	});
  	};

  	$scope.dismissTask = function(ev,id){
  		var confirm = $mdDialog.confirm()
        .title('Would you like to dismiss this task?')
        .ariaLabel('Would you like to dismiss this task?')
        .targetEvent(ev)
        .ok('Yes!')
        .cancel('Cancel');
    	$mdDialog.show(confirm).then(function() {
    		$.ajax({
				url: 'api/user/tasks/del',
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

  	$scope.dismissAll = function(ev){
  		var confirm = $mdDialog.confirm()
        .title('Would you like to dismiss all the tasks?')
        .ariaLabel('Would you like to dismiss all the tasks?')
        .targetEvent(ev)
        .ok('Yes!')
        .cancel('Cancel');
    	$mdDialog.show(confirm).then(function() {
    		refreshTemp();
    		$.ajax({
				url: 'api/user/tasks/dismiss/all',
				type: 'POST',
				dataType: 'json',
				success: function(data){
					updateTasks(data['tasks']);
					Materialize.toast('All Tasks are Dismissed!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});      		
    	}, function() {
    	});
  	};

  	$scope.checkAll = function(ev){
  		var confirm = $mdDialog.confirm()
        .title('Mark all tasks as Completed?')
        .ariaLabel('Would you like to mark all tasks as completed?')
        .targetEvent(ev)
        .ok('Yes!')
        .cancel('Cancel');
    	$mdDialog.show(confirm).then(function() {
    		refreshTemp();
    		$.ajax({
				url: 'api/user/tasks/check/all',
				type: 'POST',
				dataType: 'json',
				success: function(data){
					updateTasks(data['tasks']);
					Materialize.toast('All Tasks are Completed Now!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});      		
    	}, function() {
    	});
  	};

  	$scope.unCheckAll = function(ev){
  		var confirm = $mdDialog.confirm()
        .title('Mark all tasks as Pending?')
        .ariaLabel('Would you like to mark all tasks as pending?')
        .targetEvent(ev)
        .ok('Yes!')
        .cancel('Cancel');
    	$mdDialog.show(confirm).then(function() {
    		refreshTemp();
    		$.ajax({
				url: 'api/user/tasks/uncheck/all',
				type: 'POST',
				dataType: 'json',
				success: function(data){
					updateTasks(data['tasks']);
					Materialize.toast('All Tasks are Pending Now!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});      		
    	}, function() {
    	});
  	};

  	$scope.checkTask = function(id){
  		$.ajax({
			url: 'api/user/tasks/check',
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

  	$scope.unCheckTask = function(id){
  		$.ajax({
			url: 'api/user/tasks/uncheck',
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
			url: 'api/user/tasks',
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

  	refreshTemp();
  	start();

}]);