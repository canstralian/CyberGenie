module.exports = (on, config) => {
  // Add custom plugins or modify existing ones here
  // For example, you can add a plugin to handle file uploads
  on('file:preprocessor', (file) => {
    // Custom file preprocessor logic
    return file;
  });

  // You can also modify the Cypress configuration
  config.defaultCommandTimeout = 10000;
  config.pageLoadTimeout = 60000;

  // Return the updated configuration
  return config;
};
