'use client';

import React, { useState, useEffect } from 'react';

const Page = () => {
  const [predictions, setPredictions] = useState([]);
  const [selectedPrediction, setSelectedPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        setLoading(true);
        console.log('🔍 Fetching predictions from API...');
        
        // Try to fetch from the enhanced API first
        let response;
        try {
          response = await fetch('http://127.0.0.1:5000/predictions');
          
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
          
          const data = await response.json();
          console.log('✅ API Response received:', data);
          
          // Handle both array and object responses
          const predictions = Array.isArray(data) ? data : (data.predictions || []);
          setPredictions(predictions);
          console.log(`📊 Loaded ${predictions.length} predictions from API`);
          
        } catch (apiError) {
          console.warn('⚠️ API Error:', apiError);
          console.log('🔄 Falling back to localStorage...');
          
          // Fallback to localStorage data but enhance it with proper structure
          const savedUsers = JSON.parse(localStorage.getItem('users')) || [];
          
          // If no localStorage data either, create some sample data for testing
          if (savedUsers.length === 0) {
            console.log('📝 No data found, creating sample data...');
            const sampleData = [
              {
                ipAddress: '192.168.1.100',
                userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                timestamp: new Date().toISOString(),
                mouseMoveCount: 850,
                keyPressCount: 120,
                isBot: false,
                prediction: [{bot: false, reconstruction_error: 450.3}],
                enhanced_analysis: {
                  honeypot_analysis: {
                    threat_detected: false,
                    threat_level: 'low',
                    honeypot_score: 0.0,
                    confidence: 0.95,
                    honeypot_summary: {
                      triggered_honeypots: 0,
                      total_honeypots: 3,
                      honeypot_types_triggered: []
                    },
                    honeypot_details: {
                      detailed_results: {
                        hidden_field: { triggered: false, score: 0.0, details: 'Not triggered' },
                        fake_submit: { triggered: false, score: 0.0, details: 'Not triggered' },
                        optional_field: { triggered: false, score: 0.0, details: 'Not triggered' }
                      }
                    }
                  }
                },
                browserFeatures: {
                  webdriver: false,
                  plugins: 12,
                  mimeTypes: 45,
                  screenSize: '1920x1080',
                  touchPoints: 10,
                  suspiciousPatterns: []
                },
                fingerprintRisk: {
                  riskLevel: 'low',
                  riskScore: 0.15,
                  isBot: false,
                  riskFactors: []
                }
              },
              {
                ipAddress: '127.0.0.1',
                userAgent: 'Python-urllib/3.9',
                timestamp: new Date(Date.now() - 300000).toISOString(),
                mouseMoveCount: 150,
                keyPressCount: 25,
                isBot: true,
                prediction: [{bot: true, reconstruction_error: 150.5}],
                enhanced_analysis: {
                  honeypot_analysis: {
                    threat_detected: true,
                    threat_level: 'critical',
                    honeypot_score: 1.0,
                    confidence: 0.95,
                    honeypot_summary: {
                      triggered_honeypots: 3,
                      total_honeypots: 3,
                      honeypot_types_triggered: ['hidden_field', 'fake_submit', 'optional_field']
                    },
                    honeypot_details: {
                      detailed_results: {
                        hidden_field: { triggered: true, score: 1.0, details: 'Hidden field filled with malicious URL' },
                        fake_submit: { triggered: true, score: 1.0, details: 'Invisible fake submit button clicked' },
                        optional_field: { triggered: true, score: 1.0, details: 'JS field filled without JavaScript' }
                      }
                    }
                  }
                },
                browserFeatures: {
                  webdriver: true,
                  plugins: 0,
                  mimeTypes: 0,
                  screenSize: '1920x1080',
                  touchPoints: 0,
                  suspiciousPatterns: ['webdriver detected']
                },
                fingerprintRisk: {
                  riskLevel: 'high',
                  riskScore: 0.85,
                  isBot: true,
                  riskFactors: ['WebDriver detected', 'No plugins']
                }
              }
            ];
            
            // Save sample data to localStorage for future use
            localStorage.setItem('users', JSON.stringify(sampleData));
            setPredictions(sampleData);
            console.log(`📊 Created ${sampleData.length} sample predictions`);
          } else {
            setPredictions(savedUsers);
            console.log(`📱 Loaded ${savedUsers.length} predictions from localStorage`);
          }
          
          setError(`API Error: ${apiError.message}. Showing cached data.`);
        }
        
      } catch (error) {
        console.error('❌ Critical Error fetching predictions:', error);
        setError(error.message);
        
        // Final fallback to empty array
        setPredictions([]);
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, []);

  const getRiskLevelColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading predictions...</div>
      </div>
    );
  }

  return (
    <div className="p-6 mt-16 max-w-6xl mx-auto">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">🔍 Bot Detection Logs</h1>
            <p className="text-gray-600">Click on any log entry to view detailed analysis</p>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg"
          >
            🔄 Refresh
          </button>
        </div>
        
        {error && (
          <div className="mt-2 p-3 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded">
            ⚠️ {error}
          </div>
        )}
        
        {/* Debug Info */}
        <div className="text-sm text-gray-500 mb-4">
          Status: {loading ? 'Loading...' : `${Array.isArray(predictions) ? predictions.length : 0} entries loaded`}
          {predictions.length > 0 && (
            <span className="ml-4">
              • Data source: {error ? 'localStorage (offline)' : 'API (online)'}
            </span>
          )}
        </div>
      </div>

      {/* Simple Log View */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-4 border-b bg-gray-50">
          <h2 className="text-lg font-semibold">Detection Logs</h2>
          <p className="text-sm text-gray-600">
            Total: {Array.isArray(predictions) ? predictions.length : 0} entries
          </p>
        </div>
        
        <div className="divide-y divide-gray-200">
          {predictions && predictions.length > 0 ? (
            predictions.slice().reverse().map((prediction, index) => {
              const isBot = prediction.isBot ?? prediction.prediction?.[0]?.bot ?? false;
              const reconstructionError = prediction.prediction?.[0]?.reconstruction_error;
              const timestamp = new Date(prediction.timestamp).toLocaleString();
              const ipAddress = prediction.ipAddress || prediction.ip_address || 'Unknown IP';
              
              return (
                <div
                  key={index}
                  onClick={() => setSelectedPrediction(prediction)}
                  className={`p-4 cursor-pointer hover:bg-gray-50 transition-colors ${
                    isBot 
                      ? 'border-l-4 border-red-500 bg-red-50' 
                      : 'border-l-4 border-green-500 bg-green-50'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-4">
                      <div className={`w-3 h-3 rounded-full ${
                        isBot ? 'bg-red-500' : 'bg-green-500'
                      }`}></div>
                      
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className={`px-3 py-1 text-sm font-medium rounded-full ${
                            isBot 
                              ? 'bg-red-100 text-red-800' 
                              : 'bg-green-100 text-green-800'
                          }`}>
                            {isBot ? '🤖 BOT DETECTED' : '👤 HUMAN VERIFIED'}
                          </span>
                          
                          {prediction.fingerprintRisk && (
                            <span className={`px-2 py-1 text-xs rounded ${getRiskLevelColor(prediction.fingerprintRisk.riskLevel)}`}>
                              {prediction.fingerprintRisk.riskLevel?.toUpperCase()}
                            </span>
                          )}
                        </div>
                        
                        <div className="mt-1 text-sm text-gray-600">
                          <span className="font-medium">{ipAddress}</span>
                          {reconstructionError && (
                            <span className="ml-2">• Error: {reconstructionError.toFixed(3)}</span>
                          )}
                          <span className="ml-2">• {timestamp}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-sm text-gray-500">
                      <div>🖱️ {prediction.mouseMoveCount || 0} • ⌨️ {prediction.keyPressCount || 0}</div>
                      {prediction.browserFeatures?.webdriver && (
                        <div className="text-red-600 text-xs">⚠️ WebDriver detected</div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="text-center py-12 text-gray-500">
              <div className="text-lg mb-2">📝 No logs available</div>
              <div className="text-sm">Submit a form to see detection results here</div>
            </div>
          )}
        </div>
      </div>

      {/* Detailed Analysis Modal */}
      {selectedPrediction && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">🔍 Detailed Analysis Report</h2>
                <button
                  onClick={() => setSelectedPrediction(null)}
                  className="text-gray-500 hover:text-gray-700 text-2xl font-bold w-8 h-8 flex items-center justify-center rounded hover:bg-gray-100"
                >
                  ×
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* ML Model Results */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold border-b pb-2">🤖 ML Model Detection</h3>
                  <div className="space-y-3">
                    <div className="bg-gray-50 p-4 rounded">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Detection Result:</span>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          (selectedPrediction.isBot ?? selectedPrediction.prediction?.[0]?.bot) 
                            ? 'bg-red-100 text-red-800' 
                            : 'bg-green-100 text-green-800'
                        }`}>
                          {(selectedPrediction.isBot ?? selectedPrediction.prediction?.[0]?.bot) ? '🤖 BOT' : '👤 HUMAN'}
                        </span>
                      </div>
                      {selectedPrediction.prediction?.[0]?.reconstruction_error && (
                        <div className="text-sm text-gray-600">
                          <strong>Reconstruction Error:</strong> {selectedPrediction.prediction[0].reconstruction_error.toFixed(6)}
                          <div className="text-xs mt-1">
                            (Threshold: {selectedPrediction.prediction[0].reconstruction_error >= 300 ? 'Human ≥300' : 'Bot <300'})
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Behavioral Analysis */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold border-b pb-2">👆 Behavioral Analysis</h3>
                  <div className="space-y-3">
                    <div className="bg-gray-50 p-4 rounded">
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="font-medium">Mouse Events:</span>
                          <div className="text-lg font-bold text-blue-600">{selectedPrediction.mouseMoveCount || 0}</div>
                        </div>
                        <div>
                          <span className="font-medium">Keyboard Events:</span>
                          <div className="text-lg font-bold text-green-600">{selectedPrediction.keyPressCount || 0}</div>
                        </div>
                      </div>
                      <div className="mt-2 text-xs text-gray-500">
                        Interaction patterns analyzed for bot-like behavior
                      </div>
                    </div>
                  </div>
                </div>

                {/* Browser Fingerprinting */}
                {selectedPrediction.browserFeatures && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold border-b pb-2">🔍 Enhanced Browser Fingerprinting</h3>
                    <div className="space-y-3">
                      
                      {/* Basic Features */}
                      <div className="bg-gray-50 p-4 rounded">
                        <h4 className="font-medium text-sm mb-3 text-gray-700">Basic Browser Features</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span>WebDriver Detection:</span>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              selectedPrediction.browserFeatures.webdriver ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                            }`}>
                              {selectedPrediction.browserFeatures.webdriver ? '❌ DETECTED' : '✅ CLEAN'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Browser Plugins:</span>
                            <span className={`font-medium ${selectedPrediction.browserFeatures.plugins === 0 ? 'text-red-600' : 'text-green-600'}`}>
                              {selectedPrediction.browserFeatures.plugins}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>MIME Types:</span>
                            <span className={`font-medium ${selectedPrediction.browserFeatures.mimeTypes === 0 ? 'text-red-600' : 'text-green-600'}`}>
                              {selectedPrediction.browserFeatures.mimeTypes}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Fonts Detected:</span>
                            <span className={`font-medium ${(selectedPrediction.browserFeatures.fonts || 0) === 0 ? 'text-red-600' : 'text-green-600'}`}>
                              {selectedPrediction.browserFeatures.fonts || 0}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Screen Resolution:</span>
                            <span className="font-medium">{selectedPrediction.browserFeatures.screenSize}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Touch Points:</span>
                            <span className="font-medium">{selectedPrediction.browserFeatures.touchPoints}</span>
                          </div>
                        </div>
                      </div>

                      {/* Zero Features Warning */}
                      {(selectedPrediction.browserFeatures.plugins === 0 || 
                        selectedPrediction.browserFeatures.mimeTypes === 0 || 
                        (selectedPrediction.browserFeatures.fonts || 0) === 0) && (
                        <div className="bg-red-50 border border-red-200 p-3 rounded">
                          <div className="flex items-center">
                            <span className="text-red-600 text-lg mr-2">⚠️</span>
                            <div>
                              <div className="text-red-800 font-medium text-sm">Headless Pattern Detected</div>
                              <div className="text-red-700 text-xs mt-1">
                                Multiple zero features indicate possible headless browser or automation tool
                              </div>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Automation Detection */}
                      {selectedPrediction.browserFeatures.automationSignatures && selectedPrediction.browserFeatures.automationSignatures.length > 0 && (
                        <div className="bg-red-50 p-4 rounded border border-red-200">
                          <h4 className="font-medium text-sm mb-3 text-red-800">🤖 Automation Signatures Detected</h4>
                          <div className="space-y-1">
                            {selectedPrediction.browserFeatures.automationSignatures.map((sig, idx) => (
                              <div key={idx} className="text-xs text-red-700 bg-red-100 px-2 py-1 rounded inline-block mr-2 mb-1">
                                {sig}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Canvas & WebGL Analysis */}
                      <div className="bg-blue-50 p-4 rounded">
                        <h4 className="font-medium text-sm mb-3 text-blue-800">🎨 Canvas & WebGL Analysis</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span>Canvas Support:</span>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              selectedPrediction.browserFeatures.canvasSupported !== false ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                              {selectedPrediction.browserFeatures.canvasSupported !== false ? 'SUPPORTED' : 'MISSING'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>WebGL Support:</span>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              selectedPrediction.browserFeatures.webglSupported !== false ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                              {selectedPrediction.browserFeatures.webglSupported !== false ? 'SUPPORTED' : 'MISSING'}
                            </span>
                          </div>
                          {selectedPrediction.browserFeatures.webglVendor && (
                            <div className="flex justify-between">
                              <span>WebGL Vendor:</span>
                              <span className="font-medium text-xs">{selectedPrediction.browserFeatures.webglVendor}</span>
                            </div>
                          )}
                          {selectedPrediction.browserFeatures.webglRenderer && (
                            <div className="flex justify-between">
                              <span>WebGL Renderer:</span>
                              <span className="font-medium text-xs">{selectedPrediction.browserFeatures.webglRenderer}</span>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Suspicious Patterns */}
                      {selectedPrediction.browserFeatures.suspiciousPatterns?.length > 0 && (
                        <div className="bg-orange-50 p-4 rounded border border-orange-200">
                          <h4 className="font-medium text-sm mb-3 text-orange-800">🚩 Suspicious Patterns</h4>
                          <div className="space-y-1">
                            {selectedPrediction.browserFeatures.suspiciousPatterns.map((pattern, idx) => (
                              <div key={idx} className="text-xs text-orange-700 bg-orange-100 px-2 py-1 rounded inline-block mr-2 mb-1">
                                {pattern}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Analysis Patterns */}
                {selectedPrediction.analysisPatterns && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold border-b pb-2">🧠 Advanced Analysis</h3>
                    <div className="space-y-3">
                      
                      {/* Automation Detection */}
                      {selectedPrediction.analysisPatterns.automationDetected && (
                        <div className="bg-red-50 border border-red-200 p-4 rounded">
                          <div className="flex items-center mb-3">
                            <span className="text-red-600 text-lg mr-2">🤖</span>
                            <div className="text-red-800 font-medium">Automation Tool Detected</div>
                          </div>
                          <div className="text-red-700 text-sm">
                            High confidence automation signatures identified
                          </div>
                        </div>
                      )}

                      {/* Zero Feature Analysis */}
                      {selectedPrediction.analysisPatterns.zeroFeaturesDetected && (
                        <div className="bg-orange-50 border border-orange-200 p-4 rounded">
                          <div className="flex items-center mb-3">
                            <span className="text-orange-600 text-lg mr-2">🔍</span>
                            <div className="text-orange-800 font-medium">Zero-Feature Pattern</div>
                          </div>
                          <div className="text-orange-700 text-sm">
                            Multiple critical features show zero values (typical of headless browsers)
                          </div>
                          <div className="mt-2 text-xs text-orange-600">
                            Zero Features: {selectedPrediction.analysisPatterns.zeroFeaturesList?.join(', ') || 'plugins, mimeTypes, fonts'}
                          </div>
                        </div>
                      )}

                      {/* Canvas Signature Analysis */}
                      {selectedPrediction.analysisPatterns.canvasSignature && (
                        <div className="bg-blue-50 p-4 rounded">
                          <h4 className="font-medium text-sm mb-3 text-blue-800">🎨 Canvas Signature</h4>
                          <div className="space-y-2 text-sm">
                            <div className="flex justify-between">
                              <span>Canvas Hash:</span>
                              <span className="font-mono text-xs">{selectedPrediction.analysisPatterns.canvasSignature}</span>
                            </div>
                            {selectedPrediction.analysisPatterns.canvasDuplicate && (
                              <div className="bg-red-100 border border-red-200 p-2 rounded mt-2">
                                <div className="text-red-800 font-medium text-xs">⚠️ Duplicate Canvas Signature</div>
                                <div className="text-red-700 text-xs mt-1">
                                  This canvas signature has been seen from other IP addresses
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Timing Analysis */}
                      {selectedPrediction.analysisPatterns.timingAnalysis && (
                        <div className="bg-purple-50 p-4 rounded">
                          <h4 className="font-medium text-sm mb-3 text-purple-800">⏱️ Timing Analysis</h4>
                          <div className="space-y-2 text-sm">
                            {selectedPrediction.analysisPatterns.timingAnalysis.perfectTiming && (
                              <div className="text-purple-700">• Perfect timing patterns detected (automation signature)</div>
                            )}
                            {selectedPrediction.analysisPatterns.timingAnalysis.zeroDelays && (
                              <div className="text-purple-700">• Zero delays between actions</div>
                            )}
                            {selectedPrediction.analysisPatterns.timingAnalysis.consistentIntervals && (
                              <div className="text-purple-700">• Consistent intervals (non-human)</div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Behavioral Consistency */}
                      {selectedPrediction.analysisPatterns.behavioralConsistency && (
                        <div className="bg-green-50 p-4 rounded">
                          <h4 className="font-medium text-sm mb-3 text-green-800">🎯 Behavioral Analysis</h4>
                          <div className="space-y-2 text-sm">
                            <div className="flex justify-between">
                              <span>Consistency Score:</span>
                              <span className={`font-medium ${
                                selectedPrediction.analysisPatterns.behavioralConsistency.score > 0.8 ? 'text-red-600' : 
                                selectedPrediction.analysisPatterns.behavioralConsistency.score > 0.6 ? 'text-orange-600' : 'text-green-600'
                              }`}>
                                {(selectedPrediction.analysisPatterns.behavioralConsistency.score * 100).toFixed(1)}%
                              </span>
                            </div>
                            {selectedPrediction.analysisPatterns.behavioralConsistency.inconsistencies && (
                              <div className="mt-2">
                                <div className="text-green-700 text-xs mb-1">Inconsistencies found:</div>
                                {selectedPrediction.analysisPatterns.behavioralConsistency.inconsistencies.map((inc, idx) => (
                                  <div key={idx} className="text-green-600 text-xs">• {inc}</div>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Risk Assessment */}
                {selectedPrediction.fingerprintRisk && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold border-b pb-2">🚨 Risk Assessment</h3>
                    <div className="space-y-3">
                      <div className="bg-gray-50 p-4 rounded">
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between items-center">
                            <span>Overall Risk Level:</span>
                            <span className={`px-3 py-1 rounded font-medium ${getRiskLevelColor(selectedPrediction.fingerprintRisk.riskLevel)}`}>
                              {selectedPrediction.fingerprintRisk.riskLevel?.toUpperCase()}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Risk Score:</span>
                            <span className="font-bold">{(selectedPrediction.fingerprintRisk.riskScore * 100).toFixed(1)}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Bot Likelihood:</span>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              selectedPrediction.fingerprintRisk.isBot ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                            }`}>
                              {selectedPrediction.fingerprintRisk.isBot ? 'HIGH' : 'LOW'}
                            </span>
                          </div>
                          {selectedPrediction.fingerprintRisk.riskFactors?.length > 0 && (
                            <div className="mt-3 p-2 bg-yellow-50 rounded">
                              <div className="text-yellow-800 font-medium text-xs">Risk Factors Identified:</div>
                              <ul className="mt-1 text-yellow-700 text-xs">
                                {selectedPrediction.fingerprintRisk.riskFactors.map((factor, idx) => (
                                  <li key={idx}>• {factor}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Honeypot Analysis Section */}
                {selectedPrediction.enhanced_analysis?.honeypot_analysis && (
                  <div className="md:col-span-2 space-y-4">
                    <h3 className="text-lg font-semibold border-b pb-2">🍯 Honeypot Detection Analysis</h3>
                    <div className="bg-yellow-50 border border-yellow-200 p-4 rounded">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Overall Honeypot Results */}
                        <div className="space-y-3">
                          <div className="flex items-center justify-between">
                            <span className="font-medium">Honeypot Detection:</span>
                            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                              selectedPrediction.enhanced_analysis.honeypot_analysis.threat_detected
                                ? 'bg-red-100 text-red-800' 
                                : 'bg-green-100 text-green-800'
                            }`}>
                              {selectedPrediction.enhanced_analysis.honeypot_analysis.threat_detected ? '🚨 THREAT' : '✅ CLEAN'}
                            </span>
                          </div>
                          <div className="space-y-2 text-sm">
                            <div className="flex justify-between">
                              <span>Threat Level:</span>
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                selectedPrediction.enhanced_analysis.honeypot_analysis.threat_level === 'critical' ? 'bg-red-100 text-red-800' :
                                selectedPrediction.enhanced_analysis.honeypot_analysis.threat_level === 'high' ? 'bg-orange-100 text-orange-800' :
                                selectedPrediction.enhanced_analysis.honeypot_analysis.threat_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {selectedPrediction.enhanced_analysis.honeypot_analysis.threat_level?.toUpperCase()}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Honeypot Score:</span>
                              <span className="font-medium">
                                {(selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_score * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Confidence:</span>
                              <span className="font-medium">
                                {(selectedPrediction.enhanced_analysis.honeypot_analysis.confidence * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                        </div>

                        {/* Honeypot Triggers */}
                        <div className="space-y-3">
                          <h4 className="font-medium text-sm">🎯 Honeypot Triggers</h4>
                          {selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_summary && (
                            <div className="space-y-2">
                              <div className="flex justify-between text-sm">
                                <span>Triggered Honeypots:</span>
                                <span className="font-medium">
                                  {selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_summary.triggered_honeypots}/
                                  {selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_summary.total_honeypots}
                                </span>
                              </div>
                              
                              {/* Individual Honeypot Status */}
                              <div className="space-y-1">
                                {selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_summary.honeypot_types_triggered && 
                                 selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_summary.honeypot_types_triggered.length > 0 && (
                                  <div>
                                    <div className="text-xs font-medium text-red-700 mb-1">🚨 Triggered:</div>
                                    {selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_summary.honeypot_types_triggered.map((type, idx) => (
                                      <div key={idx} className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded inline-block mr-1 mb-1">
                                        {type.replace('_', ' ').toUpperCase()}
                                      </div>
                                    ))}
                                  </div>
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Detailed Honeypot Results */}
                      {selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_details?.detailed_results && (
                        <div className="mt-4 pt-4 border-t border-yellow-300">
                          <h4 className="font-medium text-sm mb-3">📋 Detailed Honeypot Analysis</h4>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                            {Object.entries(selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_details.detailed_results).map(([type, details], idx) => (
                              <div key={idx} className={`p-3 rounded text-sm ${
                                details.triggered ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'
                              }`}>
                                <div className="font-medium mb-1">
                                  {details.triggered ? '🚨' : '✅'} {type.replace('_', ' ').toUpperCase()}
                                </div>
                                <div className={`text-xs ${details.triggered ? 'text-red-700' : 'text-green-700'}`}>
                                  {details.triggered ? details.details || 'Triggered' : 'Not triggered'}
                                </div>
                                <div className="text-xs mt-1 font-medium">
                                  Weight: {type === 'hidden_field' ? '40%' : type === 'fake_submit' ? '30%' : '30%'} | 
                                  Score: {(details.score * 100).toFixed(0)}%
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Final Decision Impact */}
                      {selectedPrediction.enhanced_analysis?.final_verdict?.contributing_factors?.honeypot && (
                        <div className="mt-4 pt-4 border-t border-yellow-300">
                          <h4 className="font-medium text-sm mb-3">🎯 Honeypot Impact on Final Decision</h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                            <div className="space-y-2">
                              <div className="flex justify-between">
                                <span>Honeypot Weight in Decision:</span>
                                <span className="font-medium text-yellow-700">45%</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Honeypot Contribution:</span>
                                <span className="font-medium">
                                  {(selectedPrediction.enhanced_analysis.final_verdict.contributing_factors.honeypot.confidence * 
                                    selectedPrediction.enhanced_analysis.final_verdict.contributing_factors.honeypot.weight * 100).toFixed(1)}%
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span>Trigger Bonus Applied:</span>
                                <span className="font-medium">
                                  {selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_summary?.triggered_honeypots ? 
                                    `+${selectedPrediction.enhanced_analysis.honeypot_analysis.honeypot_summary.triggered_honeypots * 15}%` : 
                                    '0%'}
                                </span>
                              </div>
                            </div>
                            <div className="space-y-2">
                              <div className="text-xs">
                                <div className="font-medium mb-1">Detection Formula:</div>
                                <div className="bg-gray-100 p-2 rounded font-mono text-xs">
                                  Final = (ML×35%) + (Fingerprint×20%) + (Honeypot×45%) + Trigger Bonus
                                </div>
                              </div>
                              <div className="text-xs">
                                <div className="font-medium mb-1">Decision Logic:</div>
                                <div className="text-gray-600">
                                  {selectedPrediction.enhanced_analysis?.final_verdict?.decision_logic || 'Standard threshold evaluation'}
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Detection Method */}
                      <div className="mt-3 pt-3 border-t border-yellow-300 text-xs text-yellow-800">
                        <strong>Detection Method:</strong> {selectedPrediction.enhanced_analysis.honeypot_analysis.detection_method || 'Multi-layer Honeypot'}
                      </div>
                    </div>
                  </div>
                )}

                {/* System Information */}
                <div className="md:col-span-2 space-y-4">
                  <h3 className="text-lg font-semibold border-b pb-2">💻 System Information</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-4 rounded">
                      <div className="space-y-2 text-sm">
                        <div><strong>IP Address:</strong> {selectedPrediction.ipAddress || selectedPrediction.ip_address}</div>
                        <div><strong>Timestamp:</strong> {new Date(selectedPrediction.timestamp).toLocaleString()}</div>
                      </div>
                    </div>
                    <div className="bg-gray-50 p-4 rounded">
                      <div className="text-sm">
                        <div className="font-medium mb-2">User Agent:</div>
                        <div className="bg-white p-2 rounded text-xs font-mono break-all border">
                          {selectedPrediction.userAgent || selectedPrediction.user_agent || 'N/A'}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t">
                <button
                  onClick={() => setSelectedPrediction(null)}
                  className="w-full bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium py-2 px-4 rounded transition-colors"
                >
                  Close Analysis
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Page;
