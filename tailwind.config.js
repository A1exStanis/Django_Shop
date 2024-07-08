/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./games/**/*.{html,js}", "./user/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}