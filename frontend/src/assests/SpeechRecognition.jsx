import React from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { useState, useEffect } from "react";
import FlowDiagram from "./FlowDiagram";
import emailjs from "@emailjs/browser";
import { motion } from "framer-motion";

const Dictaphone = () => {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  const [currentStep, setCurrentStep] = useState(0);
  const [graph, setGraph] = useState([]);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep((prevStep) =>
        prevStep < graph.length - 1 ? prevStep + 1 : prevStep
      );
    }, 2000);

    return () => clearInterval(timer); // cleanup on unmount
  }, [graph]);

  const [isAutomating, setIsAutomating] = useState(false);
  const [reqType, setReqType] = useState(0);

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  const abort = async () => {
    const abortResponse = await fetch("http://0.0.0.0:8000/abort");
    const abortReply = await abortResponse.json();
    console.log(abortReply);
    setIsAutomating(!isAutomating);
    resetTranscript();
  };

  const handleRecordSubmit = async () => {
    SpeechRecognition.stopListening();
    setIsAutomating(true);
    console.log(transcript);

    try {
      const response = await fetch("http://0.0.0.0:8000/transcript", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: transcript }),
      });

      if (!response.ok) {
        console.log(response);
        throw new Error("Network response was not ok");
      }

      const data = await response.json(); // Parse response body as JSON
      setReqType(data.req);
      if (data.req == 1) {
        console.log("json : ", data.jsonres);
        console.log(data.jsonres.email);
        console.log(data.jsonres.body);
        console.log(data.jsonres.subject);
        console.log(data.jsonres.sender_name);
        console.log(data.jsonres.receiver_name);
        const jsonData = JSON.parse(data.jsonres);
        console.log(jsonData.email);
        console.log(jsonData.body);
        console.log(jsonData.subject);
        console.log(jsonData.sender_name);
        console.log(jsonData.receiver_name);

        setGraph(JSON.parse(data.steps))

        emailjs
          .send(
            "service_3jzzrvd",
            "template_8omipe5",
            {
              to_name: jsonData.receiver_name,
              message: jsonData.body,
              from_name: jsonData.sender_name,
              subject: jsonData.subject,
              reciever_email: jsonData.email,
            },
            {
              publicKey: "T-uXJUetQw84JsASr",
            }
          )
          .then(
            () => {
              console.log("SUCCESS!");
            },
            (error) => {
              console.log("FAILED...", error.text);
            }
          );
        //     console.log("json : ",data.jsonres)
        //     console.log(data.jsonres.email)
        //     console.log(data.jsonres.body)
        //     console.log(data.jsonres.subject)
        //     console.log(data.jsonres.sender_name)
        //     console.log(data.jsonres.receiver_name)

        //     emailjs.send("service_3jzzrvd","template_8omipe5",{
        //         to_name: data.jsonres.receiver_name,
        //         message: data.jsonres.body,
        //         from_name: data.jsonres.sender_name,
        //         subject: data.jsonres.subject,
        //         reciever_email: data.jsonres.email,
        //         },{
        //     publicKey: 'T-uXJUetQw84JsASr',
        //   })
        //   .then(
        //     () => {
        //       console.log('SUCCESS!');
        //     },
        //     (error) => {
        //       console.log('FAILED...', error.text);
        //     },
        //   );
      }
      console.log("Success:", data);
      setIsAutomating(true);
    } catch (error) {
      console.error("Error:", error);
      setIsAutomating(false);
    }
  };

  return (
    <div className="text-center flex flex-col">
      {!isAutomating ? (
        <div>
          <div className="flex justify-center text-center">
            {listening ? (
              <button
                className="flex justify-center rounded-full"
                onClick={SpeechRecognition.stopListening}
              >
                <svg
                  className="bg-red-700 hover:bg-red-500 rounded-full p-8
                  animate-pulse"
                  height="200px"
                  width="200px"
                  version="1.1"
                  id="_x32_"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 512 512"
                  fill="#000000"
                  transform="rotate(0)"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    {" "}
                    <style type="text/css">
                      {" "}
                      {`.st0{fill:#eeeded;}`}{" "}
                    </style>{" "}
                    <g>
                      {" "}
                      <path
                        class="st0"
                        d="M383.788,206.98v51.113c-0.013,35.266-14.301,67.108-37.475,90.318 c-23.212,23.176-55.042,37.464-90.307,37.464c-35.267,0-67.108-14.288-90.32-37.464c-23.174-23.211-37.462-55.052-37.474-90.318 V206.98H90.503v51.113c0.036style3,64.21,154.935,146.649,164.337V512h37.709v-89.57c82.426-9.402,146.599-79.407,146.636-164.337 V206.98H383.788z"
                      ></path>{" "}
                      <path
                        class="st0"
                        d="M256.006,344.41c47.589,0,86.305-38.728,86.305-86.318V86.318C342.311,38.728,303.596,0,256.006,0 c-47.59,0-86.318,38.728-86.318,86.318v171.775C169.688,305.682,208.416,344.41,256.006,344.41z"
                      ></path>{" "}
                    </g>{" "}
                  </g>
                </svg>
              </button>
            ) : (
              <button
                className="flex rounded-full justify-center"
                onClick={() => {
                  SpeechRecognition.startListening({ continuous: true });
                }}
              >
                <svg
                  className="bg-blue-400 transition-transform hover:bg-blue-300  rounded-full p-8"
                  height="200px"
                  width="200px"
                  version="1.1"
                  id="_x32_"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 512 512"
                  fill="#000000"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    {" "}
                    <style type="text/css">
                      {" "}
                      {`.st0{fill:#eeeded;}`}{" "}
                    </style>{" "}
                    <g>
                      {" "}
                      <path
                        class="st0"
                        d="M383.788,206.98v51.113c-0.013,35.266-14.301,67.108-37.475,90.318 c-23.212,23.176-55.042,37.464-90.307,37.464c-35.267,0-67.108-14.288-90.32-37.464c-23.174-23.211-37.462-55.052-37.474-90.318 V206.98H90.503v51.113c0.036,84.93,64.21,154.935,146.649,164.337V512h37.709v-89.57c82.426-9.402,146.599-79.407,146.636-164.337 V206.98H383.788z"
                      ></path>{" "}
                      <path
                        class="st0"
                        d="M256.006,344.41c47.589,0,86.305-38.728,86.305-86.318V86.318C342.311,38.728,303.596,0,256.006,0 c-47.59,0-86.318,38.728-86.318,86.318v171.775C169.688,305.682,208.416,344.41,256.006,344.41z"
                      ></path>{" "}
                    </g>{" "}
                  </g>
                </svg>
              </button>
            )}
          </div>
          <h3 className="p-10 mx-auto flex-1 text-center text-xl font-mono font-semibold">
            {transcript}
            {listening ? <span>..</span> : <span></span>}
          </h3>
          {transcript !== "" && (
            <button
              onClick={handleRecordSubmit}
              className="bg-blue-400 text-xl font-bold hover:bg-[#eeeded] transition-transform hover:text-blue-400 rounded-lg m-5 p-4 w-fit h-fit mx-auto px-6"
            >
              Automate
            </button>
          )}
        </div>
      ) : (
        <div className="bg-black min-h-screen w-screen absolute top-0 left-0 ">
          <div className="flex justify-end items-center p-2 cursor-pointer">
            <button onClick={abort} className="h-30 w-30 flex items-center">
              <h3 className="font-mono font-semibold text-xl animate-none">
                Stop Automation
              </h3>
              <img
                className="h-10 w-10 p-2 hover:animate-spin"
                src="images/cross.svg"
              />
            </button>
          </div>
          {reqType === 0 && (
            <div>
              <div className="flex justify-center items-center">
                <h1 className="text-4xl font-bold text-white">
                  Automating your commands
                </h1>
                <img
                  className="h-16 w-16 p-2 animate-spin"
                  src="images/loadingAutomate.svg"
                />
              </div>
            </div>
          )}
          {reqType === 1 && <div>mail commands automation</div>}
          {graph[0]==!null && (<div className="flex text-center flex-col overflow-y-auto">
            {graph.slice(0, currentStep + 1).map((step, index) => (
              <div
                className="flex flex-col justify-center items-center"
                key={index}
              >
                <motion.div
                  className="mx-auto bg-gradient-to-br from-pink-500 to-pink-600 text-2xl font-mono font-semibold rounded-lg flex justify-center items-center px-10 py-8"
                  initial={{ scale: 0 }}
                  animate={{ rotate: 360, scale: 1 }}
                  transition={{
                    type: "spring",
                    stiffness: 260,
                    damping: 20,
                  }}
                >
                  {step}
                </motion.div>
                {index < currentStep && (
                  <motion.div className="h-20 w-20">
                    <img src="images/downArrow.svg" alt="down-arrow" />
                  </motion.div>
                )}
              </div>
            ))}
          </div>)}
        </div>
      )}
    </div>
  );
};
export default Dictaphone;
