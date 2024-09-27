'use client';

import React, { useState, useEffect } from 'react';

const Page = () => {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/predictions'); 
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setPredictions(data);
      } catch (error) {
        console.error('Error fetching predictions:', error);
      }
    };

    fetchPredictions();
  }, []);

  return (
    <div className="overflow-x-auto p-4 mt-16">
      <h1 className="text-2xl font-bold mb-4">PREDICTIONS</h1>
      <table className="min-w-full bg-white border border-gray-300 mt-4">
        <thead>
          <tr className="bg-gray-200 text-black">
            <th className="border border-gray-300 px-8 py-2">IP Address</th>
            <th className="border border-gray-300 px-8 py-2">User Agent</th>
            <th className="border border-gray-300 px-8 py-2">Timestamp</th>
            <th className="border border-gray-300 px-2 py-2">Mouse Move Count</th>
            <th className="border border-gray-300 px-2 py-2">Key Press Count</th>
            <th className="border border-gray-300 px-2 py-2">Is Bot</th>
          </tr>
        </thead>
        <tbody>
          {predictions && predictions.length > 0 ? (
            predictions.map((prediction, index) => (
              <tr key={index} className="hover:bg-gray-100">
                <td className="border border-gray-300 px-4 py-2">{prediction.ip_address}</td>
                <td className="border border-gray-300 px-4 py-2">{prediction.user_agent}</td>
                <td className="border border-gray-300 px-4 py-2">{new Date(prediction.timestamp).toLocaleString()}</td>
                <td className="border border-gray-300 px-4 py-2">{prediction.mouseMoveCount}</td>
                <td className="border border-gray-300 px-4 py-2">{prediction.keyPressCount}</td>
                <td className="border border-gray-300 px-4 py-2">{prediction.prediction[0].bot ? 'Yes' : 'No'}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" className="text-center border border-gray-300 px-4 py-2">No predictions available</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Page;
