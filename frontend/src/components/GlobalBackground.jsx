import { useEffect } from 'react'
import { useTheme } from '../contexts/ThemeContext'
import loginBgLight from '../assets/login_bg_light.png'
import loginBgDark from '../assets/login_bg_dark.png'

export default function GlobalBackground() {
    const { theme } = useTheme()

    useEffect(() => {
        // Apply background to body
        document.body.style.backgroundImage = `url(${theme === 'dark' ? loginBgDark : loginBgLight})`
        document.body.style.backgroundSize = 'cover'
        document.body.style.backgroundPosition = 'center'
        document.body.style.backgroundRepeat = 'no-repeat'
        document.body.style.backgroundAttachment = 'fixed'
        document.body.style.transition = 'background-image 0.3s ease-in-out'

        // Cleanup on unmount (though this component likely stays mounted)
        return () => {
            document.body.style.backgroundImage = ''
            document.body.style.backgroundSize = ''
            document.body.style.backgroundPosition = ''
            document.body.style.backgroundRepeat = ''
            document.body.style.backgroundAttachment = ''
            document.body.style.transition = ''
        }
    }, [theme])

    return null
}
