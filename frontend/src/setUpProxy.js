// const { createProxyMiddleware } = require('http-proxy-middleware');
//
// module.exports = function(app) {
//
//     app.use(
//         '/aa',
//         createProxyMiddleware({
//             target: '/',
//             changeOrigin: true,
//         })
//
//     );
//     app.use(
//         '/spring',
//         createProxyMiddleware({
//             target: 'http://localhost:8080',
//             changeOrigin: true,
//         })
//     );
//
//     app.use(
//         '/django',
//         createProxyMiddleware({
//             target: 'http://localhost:8321',
//             changeOrigin: true,
//         })
//     );
// };
