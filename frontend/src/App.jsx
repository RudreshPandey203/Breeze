
import React from "react";
import Dictaphone from "./assests/SpeechRecognition";
import './index.css';

function App() {

  return (
    <div className="h-screen">
      <header className=" text-white flex text-4xl p-5 font-extrabold font-mono from-neutral-100">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          className="w-10 h-10"
          xmlns="http://www.w3.org/2000/svg"
          stroke="#ffffff"
          transform="matrix(1, 0, 0, 1, 0, 0)rotate(0)"
        >
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g
            id="SVGRepo_tracerCarrier"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke="#CCCCCC"
            stroke-width="0.72"
          ></g>
          <g id="SVGRepo_iconCarrier">
            {" "}
            <path
              d="M3 8H5M7 5.85714V5.5C7 4.11929 8.11929 3 9.5 3C10.8807 3 12 4.11929 12 5.5C12 6.88071 10.8807 8 9.5 8H8"
              stroke="#eeeded"
              stroke-width="1.752"
              stroke-linecap="round"
            ></path>{" "}
            <path
              d="M4 14H5M15 17V17.5C15 19.433 16.567 21 18.5 21C20.433 21 22 19.433 22 17.5C22 15.567 20.433 14 18.5 14H9"
              stroke="#eeeded"
              stroke-width="1.752"
              stroke-linecap="round"
            ></path>{" "}
            <path
              d="M2 11H8M15 8V7.5C15 5.567 16.567 4 18.5 4C20.433 4 22 5.567 22 7.5C22 9.433 20.433 11 18.5 11H12.25"
              stroke="#eeeded"
              stroke-width="1.752"
              stroke-linecap="round"
            ></path>{" "}
          </g>
        </svg>
        <h1 className="px-3">Breeze</h1>
      </header>
      <div className="flex p-5 justify-center">
        <div className="text-2xl text-gray-300 font-mono font-bold text-center">
          <h2 className="p-3">
            <span className="text-blue-300">Your wish, our command!</span>
          </h2>
          <p className="p-3 text-3xl">
            Experience Seamless Automation with Just Your Voice!
          </p>
        </div>
      </div>
      <div className="p-5 flex justify-center">
        {/* <RecorderHooks /> */}
        <Dictaphone/>
      </div>
    </div>
  );
}

export default App;
