import { useEffect, useState } from 'react'
import { Check, Loader2 } from 'lucide-react'

const steps = [
    { id: 1, label: 'Uploading image...' },
    { id: 2, label: 'Analyzing leaf patterns...' },
    { id: 3, label: 'Identifying potential diseases...' },
    { id: 4, label: 'Generating AI advisory...' }
]

export default function LoadingSteps({ currentStep }) {
    // We use currentStep (1-4) to control the visual state

    return (
        <div className="w-full max-w-md mx-auto p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-emerald-100 dark:border-gray-700 transition-colors duration-300">
            <h3 className="text-lg font-semibold text-center text-gray-800 dark:text-gray-100 mb-6">Processing Analysis</h3>

            <div className="space-y-4">
                {steps.map((step) => {
                    const isCompleted = currentStep > step.id
                    const isCurrent = currentStep === step.id
                    const isPending = currentStep < step.id

                    return (
                        <div key={step.id} className="flex items-center gap-4">
                            <div
                                className={`
                  flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full border-2 transition-all duration-300
                  ${isCompleted ? 'bg-emerald-500 border-emerald-500 text-white' : ''}
                  ${isCurrent ? 'border-emerald-500 text-emerald-500 dark:text-emerald-400' : ''}
                  ${isPending ? 'border-gray-200 dark:border-gray-600 text-gray-300 dark:text-gray-500' : ''}
                `}
                            >
                                {isCompleted ? (
                                    <Check className="w-5 h-5" />
                                ) : isCurrent ? (
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                ) : (
                                    <span className="text-sm font-medium">{step.id}</span>
                                )}
                            </div>

                            <div className="flex-1">
                                <p
                                    className={`
                    text-sm font-medium transition-colors duration-300
                    ${isCompleted ? 'text-gray-900 dark:text-gray-200' : ''}
                    ${isCurrent ? 'text-emerald-700 dark:text-emerald-400 font-bold' : ''}
                    ${isPending ? 'text-gray-400 dark:text-gray-500' : ''}
                  `}
                                >
                                    {step.label}
                                </p>
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
