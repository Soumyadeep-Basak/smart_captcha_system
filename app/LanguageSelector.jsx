"use client"
import React, { useState } from 'react'

export default function LanguageSelector() {
  const [selectedLanguage, setSelectedLanguage] = useState('English')

  const languages = [
    "English",
    "हिंदी",
    "বাংলা",
    "ಕನ್ನಡ",
    "ગુજરાતી",
    "മലയാളം",
    "मराठी",
    "ଓଡ଼ିଆ",
    "ਪੰਜਾਬੀ",
    "தமிழ்",
    "తెలుగు",
    "اردو",
  ]

  const handleLanguageChange = (e) => {
    setSelectedLanguage(e.target.value)
  }

  return (
    <div className="relative inline-block text-left">
      <select
        value={selectedLanguage}
        onChange={handleLanguageChange}
        className="block appearance-none w-full bg-transparent border-0 text-white px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline"
      >
        {languages.map((language) => (
          <option className='text-black' key={language} value={language}>
            {language}
          </option>
        ))}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
        <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
        </svg>
      </div>
    </div>
  )
}