/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cinema-black': '#141414',
        'cinema-red': '#E50914',
        'cinema-gray': '#2F2F2F',
      },
    },
  },
  plugins: [],
}
