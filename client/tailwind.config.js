/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
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
        100: '#ffffff',
        200: '#fefefe'
      },
      error: {},
      warning: {},
      success: {}
    },
    extend: {}
  },
  plugins: []
}
