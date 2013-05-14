'use strict';


angular.module('bilgisayfam.controllers', []).
  controller('ContentController', ["$scope", "Entry", "$location", function($scope, Entry, $location) {
        $scope.entry = null;
        $scope.submit = function() {
            if(!this.keyword){
                return;
            }
            $location.search({search: this.keyword});
            $('#header').removeClass("noentry-header").addClass("entry-header");
            $("#seo-content").hide();
            $scope.loading = "loading";
            $scope.error = "";
            var keyword = this.keyword;
            $scope.entry = Entry.get({keyword: this.keyword}, function(){
                $scope.loading = "";
            },
            function(response){
                $scope.loading = "";
                $scope.error = keyword + " kelimesi bulunamadı.";
            });
            this.keyword = ""
        };
  }]);
