'use strict';


angular.module('bilgisayfam.controllers', []).
  controller('ContentController', ["$scope", "Entry", function($scope, Entry) {
        $scope.entry = bilgisayfam.entry;
        // TODO: Loading spinner is not working. Why not?
        $scope.loading = "";
        if(bilgisayfam.entry){
            $scope.header_class = "entry-header";
        } else {
            $scope.header_class = "noentry-header";
        }
        $scope.submit = function() {
            if(!this.keyword){
                return;
            }
            $scope.loading = "loading"
            $scope.error = "";
            var keyword = this.keyword;
            $scope.entry = Entry.get({keyword: this.keyword}, function(){
                $scope.loading = "";
            },
            function(response){
                $scope.loading = "";
                $scope.error = keyword + " kelimesi bulunamadı.";
            });
            $scope.header_class = "entry-header";
            this.keyword = ""
        };
  }]);
