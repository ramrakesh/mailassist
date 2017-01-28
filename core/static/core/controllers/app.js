var app = angular.module('mailAssistApp',['ngMessages','ngResource','ngRoute','ngMaterial']);

app.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl: '/MailAssistCoreTemplates/index-template.html'
	})
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