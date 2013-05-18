'use strict';


angular.module('bilgisayfam.controllers', []).
    controller('ContentController', ["$scope", "Entry", "$location", function($scope, Entry, $location) {
        $scope.cache = $scope.entry = {};
        $scope.$watch(function() {return $location.search();}, function(newSearch, oldSearch) {
            if (typeof(newSearch) == "undefined") {
                // if there are no search parameters, do nothing.
                return;
            }
            var search_keyword = newSearch["search"];
            if (newSearch === oldSearch) {
                // this is the initialization run, just cache the result.
                $scope.cache[search_keyword] = bilgisayfam.seo_entry;
                return;
            }
            var cached_entry = $scope.cache[search_keyword];
            if (typeof(cached_entry) != "undefined") {
                $scope.entry = cached_entry;
                afterEntryFunction(search_keyword);
            }
        });
        var search_input = document.getElementById("search-input");
        var afterEntryFunction = function(keyword) {
            // Run after entry is loaded.
            $scope.keyword = "";
            search_input.blur();
            search_input.placeholder = keyword;
        };
        $scope.submit = function() {
            if(!this.keyword){
                return;
            }
            $location.search({search: this.keyword});
            $('#header').removeClass("noentry-header").addClass("entry-header");
            $("#seo-content").hide();
            // keyword is copied from /this/ so that a closure is formed for Entry.get
            var keyword = this.keyword;
            var search_button = $("#search-button");
            $scope.entry = Entry.get({keyword: keyword}, function(){
                    search_button.button("reset");
                    $scope.cache[keyword] = $scope.entry;
                },
                function(response){
                    search_button.button("reset");
                    $scope.entry.error = keyword + " kelimesi bulunamadı.";
            });
            search_button.button("loading");
            afterEntryFunction(keyword);
        };
  }]);
