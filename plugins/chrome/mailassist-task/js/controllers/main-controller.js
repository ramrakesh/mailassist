app.controller('mailAssistController', ['$scope','$location','$mdSidenav','$mdDialog', function($scope,$location,$mdSidenav,$mdDialog){

	$scope.host = 'https://mailassist.herokuapp.com/'
	$scope.hostUser = $scope.host + 'user/'

	$scope.noSession = false;
	$scope.session = false;
	$scope.loading = true;
	$scope.loadingTask = true;
	$scope.name = 'User';
	$scope.email = 'someone@example.com';
	$scope.deskNot = false;
	$scope.timeNot = null;

	$scope.taskShow = {
		task: '',
		content: '',
		subject: '',
		sender: '',
		link: '',
		notif: ''
	};

	$scope.tasks = [];
	$scope.task_nos = '';

	var date = new Date();
	var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
	
	$scope.date_text = date.getDate() + "-" + months[date.getMonth()] + "-" + date.getFullYear();

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
  			$scope.loadingTask = false;
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

  	$scope.checkTask = function(id){
  		var url = $scope.hostUser + 'api/user/tasks/check'; 
  		$.ajax({
			url: url,
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
  		var url = $scope.hostUser + 'api/user/tasks/uncheck'; 
  		$.ajax({
			url: url,
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
					$scope.deskNot = data['deskNot'];
					$scope.timeNot = data['timeNot'];
				});
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
  	};

  	var startSession = function(){
  		var url = $scope.hostUser + 'api/user/tasks';   		
	  	$.ajax({
			url: url,
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

 	var updateContent = function(data){
		$scope.$apply(function() {
  			$scope.loading = false;
			if(data['session']){
				$scope.noSession = false;
				$scope.session = true;
				startSession();
				getProfile();
			}
			else{
				$scope.noSession = true;
				$scope.session = false;
			}
		});		
	};

	$scope.viewTask = function(id){
  		for(var i = 0; i<$scope.tasks.length; i++){
			if($scope.tasks[i]['id'] == id){
				$scope.taskShow.task = $scope.tasks[i]['task'];
				$scope.taskShow.notif = $scope.tasks[i]['notif'];					
				$scope.taskShow.content = showMsgContent($scope.tasks[i]['content']);					
				$scope.taskShow.subject = $scope.tasks[i]['subject'];					
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

	

	// refreshTemp();
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