from manifesto import Manifest


class StaticManifest(Manifest):
    def cache(self):
        return [
            "//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js",
            "//ajax.googleapis.com/ajax/libs/angularjs/1.0.6/angular.min.js",
            "//code.angularjs.org/1.0.6/angular-resource.min.js",
        ]

    def network(self):
        return [
            # '*',
        ]

    def fallback(self):
        return [
            # ('/', '/offline.html'),
        ]
