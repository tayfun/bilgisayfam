'use strict';


angular.module('bilgisayfam.controllers', []).
    controller('ContentController', ["$scope", "Entry", "$location", function($scope, Entry, $location) {
        try {
            // Check to see if localStorage is available.
            localStorage.setItem("bilgisayfam", "v0.5");
            $scope.cache = localStorage;
        } catch(e) {
            // Fallback on using in memory cache.
            $scope.cache = {}
        }
        var search_input = document.getElementById("search-input");
        var search_button = $("#search-button");
        $scope.entry = {};
        $scope.$watch(function() {return $location.search();}, function(newSearch, oldSearch) {
            if (!newSearch || !newSearch["search"]) {
                // if there are no search parameters, do nothing.
                return;
            }
            var keyword = newSearch["search"];
            if (newSearch === oldSearch) {
                // this is the initialization run, just cache the result.
                $scope.cache[keyword] = JSON.stringify(bilgisayfam.seo_entry);
                return;
            }
            var json_cached_entry = $scope.cache[keyword];
            search_button.button("loading");
            if (json_cached_entry) {
                $scope.entry = JSON.parse(json_cached_entry);
                search_button.button("reset");
            } else {
                $scope.entry = Entry.get({keyword: keyword}, function(){
                        search_button.button("reset");
                        $scope.cache[keyword] = JSON.stringify($scope.entry);
                    },
                    function(response){
                        search_button.button("reset");
                        if (response.status == 404) {
                            $scope.entry.error = keyword + " kelimesi bulunamadı.";
                            $scope.cache[keyword] = JSON.stringify($scope.entry);
                        } else if (response.status == 0) {
                            $scope.entry.error = "Lütfen " +
                                "internet bağlantınızı kontrol ediniz.";
                        }
                });
            }
            $scope.keyword = "";
            search_input.blur();
        });
        $scope.submit = function() {
            if(!this.keyword){
                return;
            }
            $location.search({search: this.keyword});
            $('#header').removeClass("noentry-header").addClass("entry-header");
            $("#seo-content").hide();
        };
  }]);
