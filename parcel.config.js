module.exports = {
  // Define the entry point for the application
  entry: './src/index.js',
  
  // Define the output configuration
  output: {
    file: 'dist/bundle.js',
    format: 'cjs',
    sourcemap: true,
  },
  
  // Define the plugins to be used
  plugins: [
    require('@parcel/transformer-babel')({
      presets: ['@babel/preset-env'],
    }),
    require('@parcel/transformer-sass')(),
    require('@parcel/transformer-image')(),
    require('@parcel/transformer-json')(),
  ],
  
  // Define the module resolution configuration
  resolve: {
    extensions: ['.js', '.jsx', '.json', '.scss', '.png', '.jpg', '.jpeg', '.gif'],
  },
  
  // Define the development server configuration
  devServer: {
    contentBase: './public',
    compress: true,
    port: 1234,
  },
};
