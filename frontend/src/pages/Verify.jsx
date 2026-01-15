import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { ShieldCheck } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../services/api'

export default function Verify() {
    const [code, setCode] = useState('')
    const [loading, setLoading] = useState(false)
    const location = useLocation()
    const navigate = useNavigate()

    // Get email from state or allow user to enter (though state is preferred)
    const [email, setEmail] = useState(location.state?.email || '')
    const verification_token = location.state?.verification_token

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)

        try {
            await api.post('/auth/verify', { email, code, verification_token })
            toast.success('Account verified successfully! Please login.')
            navigate('/login')
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Verification failed')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 backdrop-blur-sm bg-opacity-95 dark:bg-opacity-95 transition-colors duration-300">
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                        <ShieldCheck className="w-8 h-8 text-primary-600" />
                    </div>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Verify Account</h1>
                    <p className="text-gray-600 dark:text-gray-300 mt-2">Enter the code sent to your email/phone</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {!location.state?.email && (
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
                                Email
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 transition-colors"
                                placeholder="Enter your email"
                            />
                        </div>
                    )}

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
                            Verification Code
                        </label>
                        <input
                            type="text"
                            value={code}
                            onChange={(e) => setCode(e.target.value)}
                            required
                            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-center text-2xl tracking-widest dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 transition-colors"
                            placeholder="123456"
                            maxLength={6}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        ) : (
                            'Verify Account'
                        )}
                    </button>
                </form>
            </div>
        </div>
    )
}
