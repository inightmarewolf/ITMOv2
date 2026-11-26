import { createTheme } from '@mui/material/styles';

/** Единая тема Mini Shop: цвета, типографика, отступы и видимый индикатор фокуса. */
export const appTheme = createTheme({
  palette: {
    primary: {
      main: '#1565c0',
      dark: '#0d47a1',
    },
    secondary: {
      main: '#00838f',
    },
    background: {
      default: '#f4f6f9',
      paper: '#ffffff',
    },
    text: {
      primary: '#1e293b',
      secondary: '#64748b',
    },
  },
  typography: {
    fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
    h5: {
      fontWeight: 700,
    },
    h6: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 10,
  },
  spacing: 8,
  components: {
    MuiButtonBase: {
      styleOverrides: {
        root: {
          '&:focus-visible': {
            outline: '3px solid #1565c0',
            outlineOffset: '2px',
          },
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderWidth: '2px',
          },
        },
      },
    },
  },
});
