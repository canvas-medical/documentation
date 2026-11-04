/* eslint-disable import/no-extraneous-dependencies */
const { merge: Merge } = require('webpack-merge');
const CommonConfig = require('./webpack.common.js');
const path = require('path');
const webpack = require('webpack');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const fs = require('fs');
const ImageMinimizerPlugin = require('image-minimizer-webpack-plugin');
const TerserPlugin = require("terser-webpack-plugin");

// oxipng compiled to WASM: lossless PNG optimization with no native binary,
// so the build runs the same on Apple Silicon, Intel, and Amplify's Linux.
let oxipngReady;
const oxipngMinify = async (original) => {
  if (path.extname(original.filename).toLowerCase() !== '.png') {
    return null;
  }

  const { default: optimise, init } = await import('@jsquash/oxipng/optimise.js');
  oxipngReady ??= init(WebAssembly.compile(fs.readFileSync(
    require.resolve('@jsquash/oxipng/codec/pkg/squoosh_oxipng_bg.wasm'),
  )));
  await oxipngReady;

  const input = original.data;
  const output = Buffer.from(await optimise(
    input.buffer.slice(input.byteOffset, input.byteOffset + input.length),
    { level: 2, interlace: false, optimiseAlpha: false },
  ));

  if (output.length >= input.length) {
    return null;
  }

  return {
    filename: original.filename,
    data: output,
    warnings: [...original.warnings],
    errors: [...original.errors],
    info: { ...original.info, minimized: true, minimizedBy: ['oxipng', ...(original.info?.minimizedBy ?? [])] },
  };
};

module.exports = Merge(CommonConfig, {
  output: {
    filename: '[name]-[hash].bundle.js',
    path: path.resolve('assets'),
    publicPath: '/assets/',
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          keep_fnames: true
        }
      }),
      new ImageMinimizerPlugin({
        test: /\.(png|svg)$/i,
        minimizer: [
          { implementation: oxipngMinify },
          { implementation: ImageMinimizerPlugin.svgoMinify },
        ],
      }),
    ]
  },
  plugins: [
    new CleanWebpackPlugin({ cleanOnceBeforeBuildPatterns: ['assets'], verbose: true }),
    new webpack.LoaderOptionsPlugin({
      minimize: true,
      debug: false,
    }),
  ],
});
