"use client"
import React, { useState, useEffect } from 'react';

const FormComponent = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    aadhaar: '',
    eid: '',
    fathers_name: '',
    phone: '',
    message: ''
  });

  const [events, setEvents] = useState([]);

  // Function to handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };
  const [loading, setLoading] = useState(false);

  const runSeleniumScript = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/bot', { method: 'GET' });
      const data = await res.text();
      console.log('Selenium response:', data);
    } catch (error) {
      console.error('Error running Selenium script:', error);
    } finally {
      setLoading(false);
    }
  };
  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);

    // Log all captured events to the console when the form is submitted
    console.log('Captured events:', events);

    // Optionally, capture a 'form_submission' event
    captureEvent('form_submission', e);
  };

  // Function to capture events
  const captureEvent = (eventType, event) => {
    const eventData = {
      element: event.target.tagName || 'window', // Capturing the element (e.g., button, input, etc.)
      eventType,
      x: event.clientX || 0, // Mouse position X
      y: event.clientY || 0, // Mouse position Y
      timestamp: new Date().toISOString(), // Timestamp of the event
    };

    setEvents((prevEvents) => {
      const newEvents = [...prevEvents, eventData];
      localStorage.setItem('domEvents', JSON.stringify(newEvents));
      return newEvents;
    });
  };

  // Clear event list and localStorage
  const clearEvents = () => {
    setEvents([]);
    localStorage.removeItem('domEvents');
  };

  // Attach event listeners to the window
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

  return (
    <div className="p-8 w-full mt-24 bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Form with Event Data Capture</h1>

      <div className="bg-white p-6 rounded-md shadow-md">
        <h2 className="text-lg font-medium mb-2">Fill the Form:</h2>
        <form
          id="event-form"
          className="space-y-4 max-w-[50%] "
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
          <div>
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
          <div>
            <label htmlFor="aadhaar" className="block text-sm font-medium mb-1">
              Aadhaar Number (14 digits):
            </label>
            <input
              type="text"
              id="aadhaar"
              name="aadhaar"
              maxLength="14"
              pattern="\d{14}"
              className="w-full border rounded-md p-2"
              required
              value={formData.aadhaar}
              onChange={handleChange}
            />
          </div>
          <div>
            <label htmlFor="eid" className="block text-sm font-medium mb-1">
              EID (12 digits):
            </label>
            <input
              type="text"
              id="eid"
              name="eid"
              maxLength="12"
              pattern="\d{12}"
              className="w-full border rounded-md p-2"
              required
              value={formData.eid}
              onChange={handleChange}
            />
          </div>
          <div>
            <label
              htmlFor="fathers_name"
              className="block text-sm font-medium mb-1"
            >
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
          <div>
            <label htmlFor="message" className="block text-sm font-medium mb-1">
              Message:
            </label>
            <textarea
              id="message"
              name="message"
              className="w-full border rounded-md p-2"
              rows="4"
              required
              value={formData.message}
              onChange={handleChange}
            ></textarea>
          </div>
          
          <button
            type="submit"
            className="bg-blue-500 text-white py-2 px-4 rounded-md"
          >
            Submit
          </button>
          <button className="bg-red-500 ml-10 text-white py-2 px-4 rounded-md" onClick={runSeleniumScript} disabled={loading}>
              {loading ? "Running..." : "Run Bot"}
            </button>
        </form>
      </div>

      <div className="bg-white p-6 rounded-md shadow-md mt-4">
        <button
          onClick={clearEvents}
          className="mt-4 bg-red-500 text-white py-2 px-4 rounded-md"
        >
          Clear Events
        </button>
        <h2 className="text-lg font-medium mb-2">Captured Events:</h2>
        <ul className="space-y-2">
          {events.map((event, index) => (
            <li key={index}>
              {`Element: ${event.element}, Event Type: ${event.eventType}, X: ${event.x}, Y: ${event.y}, Timestamp: ${event.timestamp}`}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default FormComponent;
