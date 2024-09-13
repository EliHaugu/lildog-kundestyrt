/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    colors: {
      accent: {
        400: '#BDEEED',
        500: '#469796',
        600: '#005958',
        700: '#014848',
        800: '#00312F',
        900: '#001E1E'
      },
      white: {
        100: 'ffffff',
        200: 'fefefe'
      },
      error: {},
      warning: {},
      success: {}
    },
    extend: {}
  },
  plugins: []
}
