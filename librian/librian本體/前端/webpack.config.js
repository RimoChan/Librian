const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: './src/全局.coffee',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: './dist/',
    },
    resolve: {
        alias: {
            '紙背景花紋.webp$': path.resolve(__dirname, '黑科技/synthetic_css/紙背景花紋.webp'),
            '紙背景花紋模糊.webp$': path.resolve(__dirname, '黑科技/synthetic_css/紙背景花紋模糊.webp'),
            './紙背景花紋模糊.webp$': path.resolve(__dirname, '黑科技/synthetic_css/紙背景花紋模糊.webp'),
        },
        modules: [
            path.resolve(__dirname, '黑科技/synthetic_css'),
            'node_modules',
        ],
        fallback: {
            fs: false,
            path: false,
            stream: false,
            buffer: false,
        },
    },
    module: {
        rules: [
            {
                test: /\.coffee$/,
                use: ['coffee-loader'],
            },
            {
                test: /\.sass$/,
                use: [
                    { loader: 'style-loader' },
                    { loader: 'css-loader' },
                    {
                        loader: 'sass-loader',
                        options: {
                            sassOptions: {
                                indentedSyntax: true,
                            },
                        },
                    },
                ],
            },
            {
                test: /\.(otf|png|jpg|webp|svg)$/,
                type: 'asset/resource',
                generator: {
                    filename: '[name][ext]',
                },
            },
        ],
    },
    plugins: [
        new webpack.ProgressPlugin(),
    ],
    mode: 'development',
};
