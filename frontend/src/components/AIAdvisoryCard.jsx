import ReactMarkdown from 'react-markdown'
import { useLanguage } from '../contexts/LanguageContext'

export default function AIAdvisoryCard({ advisory, loading }) {
    const { t } = useLanguage()
    if (loading) {
        return (
            <div className="bg-white dark:bg-dark-surface rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 p-6 animate-pulse">
                <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full mb-2"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
            </div>
        )
    }

    if (!advisory) return null

    return (
        <div className="relative overflow-hidden bg-gradient-to-br from-indigo-50 to-purple-50 dark:bg-none dark:bg-gray-800 rounded-xl shadow-lg border border-indigo-100 dark:border-gray-700 p-6">
            {/* Decorative background elements */}
            <div className="absolute top-0 right-0 -mr-10 -mt-10 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl"></div>
            <div className="absolute bottom-0 left-0 -ml-10 -mb-10 w-32 h-32 bg-purple-500/10 rounded-full blur-2xl"></div>

            <div className="relative z-10">
                <div className="flex items-center gap-3 mb-4">

                    <h3 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400">
                        AI Agronomist Insights
                    </h3>
                </div>

                <div className="prose prose-indigo dark:prose-invert max-w-none prose-headings:font-bold prose-headings:text-indigo-900 dark:prose-headings:text-white prose-p:text-indigo-900/80 dark:prose-p:text-gray-100 prose-li:text-indigo-900/80 dark:prose-li:text-gray-100 prose-strong:text-indigo-900 dark:prose-strong:text-white">
                    <ReactMarkdown>
                        {advisory}
                    </ReactMarkdown>
                </div>
            </div>
        </div>
    )
}
