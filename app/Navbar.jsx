import React from "react";
import LanguageSelector from "./LanguageSelector";

const Navbar= () => {
  return (
    <>
      <nav className="bg-white fixed top-0 w-screen z-[300]">
        <div className="flex justify-between mx-auto max-w-[1170px] min-h-[65px] px-4 py-1.5">
          <img className="h-12 w-12 " src={"https://raw.githubusercontent.com/Community-Programmer/SIH-1672/main/client/src/assets/satyameva.png"} alt="satyameva" />
          <h1 className="flex items-center justify-center text-[#23527c] font-bold text-[24px]">
            Unique Identification Authority of India
          </h1>
          <img className="h-12 w-12 " src={"https://raw.githubusercontent.com/Community-Programmer/SIH-1672/b663f1f371b248ca5f4f68df9bfc19c8ea632eac/client/src/assets/adhaar.svg"} alt="aadhaar" />
        </div>
        <div className="bg-gradient-to-r from-[#000046] to-[#1cb5e0] p-3 relative w-screen">
          <div className="flex items-center h-full mx-auto max-w-[1170px] px-4">
            <img
              src="https://myaadhaar.uidai.gov.in/static/media/dashboard.21335c2c89af71912adf700d228cbecd.svg"
              alt="Dashboard Icon"
              className="flex items-center justify-center w-[24px] h-[24px] bg-transparent cursor-pointer"
            />
            <div className="flex-1 bg-transparent text-white text-[1.2rem] font-medium ml-2">
              <span>myAadhaar</span>
            </div>
            <div className="flex items-center rounded-sm cursor-pointer h-[24px] p-1.5 w-max">
              <img
                src="https://myaadhaar.uidai.gov.in/static/media/LanguageSelector.dd14b8054218a45a518df6f26aaff418.svg"
                alt="Language Select Icon"
              />
              <LanguageSelector/>
            </div>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;