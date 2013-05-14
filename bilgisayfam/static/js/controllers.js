'use strict';


angular.module('bilgisayfam.controllers', []).
  controller('ContentController', ["$scope", "Entry", "$location", function($scope, Entry, $location) {
        $scope.submit = function() {
            $scope.entry = null;
            if(!this.keyword){
                return;
            }
            $location.search({search: this.keyword});
            $('#header').removeClass("noentry-header").addClass("entry-header");
            $("#seo-content").hide();
            $scope.loading = "loading";
            $scope.error = "";
            var keyword = this.keyword;
            var search_input = document.getElementById("search-input");
            var search_button = $("#search-button");
            $scope.entry = Entry.get({keyword: this.keyword}, function(){
                    search_button.button("reset");
                    search_input.blur();
                },
                function(response){
                    search_button.button("reset");
                    search_input.blur();
                    $scope.error = keyword + " kelimesi bulunamadı.";
            });
            search_input.placeholder = this.keyword;
            search_button.button("loading");
            this.keyword = ""
        };
  }]);
