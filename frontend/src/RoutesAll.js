import React from "react";
import {Route, Routes, useLocation} from "react-router-dom";
import {ROUTES} from "./constants";
import ProtocolPage from "./components/pages/ProtocolPage";
import Home from "./components/pages/Home";


export default function RoutesAll() {
    const location = useLocation();
    return(
        <Routes location={location} key={location.pathname}>
            <Route path={'/'} exact element={ROUTES[0].component} />
            {
                ROUTES.map((route) => {
                    return(
                         // <Route key={route.path} element={route.component}>
                            <Route key={route.path} path={route.path}  element={route.component}/>
                        // </Route>
                    )
                })
            }
        </Routes>
    )
}