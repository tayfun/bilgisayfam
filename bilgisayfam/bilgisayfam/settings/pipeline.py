PIPELINE_CSS = {
    'maincss': {
        'source_filenames': (
            'css/*.css',
        ),
        'output_filename': 'css/main.css',
    },
}

PIPELINE_JS = {
    'mainjs': {
        'source_filenames': (
            'js/*.js',
        ),
        'output_filename': 'js/main.js',
    }
}

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
MANIFESTO_EXCLUDED_MANIFESTS = (
        'pipeline.manifest.PipelineManifest',
)
