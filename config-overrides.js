const {
    override,
    babelInclude,
    addBabelPreset,
    addExternalBabelPlugin,
} = require('customize-cra');

module.exports = override(
    // babelInclude([
    //     path.resolve('src'),
    //     path.resolve('node_modules/react-native-animatable'),
    // ]),
    addBabelPreset("@babel/preset-react"),
    // addExternalBabelPlugin('@babel/plugin-proposal-class-properties'),
);