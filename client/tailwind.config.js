module.exports = {
  mode: 'jit',
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    backgroundColor: theme => ({
      ...theme('colors'),
      'primary': '#01000e',
      'secondary': '#0e0240',
      'danger': '#e3342f',
     }),
    extend: {
      fontFamily: {
        body: ['Dosis']
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
