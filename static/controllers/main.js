'use strict';

angular.module('wechatBot')

.controller('MainCtrl',
  ['$scope', '$rootScope', '$location', '$interval', 'getQR', 'startBot', 'getLoginStatus',
  function ($scope, $rootScope, $location, $interval, getQR, startBot, getLoginStatus) {
    startBot(function(data){
      console.log(data);
    });

    if(!$rootScope.status_daemo)
    {
      $rootScope.status_daemo = $interval(function(){
        getLoginStatus(function(data){
          $rootScope.isLoggedIn = data.data.login;
          $rootScope.status = data.data.status;
          $rootScope.avatar = data.data.avatar;

          if(!$rootScope.isLoggedIn){
            $location.path('/index/login');
          } else {
            $location.path('/index/home');
          }

        });

        getQR(function(data){
          $scope.qrcode = data.data;
        });

      }, 3000, 0, true);
    }

    $interval(function(){

    }, 3000, 0, true);

    $interval(function(){
      console.log($rootScope);

    }, 3000, 0, true);
  }]
);
