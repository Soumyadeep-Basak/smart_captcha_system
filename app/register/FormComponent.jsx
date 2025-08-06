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
    phone: '',
    // Honeypot fields
    website_url: '',      // Hidden CSS field
    optional_info: ''     // JS-based optional field
  });
  const users = useSelector((state) => state.user.information);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState([{bot: null, reconstruction_error: 0}]);
  const [mousemoveCount, setMousemoveCount] = useState(0);
  const [keypressCount, setKeypressCount] = useState(0);
  
  // Honeypot state tracking
  const [honeypotTriggered, setHoneypotTriggered] = useState({
    hidden_field: false,
    fake_submit: false,
    js_optional: false
  });

  // Function to handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    // Check for honeypot field interactions
    if (name === 'website_url' && value.trim()) {
      console.log('🚨 HONEYPOT TRIGGERED: Hidden field filled');
      setHoneypotTriggered(prev => ({ ...prev, hidden_field: true }));
      captureEvent('honeypot_hidden_field_filled', e);
    }
    
    if (name === 'optional_info' && value.trim()) {
      console.log('🚨 HONEYPOT TRIGGERED: Optional JS field filled');
      setHoneypotTriggered(prev => ({ ...prev, js_optional: true }));
      captureEvent('honeypot_js_field_filled', e);
    }
  };
  
  // Honeypot fake submit handler
  const handleFakeSubmit = (e) => {
    e.preventDefault();
    console.log('🚨 HONEYPOT TRIGGERED: Fake submit button clicked');
    setHoneypotTriggered(prev => ({ ...prev, fake_submit: true }));
    captureEvent('honeypot_fake_submit_clicked', e);
    // Do nothing else - this is a trap
  };

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    console.log('Captured events:', events);
    captureEvent('form_submission', e);
    setIsOpen(true);
    // Make an API call to send the captured events
    const payload = {
      mouseMoveCount: mousemoveCount, 
      keyPressCount: keypressCount, 
      events: events,
      // Include honeypot data for enhanced bot detection
      honeypot_data: {
        hidden_honeypot_field: formData.website_url,
        fake_submit_clicked: honeypotTriggered.fake_submit,
        js_optional_field: formData.optional_info,
        js_enabled: typeof window !== 'undefined' && window.navigator && navigator.userAgent,
        honeypot_triggers: honeypotTriggered
      },
      // Include user agent and other metadata
      metadata: {
        user_agent: typeof window !== 'undefined' ? navigator.userAgent : '',
        timestamp: new Date().toISOString(),
        form_data: {
          name: formData.name,
          email: formData.email,
          phone: formData.phone
        }
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
      console.log('Enhanced analysis:', result.enhanced_analysis);
      console.log('Honeypot analysis:', result.enhanced_analysis?.honeypot_analysis);
      
      const { ip_address, user_agent, current_timestamp, prediction, enhanced_analysis } = result;

      // Create enhanced user object with honeypot data
      const newUser = {
        ipAddress: ip_address,
        userAgent: user_agent,
        timestamp: current_timestamp,
        mouseMoveCount: mousemoveCount,
        keyPressCount: keypressCount,
        isBot: prediction[0].bot,
        // Add enhanced analysis data for admin panel
        enhanced_analysis: enhanced_analysis,
        prediction: prediction,
        // Add honeypot specific data
        honeypot_data: {
          honeypots_triggered: enhanced_analysis?.honeypot_analysis?.honeypot_summary?.triggered_honeypots || 0,
          threat_level: enhanced_analysis?.honeypot_analysis?.threat_level || 'low',
          honeypot_score: enhanced_analysis?.honeypot_analysis?.honeypot_score || 0,
          detailed_results: enhanced_analysis?.honeypot_analysis?.honeypot_details?.detailed_results || {}
        }
      }
      
      dispatch(addUserInformation(newUser));
      const savedUsers = JSON.parse(localStorage.getItem('users')) || [];
      savedUsers.push(newUser);
      localStorage.setItem('users', JSON.stringify(savedUsers));
      console.log("Enhanced user data saved:", newUser);
      setResult(result);

      // ENHANCED LOGIC: Check both ML prediction and honeypot analysis
      const mlBotDetection = prediction[0].bot;
      const honeypotThreatDetected = enhanced_analysis?.honeypot_analysis?.threat_detected || false;
      const finalVerdict = enhanced_analysis?.final_verdict?.is_bot || false;
      
      console.log('🔍 Detection Results:');
      console.log('  - ML Bot Detection:', mlBotDetection);
      console.log('  - Honeypot Threat Detected:', honeypotThreatDetected);
      console.log('  - Final Verdict:', finalVerdict);
      console.log('  - Honeypots Triggered:', enhanced_analysis?.honeypot_analysis?.honeypot_summary?.triggered_honeypots || 0);

      // Use final verdict (which includes honeypot analysis) for decision
      if(finalVerdict === true || honeypotThreatDetected === true){
        // Bot detected by either ML or honeypots - redirect to captcha
        console.log('🚨 BOT DETECTED - Redirecting to verification');
        router.push('/verify');
      } else {
        // Human detected - show success
        console.log('✅ HUMAN DETECTED - Showing success message');
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
    
    // Honeypot JS field management - Hide field if JS is enabled
    const jsOptionalContainer = document.getElementById('js-optional-container');
    if (jsOptionalContainer) {
      // Keep it hidden if JS is working properly
      jsOptionalContainer.style.display = 'none';
      console.log('🍯 Honeypot: JS optional field hidden (JS is enabled)');
    }
    
    // Cleanup event listeners on component unmount
    return () => {
      eventNames.forEach((eventName) => {
        window.removeEventListener(eventName, eventHandler);
      });
    };
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
        
            {/* Honeypot Fields - Bot Detection */}
            {/* 1. Hidden CSS Field - Only bots can see this */}
            <div className="honeypot-hidden" style={{position: 'absolute', left: '-9999px', visibility: 'hidden', opacity: 0}}>
              <label htmlFor="website_url">Website URL (leave blank):</label>
              <input
                type="text"
                id="website_url"
                name="website_url"
                value={formData.website_url}
                onChange={handleChange}
                tabIndex="-1"
                autoComplete="off"
              />
            </div>
            
            {/* 2. Fake Submit Button - Invisible to humans */}
            <button 
              type="button"
              className="honeypot-fake-submit"
              style={{position: 'absolute', left: '-9999px', visibility: 'hidden', opacity: 0}}
              onClick={handleFakeSubmit}
              tabIndex="-1"
            >
              Submit Form
            </button>
            
            {/* 3. JS-based Optional Field - Should be hidden by JS if enabled */}
            <div className="honeypot-js-field" style={{display: 'none'}} id="js-optional-container">
              <label htmlFor="optional_info" className="block text-sm font-medium mb-1">
                Additional Info (Optional):
              </label>
              <input
                type="text"
                id="optional_info"
                name="optional_info"
                value={formData.optional_info}
                onChange={handleChange}
                placeholder="This field should remain empty"
                className="w-full border rounded-md p-2"
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