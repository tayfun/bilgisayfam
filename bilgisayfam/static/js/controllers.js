'use strict';


angular.module('bilgisayfam.controllers', []).
  controller('ContentController', ["$scope", "Entry", function($scope, Entry) {
        $scope.entry = null;
        $scope.submit = function() {
            if(!this.keyword){
                return;
            }
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
