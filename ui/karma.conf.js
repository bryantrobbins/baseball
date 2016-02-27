module.exports = function(config){
  config.set({

    basePath : './',

    files : [
        "app/**/*.js",
        "test/unit/**/*.js"
    ],
    preprocessors: {
        "app/**/*.js": ["babel"],
        "test/unit/**/*.js": ["babel"]
    }

    "babelPreprocessor":{

    }

    autoWatch : true,

    frameworks: ['jasmine'],

    browsers : ['Chrome'],

    plugins : [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine',
            'karma-junit-reporter'
            ],

    junitReporter : {
      outputFile: 'test_out/unit.xml',
      suite: 'unit'
    }

  });
};
