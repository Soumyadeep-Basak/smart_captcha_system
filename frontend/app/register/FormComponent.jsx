'use client';
import { useRouter } from 'next/navigation';
import React, { useState, useEffect } from 'react';
import { Bounce, toast } from 'react-toastify';
import { useDispatch, useSelector } from 'react-redux';
import { addUserInformation } from '../slice/userSlice';
import {
  Dialog,
  DialogContent,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Loader2 } from "lucide-react"
import { collectBrowserFingerprint, calculateFingerprintRisk } from '../utils/browserFingerprint';

const FormComponent = () => {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false)
  const dispatch = useDispatch();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    aadhaar: '',
    eid: '',
    fathers_name: '',
    phone: ''
  });
  const users = useSelector((state) => state.user.information);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState([{bot: null, reconstruction_error: 0}]);
  const [mousemoveCount, setMousemoveCount] = useState(0);
  const [keypressCount, setKeypressCount] = useState(0);
  const [browserFingerprint, setBrowserFingerprint] = useState(null);
  const [fingerprintRisk, setFingerprintRisk] = useState(null);

  // Function to handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    console.log('Captured events:', events);
    console.log('Browser fingerprint:', browserFingerprint);
    console.log('Fingerprint risk assessment:', fingerprintRisk);
    
    captureEvent('form_submission', e);
    setIsOpen(true);
    
    // Collect fresh browser fingerprint data at submission time
    const freshFingerprint = collectBrowserFingerprint();
    const freshRiskAssessment = calculateFingerprintRisk(freshFingerprint);
    
    // Make an API call to send the captured events and fingerprint data
    const payload = {
      mouseMoveCount: mousemoveCount, 
      keyPressCount: keypressCount, 
      events: events,
      // Enhanced fingerprinting data
      browserFingerprint: freshFingerprint,
      fingerprintRisk: freshRiskAssessment,
      metadata: {
        user_agent: navigator.userAgent || '',
        screen_resolution: `${screen.width}x${screen.height}`,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || '',
        language: navigator.language || '',
        platform: navigator.platform || '',
        webdriver_detected: navigator.webdriver || false,
        plugins_count: navigator.plugins ? navigator.plugins.length : 0,
        mime_types_count: navigator.mimeTypes ? navigator.mimeTypes.length : 0,
        touch_points: navigator.maxTouchPoints || 0,
        hardware_concurrency: navigator.hardwareConcurrency || 0,
        device_memory: navigator.deviceMemory || 0
      }
    };

    try {
      const res = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify(payload),
      });

      const result = await res.json();
      console.log('API response:', result);
      const { ip_address, user_agent, current_timestamp, prediction } = result;

      const newUser={
        ipAddress: ip_address,
        userAgent: user_agent,
        timestamp: current_timestamp,
        mouseMoveCount: mousemoveCount,
        keyPressCount: keypressCount,
        isBot:prediction[0].bot,
        // Add fingerprinting data to user record
        fingerprintRisk: freshRiskAssessment,
        browserFeatures: {
          webdriver: freshFingerprint.webdriver_detected,
          plugins: freshFingerprint.plugins_count,
          mimeTypes: freshFingerprint.mime_types_count,
          screenSize: `${freshFingerprint.screen_width}x${freshFingerprint.screen_height}`,
          touchPoints: freshFingerprint.max_touch_points,
          suspiciousPatterns: freshFingerprint.suspicious_ua_patterns
        }
      }
      
      dispatch(addUserInformation(newUser));
      const savedUsers = JSON.parse(localStorage.getItem('users')) || [];
      savedUsers.push(newUser);
      localStorage.setItem('users', JSON.stringify(savedUsers));
      console.log("user ",newUser);
      setResult(result);

      // CORRECTED LOGIC: bot=true should redirect to captcha, bot=false should show success
      if(prediction[0].bot === true){
        // Bot detected (reconstruction error < 300) - redirect to captcha
        router.push('/verify');
      } else if(prediction[0].bot === false){
        // Human detected (reconstruction error >= 300) - show success
        toast.success('Form Submitted Successfully', {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "light",
          transition: Bounce,
        });
      }
    } catch (error) {
      console.error('Error submitting event data:', error);
      // Show error toast when API call fails
      toast.error('Failed to submit form. Please try again.', {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "light",
        transition: Bounce,
      });
    } finally {
      setIsOpen(false);
    }
  };


  const handleDownload = () => {

    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "event_name,timestamp,x_position,y_position\n"; // CSV header

    events.forEach(event => {
      const row = `${event.eventType},${event.timestamp},${event.x},${event.y}\n`;
      csvContent += row;
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'event_data.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  
  // Function to capture events
  const captureEvent = (event_name, event) => {
    const eventData = {
      // element: event.target.tagName || 'window',
      event_name,
      x_position: event.clientX || window.scrollX || 0,
      y_position: event.clientY || window.scrollY || 0,
      timestamp: new Date().getTime(),
    };

    if ((event_name === 'mousemove') || (event_name === 'mouseup') || (event_name === 'mouseover') || (event_name === 'mousedown') || (event_name === 'mouseout')) {
      setMousemoveCount((prevCount) => prevCount + 1);
    } else if ((event_name === 'keypress') || (event_name === 'keydown')  || (event_name === 'keyup') ) {
      setKeypressCount((prevCount) => prevCount + 1);
    }

    setEvents((prevEvents) => {
      const newEvents = [...prevEvents, eventData];
      localStorage.setItem('domEvents', JSON.stringify(newEvents));
      return newEvents;
    });
  };

  
  const clearEvents = () => {
    setEvents([]);
    localStorage.removeItem('domEvents');
  };

  
  useEffect(() => {
    const eventNames = [
      'scroll', 'mousedown', 'mousemove', 'mouseout', 'mouseover', 'mouseup', 
      'beforeunload', 'click', 'keydown', 'keypress', 'keyup', 'copy'
    ];

    const eventHandler = (event) => {
      captureEvent(event.type, event);
    };

    eventNames.forEach((eventName) => {
      window.addEventListener(eventName, eventHandler);
    });
    
    // Cleanup event listeners on component unmount
    return () => {
      eventNames.forEach((eventName) => {
        window.removeEventListener(eventName, eventHandler);
      });
    };
  }, []);

  // Collect browser fingerprint on component mount
  useEffect(() => {
    console.log('🔍 Collecting browser fingerprint...');
    const fingerprint = collectBrowserFingerprint();
    const riskAssessment = calculateFingerprintRisk(fingerprint);
    
    setBrowserFingerprint(fingerprint);
    setFingerprintRisk(riskAssessment);
    
    console.log('🔍 Initial fingerprint collected:', fingerprint);
    console.log('🚨 Risk assessment:', riskAssessment);
  }, []);

  return (
    <div className="p-8 w-full mt-24 bg-gray-100 min-h-screen grid grid-cols-2 gap-8 ">
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[350px]">
        <div className="flex items-center justify-center gap-4">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-lg font-semibold text-center">Verifying Identity</p>
        </div>
      </DialogContent>
    </Dialog>
      <div className='w-full h-full flex flex-col justify-start items-start gap-4'>
        <h1 className="text-2xl font-bold mb-4">Register Your Details</h1>
        <div className="bg-white p-6 rounded-md shadow-md w-full">
          <h2 className="text-lg font-medium mb-2">Fill the Form:</h2>
          <form
            id="event-form"
            className="space-y-4 w-full"
            onSubmit={handleSubmit}
          >
            <div>
              <label htmlFor="name" className="block text-sm font-medium mb-1">
                Name:
              </label>
              <input
                type="text"
                id="name"
                name="name"
                className="w-full border rounded-md p-2"
                required
                value={formData.name}
                onChange={handleChange}
              />
            </div>
            <div className=' flex items-center gap-4 '>
              <div className='w-1/2'>
                <label htmlFor="email" className="block text-sm font-medium mb-1">
                  Email:
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="w-full border rounded-md p-2"
                  required
                  value={formData.email}
                  onChange={handleChange}
                />
              </div>
              <div className='w-1/2'>
                <label htmlFor="fathers_name" className="block text-sm font-medium mb-1">
                  Father{"'"}s Name:
                </label>
                <input
                  type="text"
                  id="fathers_name"
                  name="fathers_name"
                  className="w-full border rounded-md p-2"
                  required
                  value={formData.fathers_name}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className='flex gap-4 items-center'>
              <div className='w-full'>
                <label htmlFor="aadhaar" className="block text-sm font-medium mb-1">
                  Aadhaar Number (14 digits):
                </label>
                <input
                  type="text"
                  id="aadhaar"
                  name="aadhaar"
                  maxLength={14}
                  pattern="\d{14}"
                  className="w-full border rounded-md p-2"
                  required
                  value={formData.aadhaar}
                  onChange={handleChange}
                />
              </div>
              <div className='w-1/2'>
            </div>
              <label htmlFor="eid" className="block text-sm font-medium mb-1">
                EID (12 digits):
              </label>
              <input
                type="text"
                id="eid"
                name="eid"
                maxLength={12}
                pattern="\d{12}"
                className="w-full border rounded-md p-2"
                required
                value={formData.eid}
                onChange={handleChange}
              />
            </div>
        
            <div>
              <label htmlFor="phone" className="block text-sm font-medium mb-1">
                Phone Number:
              </label>
              <input
                type="tel"
                id="phone"
                name="phone"
                pattern="\d{10}"
                className="w-full border rounded-md p-2"
                required
                value={formData.phone}
                onChange={handleChange}
              />
            </div>
        
            <button type="submit" id='submit' className="bg-blue-500 text-white py-2 px-4 rounded-md">
              Submit
            </button>
          </form>
        </div>

      </div>

      <div className="bg-white px-6 rounded-md max-h-[35rem] overflow-scroll relative flex flex-col justify-between items-center shadow-md mt-4">
          <h2 className="text-lg font-medium mb-2">Captured Events:</h2>
          <ul className="space-y-2 flex flex-col-reverse ">
            {events.map((event, index) => (
              <li key={index}>
                {`Event Type: ${event.event_name}, X: ${event.x_position}, Y: ${event.y_position}, Timestamp: ${event.timestamp}`}
              </li>
            ))}
          </ul>
          <div className='sticky bottom-0 p-4 bg-white w-full '>
            <div className='flex justify-center items-center gap-4 w-full'>
              <button
                onClick={clearEvents}
                id='clear-events'
                className="mt-4 bg-red-500 text-white py-2 px-4 rounded-md"
              >
                Clear Events
              </button>
              <button id="download-csv" onClick={handleDownload} className="mt-4 bg-green-500 text-white py-2 px-4 rounded-md">Download CSV</button>
            </div>
          </div>
        </div>
      
    </div>
  );
}

export default FormComponent;