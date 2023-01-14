/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
    fontFamily: {
      mono: ['Consolas']
    }
  },
  plugins: [
    require('flowbite/plugin'),
    require('flowbite-typography'),
  ],
}