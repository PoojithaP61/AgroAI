import { useState, useEffect } from 'react'
import { Upload, Plus, RefreshCw, CheckCircle, AlertCircle, Shield } from 'lucide-react'
import api from '../services/api'
import toast from 'react-hot-toast'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

import DiseaseChart from '../components/DiseaseChart'

export default function AdminDashboard() {
    const { user } = useAuth()
    const navigate = useNavigate()

    const [diseaseName, setDiseaseName] = useState('')
    const [files, setFiles] = useState([])
    const [training, setTraining] = useState(false)
    const [stats, setStats] = useState(null)
    const [diseaseStats, setDiseaseStats] = useState([])
    const [statsLoading, setStatsLoading] = useState(true)

    useEffect(() => {
        // Redirect if not admin
        if (user && !user.is_admin) {
            toast.error("Access denied. Admin only.")
            navigate('/dashboard')
            return
        }
        fetchStats()
    }, [user, navigate])

    const fetchStats = async () => {
        try {
            const [statsRes, diseasesRes] = await Promise.all([
                api.get('/admin/stats'),
                api.get('/admin/diseases')
            ])
            setStats(statsRes.data)

            // Format for chart: { name: 'Tomato Blight', count: 15 }
            const chartData = diseasesRes.data.map(d => ({
                name: d.disease_name,
                count: d.total_detections
            }))
            setDiseaseStats(chartData)

        } catch (error) {
            console.error("Failed to fetch stats", error)
        } finally {
            setStatsLoading(false)
        }
    }

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFiles(Array.from(e.target.files))
        }
    }

    const handleTrain = async (e) => {
        e.preventDefault()
        if (!diseaseName || files.length === 0) {
            toast.error("Please provide a disease name and at least one image")
            return
        }

        if (files.length < 5) {
            toast("For best results, upload at least 5 images", { icon: 'ℹ️' })
        }

        setTraining(true)
        const formData = new FormData()
        formData.append('disease_name', diseaseName)
        files.forEach(file => {
            formData.append('files', file)
        })

        try {
            const response = await api.post('/admin/train', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })
            toast.success(response.data.message)
            setDiseaseName('')
            setFiles([])
            fetchStats() // Refresh stats
        } catch (error) {
            console.error(error)
            const msg = error.response?.data?.detail || "Training failed"
            toast.error(msg)
        } finally {
            setTraining(false)
        }
    }

    if (statsLoading) {
        return <div className="flex justify-center p-12"><RefreshCw className="animate-spin text-primary-500" /></div>
    }

    return (
        <div className="max-w-6xl mx-auto space-y-8">
            <div className="flex items-center gap-4 border-b border-gray-100 dark:border-gray-800 pb-6">
                <div className="p-3 bg-indigo-100 dark:bg-indigo-900/30 rounded-2xl text-indigo-600 dark:text-indigo-400">
                    <Shield className="w-8 h-8" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Admin Console</h1>
                    <p className="text-gray-600 dark:text-gray-400">System metrics and continual learning interface</p>
                </div>
            </div>

            <div className="grid lg:grid-cols-3 gap-8">
                {/* Training Card */}
                <div className="lg:col-span-2">
                    <div className="bg-white dark:bg-dark-surface rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800 p-8">
                        <div className="mb-8">
                            <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                                <Plus className="w-6 h-6 text-primary-500" />
                                Train New Disease
                            </h2>
                            <p className="text-gray-500 dark:text-gray-400 mt-1">
                                Add a new disease class to the model dynamically. No downtime required.
                            </p>
                        </div>

                        <form onSubmit={handleTrain} className="space-y-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Disease Name
                                </label>
                                <input
                                    type="text"
                                    value={diseaseName}
                                    onChange={(e) => setDiseaseName(e.target.value)}
                                    placeholder="e.g. Tomato Early Blight"
                                    className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-primary-100 outline-none transition-all"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Training Images
                                </label>
                                <div className="border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-2xl p-8 text-center bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                                    <input
                                        type="file"
                                        multiple
                                        onChange={handleFileChange}
                                        accept="image/*"
                                        className="hidden"
                                        id="images-upload"
                                    />
                                    <label htmlFor="images-upload" className="cursor-pointer block">
                                        <Upload className="w-10 h-10 text-gray-400 mx-auto mb-3" />
                                        <p className="text-gray-900 dark:text-white font-medium mb-1">
                                            {files.length > 0 ? `${files.length} images selected` : 'Click to upload images'}
                                        </p>
                                        <p className="text-xs text-gray-500">
                                            Recommended: 5-20 distinct images
                                        </p>
                                    </label>
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={training}
                                className={`w-full py-4 rounded-xl font-bold text-white shadow-lg transition-all ${training
                                    ? 'bg-gray-400 cursor-not-allowed'
                                    : 'bg-primary-600 hover:bg-primary-700 hover:-translate-y-1 hover:shadow-xl'
                                    }`}
                            >
                                {training ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <RefreshCw className="w-5 h-5 animate-spin" />
                                        Training Model...
                                    </span>
                                ) : (
                                    'Start Training'
                                )}
                            </button>
                        </form>
                    </div>
                </div>

                {/* Stats Card */}
                <div className="space-y-6">
                    <div className="bg-white dark:bg-dark-surface rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800 p-6">
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-6">System Health</h3>

                        <div className="space-y-4">
                            <div className="flex items-center justify-between p-4 rounded-xl bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300">
                                <div className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5" />
                                    <span className="font-medium">Model Status</span>
                                </div>
                                <span className="font-bold">Active</span>
                            </div>

                            {stats && (
                                <>
                                    <div className="flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50">
                                        <span className="text-gray-600 dark:text-gray-400">Total Users</span>
                                        <span className="text-xl font-bold text-gray-900 dark:text-white">{stats.total_users}</span>
                                    </div>
                                    <div className="flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50">
                                        <span className="text-gray-600 dark:text-gray-400">Predictions</span>
                                        <span className="text-xl font-bold text-gray-900 dark:text-white">{stats.total_predictions}</span>
                                    </div>
                                    <div className="flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-800/50">
                                        <span className="text-gray-600 dark:text-gray-400">Disease Classes</span>
                                        <span className="text-xl font-bold text-primary-600 dark:text-primary-400">{stats.unique_diseases_detected}</span>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>

                    <div className="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-6 border border-blue-100 dark:border-blue-800">
                        <div className="flex items-start gap-3">
                            <AlertCircle className="w-6 h-6 text-blue-600 dark:text-blue-400 mt-0.5" />
                            <div>
                                <h4 className="font-bold text-blue-900 dark:text-blue-300 mb-1">Tip</h4>
                                <p className="text-sm text-blue-800 dark:text-blue-200/80">
                                    When adding a new disease, try to include images with different lighting and angles to improve robustness.
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Analytics Chart */}
                    <div>
                        <DiseaseChart data={diseaseStats} />
                    </div>
                </div>
            </div>
        </div>
    )
}
