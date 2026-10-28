/** @type {import('tailwindcss').Config} */
module.exports = {
  // Python files too: the bento template tag builds grid/span classes in app_main/templatetags/bento.py
  content: [
    "./templates/**/*.html",
    "./app_main/templates/**/*.html",
    "./app_main/**/*.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
