import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Welcome from "./Welcome";
import "./index.css";

// Add Poppins font from Google Fonts
const fontLink = document.createElement("link");
fontLink.rel = "stylesheet";
fontLink.href = "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap";
document.head.appendChild(fontLink);

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Welcome />} />
      <Route path="/game" element={<App />} />
    </Routes>
  </BrowserRouter>
);
