'use strict';
/**
 * @ngdoc overview
 * @name marketApp
 * @description
 * # marketApp
 *
 * Main module of the application.
 */
var app = angular.module('wechatBot', [
  'ui.router',
  'servData',
  'Authentication'
]).config([
  '$stateProvider','$urlRouterProvider', '$compileProvider',
  function ($stateProvider,$urlRouterProvider,$compileProvider) {

    $compileProvider.imgSrcSanitizationWhitelist(/^\s*(https?|local|data|chrome-extension):/);

    $urlRouterProvider.when('', '/index/home');
    $urlRouterProvider.when('/', '/index/home');
    $urlRouterProvider.otherwise('/notfound');

    $stateProvider.state('index', {
      url:'/index',
      templateUrl: '/static/views/template.html',
      controller: 'MainCtrl'
    }).state('index.home', {
      url:'/home',
      templateUrl: '/static/views/index.html'
    }).state('index.login', {
      url:'/login',
      templateUrl: '/static/views/login.html',
      controller:'LoginCtrl'
    });
}
]).run(['$rootScope', '$location', function($rootScope, $location){
  $rootScope.host = '/';

  $rootScope.$on('$locationChangeStart', function (event, next, current) {
    if(!$rootScope.isLoggedIn){
      $location.path('/index/login');
    }
  });
}]);
