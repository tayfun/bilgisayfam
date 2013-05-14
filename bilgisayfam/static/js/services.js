'use strict';


angular.module('bilgisayfam.services', ["ngResource"]).
  factory("Entry", ["$resource", function($resource){
    return $resource("/?search=:keyword");
}]);
