const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

let WEBPACK_ENV = process.env.WEBPACK_ENV || 'dev';
console.log(WEBPACK_ENV)
module.exports = {
    entry: './src/app.jsx',
    output: {
        path: path.resolve(__dirname, 'dist'),
        publicPath: WEBPACK_ENV === 'dev' ? '/dist/' : '//140.211.168.111/front-end-code/dist/',
        filename: 'js/app.js'
    },
    resolve: {
        // extensions: ['', '.js', '.jsx'],
        alias: {
            page: path.resolve(__dirname, 'src/page'),
            image: path.resolve(__dirname, 'src/image'),
            component: path.resolve(__dirname, 'src/component'),
            service: path.resolve(__dirname, 'src/service'),
            util: path.resolve(__dirname, 'src/util'),
        }
    },

    module: {
        rules: [{
            test: /\.jsx$/,
            exclude: /(node_modules)/,
            use: {
                loader: 'babel-loader',
                options: {
                    presets: ['env', 'react']
                }
            },
        },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: "style-loader",
                    use: "css-loader"
                })
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: ['css-loader', 'sass-loader']
                })
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: [{
                    loader: 'url-loader',
                    options: {
                        limit: 8192,
                        name: 'resource/[name].[ext]'
                    }
                }]
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2|otf)$/,
                use: [{
                    loader: 'url-loader',
                    options: {
                        limit: 80000,
                        name: 'resource/[name].[ext]'
                    }
                }]
            },

        ]
    },

    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index.html',
        }),
        new ExtractTextPlugin('css/[name].css'),
        new webpack.optimize.CommonsChunkPlugin({
            name: 'common',
            filename: 'js/base.js'
        })
    ],
    devServer: {
        contentBase: path.join(__dirname, "/dist/"),
        //compress: true,
        port: 8086,
        historyApiFallback: true,
        // historyApiFallback: {
        //             index: '/dist/index.html'
        // }
    }
};