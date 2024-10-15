/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: ['selector'],
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
      primary: {
        100: 'var(--primary-100)',
        200: 'var(--primary-200)',
        300: 'var(--primary-300)'
      },
      white: {
        100: '#ffffff',
        200: '#fbfbfb'
      },
      error: '#FF5B49',
      warning: '#FAFA00',
      success: '#00AA00',
      idle: '#AAAAAA'
    },
    extend: {}
  },
  plugins: []
}
