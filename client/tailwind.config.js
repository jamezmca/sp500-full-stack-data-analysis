module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    backgroundColor: theme => ({
      ...theme('colors'),
      'primary': '#01000e',
      'secondary': '#ffed4a',
      'danger': '#e3342f',
     }),
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
