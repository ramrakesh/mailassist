app.controller('keywordsController', ['$scope','$location','$mdSidenav','$mdDialog','$mdPanel', function($scope,$location,$mdSidenav,$mdDialog,$mdPanel){

	$scope.keys = [];
	$scope.keywords = [];
	$scope.loading = true;
	$scope.newKey = {
		key: '',
		action: ''
	};
	$scope.addRemTemp = false;
	$scope.addRemError = "";
	$scope.addRemErrorP = false;
	$scope.loading = true;
	$scope.addRemLoading = false;

	var refreshForm = function(){
		$scope.newKey.key = '';
		$scope.newKey.action = '';
		$scope.validKey = false;
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
	        if(!arr.contains(this[i].key)) {
	            arr.push(this[i].key);
	        }
	    }
	    return arr; 
	}

	var getKeys = function(){
		$scope.keys = $scope.keywords.unique();
	};

	var updateKeywords = function(data){
		$scope.loading = false;
		if(data.keywords.length == 0 || (data.keywords.length == 1 && data.keywords[0].key == "")){
			$scope.no_key = true;
			$scope.key_present = false;
		}else{
			$scope.keywords = data.keywords;
			$scope.key_present = true;
			$scope.no_key = false;
		}		
  		getKeys();
	};

	$scope.validForm = function(){
  		if($scope.newKey.key == '' || $scope.newKey.action == ''){
  			return false;
  		}
  		return true;
  	};

	$scope.addNewKey = function() {
  		$scope.addKeyError = "";
  		$scope.addkeyErrorP = false;
  		$scope.addKeyLoading = true;
  		if(!$scope.validForm()){
  			$scope.addKeyError = "Please fill out both the details";
  			$scope.addKeyErrorP = true;
  			$scope.addKeyLoading = false;
  		}else{
  			$.ajax({
				url: 'api/user/keywords/add',
				type: 'POST',
				dataType: 'json',
				data: {
					key: $scope.newKey.key,
					action: $scope.newKey.action
				},
				success: function(data){
					updateKeywords(data);
					refreshForm();
					Materialize.toast('Keyword Added!', 4000);
					$scope.$apply(function() {
			  			$scope.addKeyLoading = false;
					});	
				},
				error: function(error){
					$scope.$apply(function() {
			  			$scope.addKeyError = "Some Error Occured!. Please Try Again!";
			  			$scope.addKeyErrorP = true;
			  			$scope.addKeyLoading = false;
			  		});
				}
			});
		}
  	};

  	$scope.addActionHelper = function(key,result) {
		$.ajax({
			url: 'api/user/keywords/add',
			type: 'POST',
			dataType: 'json',
			data: {
				action: result,
				key: key
			},
			success: function(data){
				updateKeywords(data);
				Materialize.toast('Action Added!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.addActionInvalid = function(key) {
		var confirm = $mdDialog.prompt()
      	.title('Add new action...')
      	.textContent('Please provide some action')
      	.placeholder('Action')
      	.ariaLabel('Action')
      	.initialValue('')
      	.ok('Add Action!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.addActionInvalid(key);
    		$scope.addActionHelper(key,result);
    	}, function() {
    	});
  	};

  	$scope.addAction = function(ev,key) {
		var confirm = $mdDialog.prompt()
      	.title('Add new action for '+key+'...')
      	.textContent('')
      	.placeholder('Action')
      	.ariaLabel('Action')
      	.initialValue('')
      	.targetEvent(ev)
      	.ok('Add Action!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.addActionInvalid(key);
    		$scope.addActionHelper(key,result);
    	}, function() {
    	});
  	};

  	$scope.keyEditHelper = function(key,result) {
		$.ajax({
			url: 'api/user/keywords/key/edit',
			type: 'POST',
			dataType: 'json',
			data: {
				key: key,
				newkey: result
			},
			success: function(data){
				updateKeywords(data);
				Materialize.toast('Keyword Updated!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.keyEditInvalid = function(key) {
		var confirm = $mdDialog.prompt()
      	.title('Edit keyword...')
      	.textContent('Please provide some keyword')
      	.placeholder('New Keyword')
      	.ariaLabel('New Keyword')
      	.initialValue('')
      	.ok('Update Keyword!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.keyEditInvalid(key);
    		$scope.keyEditHelper(key,result);
    	}, function() {
    	});
  	};

  	$scope.keyEdit = function(ev,key) {
		var confirm = $mdDialog.prompt()
      	.title('Edit keyword...')
      	.textContent('Current Keyword: '+key)
      	.placeholder('New Keyword')
      	.ariaLabel('New Keyword')
      	.initialValue(key)
      	.targetEvent(ev)
      	.ok('Update Keyword!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.keyEditInvalid(key);
    		$scope.keyEditHelper(key,result);
    	}, function() {
    	});
  	};

  	$scope.actionEditHelper = function(id,result) {
		$.ajax({
			url: 'api/user/keywords/action/edit',
			type: 'POST',
			dataType: 'json',
			data: {
				id: id,
				action: result
			},
			success: function(data){
				updateKeywords(data);
				Materialize.toast('Action Updated!', 4000);
			},
			error: function(error){
				Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
			}
		});
  	};

  	$scope.actionEditInvalid = function(id) {
		var confirm = $mdDialog.prompt()
      	.title('Edit action...')
      	.textContent('Please provide some action')
      	.placeholder('New Action')
      	.ariaLabel('New Action')
      	.initialValue('')
      	.ok('Update Action!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.actionEditInvalid(id);
    		$scope.actionEditHelper(id,result);
    	}, function() {
    	});
  	};

  	$scope.actionEdit = function(ev,key,action,id) {
		var confirm = $mdDialog.prompt()
      	.title('Edit action for Keyword: '+key+'...')
      	.textContent('Current Action: '+action)
      	.placeholder('New Action')
      	.ariaLabel('New Action')
      	.initialValue(action)
      	.targetEvent(ev)
      	.ok('Update Action!')
      	.cancel('Cancel');
    	
    	$mdDialog.show(confirm).then(function(result) {
    		if(!result || result == '') $scope.actionEditInvalid(id);
    		$scope.actionEditHelper(id,result);
    	}, function() {
    	});
  	};

	$scope.dismissAction = function(ev,id){
  		var confirm = $mdDialog.confirm()
        .title('Would you like to remove this Action?')
        .ariaLabel('Would you like to remove this Action?')
        .targetEvent(ev)
        .ok('Yes!')
        .cancel('Cancel');
    	$mdDialog.show(confirm).then(function() {
      		$.ajax({
				url: 'api/user/keywords/action/del',
				type: 'POST',
				dataType: 'json',
				data: {
					id: id
				},
				success: function(data){
					updateKeywords(data);
					Materialize.toast('Action Removed!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});
    	}, function() {
    	});
  	};

  	$scope.dismissKey = function(ev,key){
  		var confirm = $mdDialog.confirm()
        .title('Would you like to remove '+key+' from the set of Keywords?')
        .ariaLabel('Would you like to remove '+key+' from the set of Keywords?')
        .targetEvent(ev)
        .ok('Yes!')
        .cancel('Cancel');
    	$mdDialog.show(confirm).then(function() {
      		$.ajax({
				url: 'api/user/keywords/del',
				type: 'POST',
				dataType: 'json',
				data: {
					key: key
				},
				success: function(data){
					updateKeywords(data);
					Materialize.toast('Keyword Removed!', 4000);
				},
				error: function(error){
					Materialize.toast('Some Error Occurred. Please Refresh!', 4000);
				}
			});
    	}, function() {
    	});
  	};

	var start = function(){
		$.ajax({
			url: 'api/user/keywords/get',
			type: 'POST',
			dataType: 'json',
			success: function(data){
				$scope.$apply(function() {
					$scope.loading = false;
					updateKeywords(data);
				});
			},
			error: function(error){
				alert("Some Error Occurred. Please Refresh");
			}
		});
	};

	$scope.openKeyConsole = function(){
		$scope.addKeyTemp = true;
	};

	$scope.closeKeyConsole = function(){
		$scope.addKeyTemp = false;
	};

	start();

}]);