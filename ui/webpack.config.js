var path = require("path");
var webpack = require("webpack");

//var BowerWebpackPlugin = require("bower-webpack-plugin");

var libs = [
    'angular',
    'angular-animate',
    'angular-aria',
    'angular-material',
    'angular-mocks',
    'angular-ui-router'
]

var plugins = [
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.optimize.CommonsChunkPlugin('common', 'common.js'),
]

module.exports = {
    context: path.resolve(__dirname, 'app'),
    entry: {
        libs:libs,
        bundle:['babel-polyfill', './app.js']
    },
    output: {
        path: __dirname + "/dist",
        filename: "[name].js"
    },
    module: {
        loaders: [
            { test: /\.js$/, loader: "babel!imports?angular", include: /app|test/},
            { test: /\.css$/, loader: "style!css" },
            { test: /\.tpl\.html$/, loader: "raw" }

        ]
    },
    plugins: plugins
};