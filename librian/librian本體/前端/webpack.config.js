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
                    { loader: 'style-loader' },
                    { loader: 'css-loader' },
                    { loader: 'resolve-url-loader' },
                    { loader: 'sass-loader', options: { sourceMap: true } }
                ]
            }, {
                test: /\.(otf|png|jpg|webp|svg)$/,
                use: [
                    {
                        loader: 'file-loader', options: {
                            name: () => '[name].[ext]',
                        }
                    },
                ]
            },
        ],
    },
    plugins: [
        new WebpackBar()
    ],
    node: { fs: 'empty' },
    mode: 'development',
    // mode: 'production',
};