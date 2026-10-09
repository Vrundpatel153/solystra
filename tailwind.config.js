/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        royal: {
          DEFAULT: '#145C59',
          deep: '#0D3F3D',
          rich: '#1A6E6B',
          light: '#228B87',
          soft: '#F0F7F6',
          tint: '#E1EFEB'
        },
        champagne: {
          DEFAULT: '#C5A059',
          light: '#EAD7AE',
          dark: '#9E7B35',
          pale: '#F9F5EC'
        },
        ivory: {
          DEFAULT: '#FAF8F5',
          cream: '#F5F1EB',
          pure: '#FFFFFF',
          border: '#EAE4DC',
          line: '#DFD7CB'
        },
        onyx: {
          DEFAULT: '#231F20',
          soft: '#423B3D',
          muted: '#766D6F',
          subtle: '#A29A9C'
        }
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        cinzel: ['"Cinzel"', 'serif'],
        sans: ['"Montserrat"', '"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'royal-sm': '0 2px 10px -1px rgba(20, 92, 89, 0.15)',
        'royal-md': '0 6px 20px -3px rgba(20, 92, 89, 0.25)',
        'champagne-sm': '0 2px 10px -1px rgba(197, 160, 89, 0.25)',
        'champagne-glow': '0 0 25px rgba(197, 160, 89, 0.3)',
      }
    },
  },
  plugins: [],
}
