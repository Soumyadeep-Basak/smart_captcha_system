import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: {
    information: [],
  },
  reducers: {
    addUserInformation(state, action) {
      state.information.push(action.payload); 
    },
  },
});

export const { addUserInformation } = userSlice.actions;
export default userSlice.reducer;

