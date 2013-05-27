'use strict';


// Declare app level module which depends on filters, and services
angular.module('bilgisayfam', ['bilgisayfam.filters', 'bilgisayfam.services', 'bilgisayfam.directives', 'bilgisayfam.controllers'])
  .config(['$locationProvider', function($locationProvider){
    $locationProvider.html5Mode(true).hashPrefix("!");
  }]
);
