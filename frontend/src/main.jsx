import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import "nprogress/nprogress.css";
import { AuthProvider } from "./context/AuthContext";

const style = document.createElement("style");

style.innerHTML = `
#nprogress .bar {
  background: #d97706;
  height: 3px;
}

#nprogress .peg {
  box-shadow: 0 0 10px #d97706, 0 0 5px #d97706;
}

#nprogress .spinner {
  display: none;
}
`;

document.head.appendChild(style);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);