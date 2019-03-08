//https://stackoverflow.com/questions/41194264/mocha-react-navigator-is-not-defined
var jsdom = require('jsdom').jsdom;

global.document = jsdom('');
global.window = document.defaultView;
Object.keys(document.defaultView).forEach((property) => {
  if (typeof global[property] === 'undefined') {
    global[property] = document.defaultView[property];
  }
});

global.navigator = {
  userAgent: 'node.js'
};



// https://stackoverflow.com/questions/32236443/mocha-testing-failed-due-to-css-in-webpack
// Prevent mocha from interpreting CSS @import files
function noop() {
  return null;
}

require.extensions['.css'] = noop;
require.extensions['.png'] = noop;
