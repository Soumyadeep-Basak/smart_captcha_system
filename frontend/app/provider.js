'use client'; 

import React from 'react';
import { Provider } from 'react-redux';
import PropTypes from 'prop-types';
import store from './store';

 const ReduxProvider = ({ children }) => {
  return <Provider store={store}>{children}</Provider>;
};

// Adding prop types for validation (optional but recommended)
ReduxProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export default ReduxProvider;


