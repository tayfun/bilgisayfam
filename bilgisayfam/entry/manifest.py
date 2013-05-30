from django.conf import settings

from pipeline import manifest


class StaticManifest(manifest.PipelineManifest):
    def cache(self):
        if getattr(settings, "PIPELINE_ENABLED", None) or not settings.DEBUG:
            for package in self.packages:
                if self.pcs:
                    filename = self.pcs.hashed_name(package.output_filename)
                else:
                    filename = package.output_filename
                self.package_files.append(filename)
                yield str(self.packager.individual_url(filename))

        extra_resources = [
            "//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js",
            "//ajax.googleapis.com/ajax/libs/angularjs/1.0.6/angular.min.js",
            "//code.angularjs.org/1.0.6/angular-resource.min.js",
            "/static/img/favicon.ico",
        ]
        for resource in extra_resources:
            yield resource

    def network(self):
        return [
            '*',
        ]

    def fallback(self):
        return [
            # ('/', '/offline.html'),
        ]
