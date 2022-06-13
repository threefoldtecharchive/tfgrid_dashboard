const { defineConfig } = require('@vue/cli-service')


module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  pluginOptions: 
   { Buffer: ['buffer', 'Buffer'] , process: "process/browser"}
  ,
  configureWebpack: {
    resolve: {
      fallback: {
        crypto: require.resolve("crypto-browserify"),
        path: require.resolve("path-browserify"),
        stream: require.resolve("stream-browserify"),
        buffer: require.resolve("buffer")
      },
    },},
})
