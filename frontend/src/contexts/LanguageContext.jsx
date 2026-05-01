import { createContext, useContext, useState, useEffect } from 'react'

const LanguageContext = createContext()

export function useLanguage() {
    return useContext(LanguageContext)
}

export const LANGUAGES = [
    { code: 'en', name: 'English', native: 'English' },
    { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
    { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
    { code: 'te', name: 'Telugu', native: 'తెలుగు' },
    { code: 'ta', name: 'Tamil', native: 'தமிழ்' }
]

const translations = {
    'English': {
        diagnosis_status: 'Diagnosis Status',
        detected_pathogen: 'Detected Pathogen',
        severity: 'Severity',
        impact: 'Impact',
        recommended_action: 'Recommended Action',
        ai_insights: 'AI Agronomist Insights',
        field_notes: 'Field Notes',
        heatmap_analysis: 'Heatmap Analysis',
        confidence: 'Confidence',
        high: 'High',
        moderate: 'Moderate',
        low: 'Low',
        report_incorrect: 'Report Incorrect Diagnosis',
        back_to_history: 'Back to History',
        unknown_disease: 'Unknown Disease',
        healthy_msg: '🎉 Plant is healthy! No action needed.',
        analyzed_image: 'Analyzed Image'
    },
    'Hindi': {
        diagnosis_status: 'निदान स्थिति',
        detected_pathogen: 'पता चला रोगज़नक़',
        severity: 'गंभीरता',
        impact: 'प्रभाव',
        recommended_action: 'अनुशंसित कार्रवाई',
        ai_insights: 'एआई कृषि विज्ञानी अंतर्दृष्टि',
        field_notes: 'फील्ड नोट्स',
        heatmap_analysis: 'हीटमैप विश्लेषण',
        confidence: 'विश्वास',
        high: 'उच्च',
        moderate: 'मध्यम',
        low: 'कम',
        report_incorrect: 'गलत निदान की रिपोर्ट करें',
        back_to_history: 'इतिहास पर वापस जाएं',
        unknown_disease: 'अज्ञात बीमारी',
        healthy_msg: '🎉 पौधा स्वस्थ है! किसी कार्रवाई की आवश्यकता नहीं है।',
        analyzed_image: 'विश्लेषण की गई छवि'
    },
    'Tamil': {
        diagnosis_status: 'கண்டறியும் நிலை',
        detected_pathogen: 'கண்டறியப்பட்ட நோய்',
        severity: 'தீவிரம்',
        impact: 'பாதிப்பு',
        recommended_action: 'பரிந்துரைக்கப்பட்ட நடவடிக்கை',
        ai_insights: 'AI வேளாண் நிபுணர் நுண்ணறிவு',
        field_notes: 'களக் குறிப்புகள்',
        heatmap_analysis: 'வெப்பநிலை வரைபட பகுப்பாய்வு',
        confidence: 'நம்பிக்கை',
        high: 'அதிகம்',
        moderate: 'மிதமானது',
        low: 'குறைவு',
        report_incorrect: 'தவறான நோயறிதலைப் புகாரளிக்கவும்',
        back_to_history: 'வரலாற்றுக்குத் திரும்பு',
        unknown_disease: 'அறியப்படாத நோய்',
        healthy_msg: '🎉 செடி ஆரோக்கியமாக உள்ளது! எந்த நடவடிக்கையும் தேவையில்லை.',
        analyzed_image: 'ஆய்வு செய்யப்பட்ட படம்'
    },
    'Telugu': {
        diagnosis_status: 'రోగ నిర్ధారణ స్థితి',
        detected_pathogen: 'గుర్తించబడిన వ్యాధి',
        severity: 'తీవ్రత',
        impact: 'ప్రభావం',
        recommended_action: 'సిఫార్సు చేయబడిన చర్య',
        ai_insights: 'AI అగ్రోనమిస్ట్ అంతర్దృష్టులు',
        field_notes: 'ఫీల్డ్ గమనికలు',
        heatmap_analysis: 'హీట్‌మ్యాప్ విશ્లేషణ',
        confidence: 'నమ్మకం',
        high: 'అధిక',
        moderate: 'మితమైన',
        low: 'తక్కువ',
        report_incorrect: 'తప్పు రోగ నిర్ధారణను నివేదించండి',
        back_to_history: 'తిరిగి చరిత్రకు',
        unknown_disease: 'తెలియని వ్యాధి',
        healthy_msg: '🎉 మొక్క ఆరోగ్యంగా ఉంది! ఎటువంటి చర్య అవసరం లేదు.',
        analyzed_image: 'విశ్లేషించబడిన చిత్రం'
    },
    'Kannada': {
        diagnosis_status: 'ರೋಗನಿರ್ಣಯದ ಸ್ಥಿತಿ',
        detected_pathogen: 'ಪತ್ತೆಯಾದ ರೋಗಕಾರಕ',
        severity: 'ತೀವ್ರತೆ',
        impact: 'ಪರಿಣಾಮ',
        recommended_action: 'ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮ',
        ai_insights: 'AI ಕೃಷಿ ತಜ್ಞರ ಒಳನೋಟಗಳು',
        field_notes: 'ಕ್ಷೇತ್ರದ ಟಿಪ್ಪಣಿಗಳು',
        heatmap_analysis: 'ಹೀಟ್‌ಮ್ಯಾಪ್ ವಿಶ್ಲೇಷಣೆ',
        confidence: 'ನಂಬಿಕೆ',
        high: 'ಹೆಚ್ಚು',
        moderate: 'ಸಾಧಾರಣ',
        low: 'ಕಡಿಮೆ',
        report_incorrect: 'ತಪ್ಪು ರೋಗನಿರ್ಣಯವನ್ನು ವરದಿ ಮಾಡಿ',
        back_to_history: 'ಹಿಂದಿನ ಇತಿಹಾಸಕ್ಕೆ',
        unknown_disease: 'ಅಪರಿಚಿತ ರೋಗ',
        healthy_msg: '🎉 ಸಸ್ಯವು ಆರೋಗ್ಯಕರವಾಗಿದೆ! ಯಾವುದೇ ಕ್ರಮದ ಅಗತ್ಯವಿಲ್ಲ.',
        analyzed_image: 'ವಿಶ್ಲೇಷಿಸಿದ ಚಿತ್ರ'
    }
}

export function LanguageProvider({ children }) {
    // Force English as default regardless of localStorage for this session fix
    const [language, setLanguage] = useState('English')

    const t = (key) => {
        return translations[language]?.[key] || translations['English'][key] || key
    }

    const value = {
        language,
        setLanguage,
        LANGUAGES,
        t
    }

    return (
        <LanguageContext.Provider value={value}>
            {children}
        </LanguageContext.Provider>
    )
}
