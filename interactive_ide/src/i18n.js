import {createI18n} from "vue-i18n";
import messages from '../src/assets/locales/fr.json'


const i18n = createI18n({
  locale: 'fr',
  fallbackLocale: 'fr',
  messages: {
    'fr': messages
  }
})

export default i18n