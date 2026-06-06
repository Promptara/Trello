/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: '#3EB8B8',
        'brand-dark': '#2AA0A0',
        'brand-light': '#E8F7F7',
        ink: '#17172E',
        muted: '#6B6B88',
        faint: '#B0AFBF',
        surface: '#F7F6F3',
        line: '#E5E4EF',
      },
      fontFamily: {
        sans: ["'Plus Jakarta Sans'", 'sans-serif'],
      },
    },
  },
  plugins: [],
};
