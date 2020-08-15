const path = require('path');
const WebpackBar = require('webpackbar');

module.exports = {
    entry: './src/全局.coffee',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: './dist/',
    },
    module: {
        rules: [
            {
                test: /\.coffee$/,
                use: ['coffee-loader']
            }, {
                test: /\.sass$/,
                use: [
                    {loader: 'style-loader', options: {injectType: 'linkTag'}}, 
                    {loader: 'file-loader', options: {
                            name: function(file){return '[name].css'},
                        }
                    }, 
                    {loader: 'resolve-url-loader', options: {}},
                    {loader: 'sass-loader', options: {sourceMap: true}}
                ]
            }, 
        ],
    },
    plugins: [
        new WebpackBar()
    ],
    node: { fs: 'empty' },
    // mode: 'development',
    mode: 'production',
};