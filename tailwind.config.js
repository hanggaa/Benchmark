/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        mono: ['"Geist Mono"', '"IBM Plex Mono"', '"JetBrains Mono"', 'monospace'],
        display: ['"Inter"', 'Arial', 'sans-serif'],
      },
      colors: {
        substrate: {
          dark: '#0A0A0A',
          card: '#111113',
          elevated: '#161619',
          border: '#2A2A2E',
          borderStrong: '#3E3E44',
        },
        phosphor: {
          white: '#EAEAEA',
          dim: '#8E8E93',
          subtle: '#5A5A60',
        },
        hazard: {
          red: '#FF2A2A',
          redMuted: '#E61919',
          redBg: 'rgba(255, 42, 42, 0.12)',
        },
        telemetry: {
          green: '#4AF626',
        }
      },
      letterSpacing: {
        'tight-macro': '-0.05em',
        'wide-telemetry': '0.08em',
        'widest-telemetry': '0.14em',
      },
      lineHeight: {
        'macro': '0.88',
      },
      borderRadius: {
        'none': '0px',
      }
    },
  },
  plugins: [],
}
