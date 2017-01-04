angular.module('servData', []).factory(
  'getQR', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(onSuccess){
      var query = $rootScope.host + 'api/qr';
      $http.get(query, { cache: false }).then(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'startBot', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(onSuccess){
      var query = $rootScope.host + 'api/start';
      $http.get(query, { cache: false }).then(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getLoginStatus', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(onSuccess){
      var query = $rootScope.host + 'api/loginstatus';
      $http.get(query, { cache: false }).then(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getBasicInfo', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(onSuccess){
      var query = $rootScope.host + 'api/init_info';
      $http.get(query, { cache: false }).then(function(data){
        onSuccess(data);
      });
    }
  }]
).factory(
  'getContacts', ['$http', '$rootScope',
  function($http, $rootScope) {
    return function(onSuccess){
      var query = $rootScope.host + 'api/contacts';
      $http.get(query, { cache: false }).then(function(data){
        onSuccess(data);
      });
    }
  }]
);
