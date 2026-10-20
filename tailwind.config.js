/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#61532E',
          hover: '#4D4224',
          dark: '#3D341B',
          deep: '#252010',
          rich: '#7A693A',
          light: '#938048',
          subtle: 'rgba(97, 83, 46, 0.08)'
        },
        secondary: {
          DEFAULT: '#CEBDA7',
          light: '#E8DFD5',
          dark: '#B5A087',
          border: '#CEBDA7',
          soft: 'rgba(206, 189, 167, 0.18)',
          tint: '#F6F3EE'
        },
        royal: {
          DEFAULT: '#61532E',
          deep: '#3D341B',
          rich: '#7A693A',
          light: '#938048',
          soft: '#F6F3EE',
          tint: '#EFEAE3'
        },
        gold: {
          DEFAULT: '#C5A059',
          light: '#EAD7AE',
          dark: '#9E7B35',
          accent: '#D4AF37',
          pale: '#F9F5EC'
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
          border: '#CEBDA7',
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
        'primary-sm': '0 2px 10px -1px rgba(97, 83, 46, 0.2)',
        'primary-md': '0 6px 20px -3px rgba(97, 83, 46, 0.35)',
        'primary-lg': '0 10px 28px -4px rgba(97, 83, 46, 0.45)',
        'secondary-sm': '0 2px 10px -1px rgba(206, 189, 167, 0.35)',
        'royal-sm': '0 2px 10px -1px rgba(97, 83, 46, 0.2)',
        'royal-md': '0 6px 20px -3px rgba(97, 83, 46, 0.35)',
        'champagne-sm': '0 2px 10px -1px rgba(197, 160, 89, 0.25)',
        'champagne-glow': '0 0 25px rgba(197, 160, 89, 0.3)',
      }
    },
  },
  plugins: [],
}
