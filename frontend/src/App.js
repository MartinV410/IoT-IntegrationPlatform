import React from "react";
import {BrowserRouter} from "react-router-dom";
import Sidebar from "./components/Sidebar";
import "bootstrap/dist/css/bootstrap.min.css";
import "./main.css"
import 'react-loading-skeleton/dist/skeleton.css'
import ProtocolPage from "./components/pages/ProtocolPage";
import RoutesAll from "./RoutesAll";
import {SkeletonTheme} from "react-loading-skeleton";

function App() {
  return (
    <div className="App">
        <SkeletonTheme baseColor="#202020" highlightColor="#444">
          <BrowserRouter>
                <Sidebar>
                    <RoutesAll />
                </Sidebar>
          </BrowserRouter>
        </SkeletonTheme>
    </div>
  );
}

export default App;
