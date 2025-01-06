/** @type {import('tailwindcss').Config} */
export default {
  content: ['./calyvim/static/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#7D52E9'
      }
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false
  },
}
