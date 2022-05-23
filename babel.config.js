module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  webpack: (config) => {
    // this will override the experiments
    config.experiments = { topLevelAwait: true };
    // this will just update topLevelAwait property of config.experiments
    config.experiments.topLevelAwait = true 
    return config;
  },
}
