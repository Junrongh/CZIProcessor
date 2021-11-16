const path = require('path')
const HtmlWebPackPlugin = require('html-webpack-plugin')

const config = {
    entry: {
        bundle: './src/index.ts'
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].js',
        publicPath: 'dist'
    },

    devServer: {
        contentBase: __dirname,
        compress: true,
        port: process.env.NODE_PORT || 9000
    },

    resolve: {
        extensions: ['.ts', '.js']
    },

    module: {
        rules: [
            {
                test: /\.ts$/,
                loader: 'awesome-typescript-loader'
            },
            // {
            //     test: /\.ts$/,
            //     use: ['ts-loader']
            // },
            {
                test: /\.(glsl|vs|fs)$/,
                loader: "shader-loader"
            }
        ]
    },
    plugins: [
        new HtmlWebPackPlugin({
            template: './src/index.html',
            chunks: ['bundle'],
            filename: 'index.html'
        })
    ]
};

config['devtool'] = 'source-map'

module.exports = config;

