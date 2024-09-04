/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    colors: {
      white: '#ffffff',
      accent: {
        400: '#BDEEED',
        500: '#469796',
        600: '#005958',
        700: '#014848',
        800: '#00312F',
        900: '#001E1E'
      },
      disabled: {
        500: '#B7B7B7',
        600: '#E0E0E0'
      },
      error: {
        500: '#E76C6C',
        600: '#C53030'
      }
    },
    extend: {}
  },
  plugins: []
}
