import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'
import '@fortawesome/fontawesome-free/css/all.css' // Ensure you are using css-loader

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    options: {
      customProperties: true
    },
    themes: {
      light: {
        primary: '#1982b1',
        // secondary: '#b0bec5',
        // accent: '#8c9eff',
        // error: '#b71c1c',
        bg: '#064663',
        background: '#f4f4f4',
        // header: '#3739FF',
        // footer: '#101721'
      },
      dark: {
        primary: '#1982b1',
        background: '#333',
        // header: '#3739FF',
        // footer: '#101721'
      }
    },
    dark: false
  },
  icons: {
    iconfont: 'fa'
  }
})
