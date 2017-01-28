var app = angular.module('mailAssistApp',['ngMessages','ngResource','ngRoute','ngMaterial']);

app.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl: '/user/MailAssistUserTemplates/index-template.html'
	})
	.when('/reminders', {
		templateUrl: '/user/MailAssistUserTemplates/reminders-template.html'
	})
	// .when('/inbox', {
	// 	templateUrl: '/user/MailAssistUserTemplates/inbox-template.html'
	// })
	// .when('/sent', {
	// 	templateUrl: '/user/MailAssistUserTemplates/sent-template.html'
	// })
	.when('/preferences', {
		templateUrl: '/user/MailAssistUserTemplates/preferences-template.html'
	})
	.when('/keywords', {
		templateUrl: '/user/MailAssistUserTemplates/keywords-template.html'
	})
	.when('/history', {
		templateUrl: '/user/MailAssistUserTemplates/missed-template.html'
	})
	// .when('/compose', {
	// 	templateUrl: '/user/MailAssistUserTemplates/compose-template.html'
	// })
	.when('/plugin', {
        templateUrl: '/MailAssistCoreTemplates/plugin-template.html'
    })
    .when('/mobile', {
        templateUrl: '/MailAssistCoreTemplates/mobile-template.html'
    })
    .otherwise({
        templateUrl: '/MailAssistCoreTemplates/page-not-found.html'
    });
}]);