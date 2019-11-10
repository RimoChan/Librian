const path = require('path');

module.exports = {
    entry: './src/全局.coffee',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '束.js',
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
                    // {loader: 'css-loader', options: {url: false}}, 
                    {loader: 'resolve-url-loader', options: {}},
                    {loader: 'sass-loader', options: {sourceMap: true}}
                ]
            }, 
        ],
    },
    mode: 'development',
};