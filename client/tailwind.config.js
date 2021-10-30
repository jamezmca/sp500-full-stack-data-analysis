module.exports = {
  // mode: 'jit',
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    backgroundColor: theme => ({
      ...theme('colors'),
      'primary': '#07004a',
      'secondary': '#0e0230',
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
