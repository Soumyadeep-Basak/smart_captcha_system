import React from "react";
import bg from "./assets/bg.jpg"
import Link from "next/link";
import {
  MdOutlineContactPage,
  MdOutlineFileCopy,
  MdOutlinePostAdd,
} from "react-icons/md";
import Image from "next/image";

const HomePage= () => {
  const styles = {
    languageOption: {
      marginLeft: "36px",
      cursor: "pointer",
    },
  };

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
  ];

  return (
    <>
      <section
        className="bg-cover bg-no-repeat relative w-full mb-[23px] mt-10 ">
          <img src='./assets/bg.jpg' alt="bg" className="w-full h-full object-cover absolute top-0 inset-0 -z-10" />
        <div className="flex flex-col xl:flex-row lg:flex-row md:flex-row pt-28 pb-5 gap-5 h-full justify-between items-center mx-auto max-w-[1170px] px-8 w-full">
          <div className="text-white">
            <p className="xl:text-[5rem] lg:text-[5rem] md:text-[5rem] text-[4rem] mb-[28px] p-0 pt-[8rem] xl:pt-3 lg:pt-3 md:pt-3 text-left leading-none">
              Welcome to <span className="font-semibold">myAadhaar</span>
            </p>
            <p className="bg-transparent p-0 text-left">
              {" "}
              Click on <b className="font-bold">Register </b>button to explore
              online demographics update service, Aadhaar PVC card ordering
              &amp; tracking, and more value-added services offered by UIDAI.
              Your mobile number is required to be registered with the Aadhaar
              to register.
            </p>
          </div>
          <div className="flex flex-col items-center justify-evenly bg-white rounded-[6px] h-[384px] min-w-[328px] p-4 z-2 ">
            <img
              className="h-[187px] w-[160px]"
              src="https://myaadhaar.uidai.gov.in/static/media/fingerPrint.54859169124a05ba0132.jpg"
              alt="biometrics icon"
            />
            <div className="font-bold w-full">
              <Link href="/register">
                <button
                  type="button"
                  className="bg-gradient-to-r from-[#020d51] to-[#19b0dc] text-white font-bold h-[42px] flex items-center justify-center self-center border-0 rounded transition-all duration-100 cursor-pointer text-base w-full"
                >
                  Register
                </button>
              </Link>
              <p className="text-[0.7rem] font-normal pt-[3px] text-center">
                Register with Aadhaar and OTP
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center justify-center text-white font-bold mt-[-49px] text-center w-screen z-999 xl:flex-row lg:flex-row md:flex-col flex-col xl:text-white lg:text-white pt-14 text-black">
          {languages.map((language) => (
            <div key={language} style={styles.languageOption}>
              {language}
            </div>
          ))}
        </div>
      </section>

      <section className="bg-white shadow-[0_8px_6px_-6px_rgba(50,50,93,0.25)] mb-7 pb-1 pt-0">
        <div className="flex justify-center items-center text-left text-[1rem] font-bold px-4 pb-4 xl:flex-row lg:flex-row md:flex-row flex-col">
          <span className="flex items-center gap-1 text-[calc(1rem+2px)]">
            <MdOutlineContactPage size={25} />
            <Link
              href="https://uidai.gov.in/images/Aadhaar_Enrolment__and__Update__-__English.pdf"
              target="_blank"
              rel="noreferrer"
              className="border-r border-gray-300 ml-1 mr-2 pr-2 align-middle text-inherit cursor-pointer no-underline"
            >
              Aadhaar Enrolment &amp; Update Charges
            </Link>
          </span>
          <span className="flex items-center gap-1 text-[calc(1rem+2px)]">
            <MdOutlinePostAdd size={25} />
            <Link
              href="https://uidai.gov.in/en/my-aadhaar/downloads/enrolment-and-update-forms.html"
              target="_blank"
              rel="noreferrer"
              className="border-r border-gray-300 ml-1 mr-2 pr-2 align-middle text-inherit cursor-pointer no-underline"
            >
              Enrolment &amp; Update Forms
            </Link>
          </span>

          <span className="flex items-center gap-1 text-[calc(1rem+2px)]">
            <MdOutlineFileCopy size={25} />
            <Link
              href="https://uidai.gov.in/images/commdoc/List_of_Supporting_Document_for_Aadhaar_Enrolment_and_Update.pdf"
              target="_blank"
              rel="noreferrer"
              className="border-r border-gray-300 ml-1 mr-2 pr-2 align-middle text-inherit cursor-pointer no-underline"
            >
              List of Supporting Documents for Aadhaar Enrolment &amp; Update
            </Link>
          </span>
        </div>
      </section>
      <p className="text-center text-base font-bold px-4 pb-4">
        Services which require mobile number to be registered with Aadhaar
      </p>
      <p className="text-center px-4 pb-4">
        Please Visit Official UIDAI website:{" "}
        <Link
          className="text-blue-600"
          href="https://myaadhaar.uidai.gov.in/en_IN"
        >
          https://myaadhaar.uidai.gov.in/en_IN
        </Link>
      </p>
    </>
  );
};

export default HomePage;