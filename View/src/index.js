import React, { useState } from "react";
import ReactDOM from "react-dom";
import MapChart from "./Mapchart";
import ReactTooltip from "react-tooltip";


function App(){
  const [content, setContent] = useState("");
    return (
      <div>
        <MapChart setTooltipContent={setContent} />
        <ReactTooltip>{content}</ReactTooltip>
      </div>
    );
  
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);