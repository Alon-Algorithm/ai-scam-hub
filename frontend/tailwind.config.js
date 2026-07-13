/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#25DEEB',
          dark: '#12B8C5',
          light: '#E6FBFD',
        },
        background: '#F8FAFC',
        surface: '#FFFFFF',
        text: {
          DEFAULT: '#0F172A',
          secondary: '#64748B',
        },
        border: '#E2E8F0',
        success: '#22C55E',
        error: '#EF4444',
        warning: '#F59E0B',
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        'custom-sm': '0 1px 2px rgba(15, 23, 42, 0.05)',
        'custom-md': '0 4px 6px rgba(15, 23, 42, 0.07)',
        'custom-lg': '0 10px 15px rgba(15, 23, 42, 0.1)',
      },
    },
  },
  plugins: [],
}
