"use client";

import { useState } from "react";

export default function PatientPortal() {
  const [reportText, setReportText] = useState("");
  const [explanation, setExplanation] = useState("");
  const [readingLevel, setReadingLevel] = useState("intermediate");
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://luminamed-ai-production.up.railway.app";

  const handleExplain = async () => {
    if (!reportText.trim()) {
      alert("Please paste your radiology report first");
      return;
    }

    setLoading(true);
    setExplanation("");

    try {
      const response = await fetch(`${API_URL}/v1/explain`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          report_text: reportText,
          reading_level: readingLevel,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setExplanation(data.explanation || data.plain_language_summary || "Explanation generated successfully");
      } else {
        const error = await response.text();
        setExplanation(`Error: Unable to generate explanation. ${error}`);
      }
    } catch (error) {
      setExplanation(`Error: Could not connect to the API. Please try again later.`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-indigo-600 rounded-lg flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">LuminaMed Patient Portal</h1>
              <p className="text-sm text-gray-600">Understanding your radiology report, simplified</p>
            </div>
          </div>
        </div>
      </header>

      {/* Compliance Badges */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex flex-wrap gap-3 justify-center text-sm">
          <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full font-medium">
            ? HIPAA Compliant
          </span>
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full font-medium">
            ? Secure & Private
          </span>
          <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full font-medium">
            ? AI-Powered
          </span>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel - Input */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Your Radiology Report
            </h2>
            <p className="text-sm text-gray-600 mb-4">
              Paste your radiology report below to receive a clear explanation.
            </p>

            <label className="block text-sm font-medium text-gray-700 mb-2">
              Report Text
            </label>
            <textarea
              className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none font-mono text-sm"
              placeholder="IMPRESSION:&#10;&#10;Example: The diagnostic quality of this thoracolumbar spine and pelvis X-ray is severely limited by glare, overexposure, and external artifacts..."
              value={reportText}
              onChange={(e) => setReportText(e.target.value)}
            />

            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reading Level
              </label>
              <select
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                value={readingLevel}
                onChange={(e) => setReadingLevel(e.target.value)}
              >
                <option value="basic">Basic (5th-6th Grade)</option>
                <option value="intermediate">Intermediate (8th Grade)</option>
                <option value="advanced">Advanced (12th Grade)</option>
              </select>
            </div>

            <button
              onClick={handleExplain}
              disabled={loading || !reportText.trim()}
              className="mt-6 w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Explaining...</span>
                </>
              ) : (
                <>
                  <span>? Explain My Report</span>
                </>
              )}
            </button>
          </div>

          {/* Right Panel - Output */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Plain Language Explanation
            </h2>

            {!explanation && !loading && (
              <div className="h-full flex items-center justify-center">
                <div className="text-center text-gray-400">
                  <svg className="mx-auto h-16 w-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p className="text-sm">Your explanation will appear here</p>
                </div>
              </div>
            )}

            {loading && (
              <div className="h-full flex items-center justify-center">
                <div className="text-center">
                  <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
                  <p className="text-gray-600">AI is analyzing your report...</p>
                </div>
              </div>
            )}

            {explanation && (
              <div className="space-y-4">
                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                  <h3 className="font-semibold text-blue-900 mb-2">Key Takeaway</h3>
                  <p className="text-blue-800 text-sm leading-relaxed">
                    {explanation.split('\n')[0]}
                  </p>
                </div>

                <div className="prose prose-sm max-w-none">
                  <h3 className="text-lg font-semibold text-gray-900">Detailed Explanation</h3>
                  <div className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                    {explanation}
                  </div>
                </div>

                <div className="mt-6 pt-6 border-t border-gray-200">
                  <h4 className="text-sm font-semibold text-gray-900 mb-3">Medical Terms Glossary</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div className="p-3 bg-gray-50 rounded">
                      <span className="font-semibold text-gray-900">Consolidation:</span>
                      <p className="text-gray-600 text-xs mt-1">An area where lung tissue is filled with fluid</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded">
                      <span className="font-semibold text-gray-900">Infiltrate:</span>
                      <p className="text-gray-600 text-xs mt-1">Abnormal substance in the lung tissue</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded">
                      <span className="font-semibold text-gray-900">Pleural Effusion:</span>
                      <p className="text-gray-600 text-xs mt-1">Fluid around the lung</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded">
                      <span className="font-semibold text-gray-900">Cardiomegaly:</span>
                      <p className="text-gray-600 text-xs mt-1">Enlarged heart</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded">
                      <span className="font-semibold text-gray-900">Atelectasis:</span>
                      <p className="text-gray-600 text-xs mt-1">Collapsed or partially collapsed lung</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded">
                      <span className="font-semibold text-gray-900">Opacity:</span>
                      <p className="text-gray-600 text-xs mt-1">Area that appears white/cloudy on X-ray</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
          <details className="group">
            <summary className="cursor-pointer list-none flex items-center justify-between font-semibold text-gray-900">
              <span className="flex items-center">
                <span className="text-2xl mr-2">??</span>
                How to Use
              </span>
              <span className="transition group-open:rotate-180">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </span>
            </summary>
            <div className="mt-4 text-gray-700 space-y-3 text-sm">
              <p><strong>1. Upload your report:</strong> Copy and paste the radiology report text from your patient portal or email.</p>
              <p><strong>2. Select reading level:</strong> Choose how technical you want the explanation to be.</p>
              <p><strong>3. Get your explanation:</strong> Our AI will break down the medical jargon into clear, understandable language.</p>
              <p><strong>4. Review the glossary:</strong> Learn what common medical terms mean in simple language.</p>
              <p className="pt-3 border-t border-gray-200 text-xs text-gray-500">
                <strong>Important:</strong> This tool is for educational purposes only. Always discuss your results with your healthcare provider.
              </p>
            </div>
          </details>
        </div>

        {/* Disclaimer */}
        <div className="mt-6 text-center">
          <p className="text-xs text-gray-500">
            ?? <strong>Disclaimer:</strong> This tool is for research and educational purposes only. Not for clinical diagnosis.
          </p>
        </div>
      </main>
    </div>
  );
}
