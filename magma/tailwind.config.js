/** @type {import('tailwindcss').Config} */
export default {
  content: [
    '.src/components/**/*.{vue,js,ts,jsx,tsx}',
    '.src/views/**/*.{vue,js,ts,jsx,tsx}',
    'src/views/*.vue',
    'src/components/**/*.vue',
    '.src/App.vue'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui')
  ],
  daisyui: {
    themes: ["light", "dark"]
  }
}

