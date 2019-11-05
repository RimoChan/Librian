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
                    'style-loader', 
                    {loader: 'css-loader', options: {url: false}}, 
                    'sass-loader',
                ]
            }, 
        ],
    },
    mode: 'development',
};