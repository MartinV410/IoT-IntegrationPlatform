import React from "react";
import {useState} from "react";
import {NavLink} from "react-router-dom";
import {AnimatePresence, motion} from "framer-motion";
import { Row, Col } from "react-bootstrap";
import {ROUTES} from "../constants";
import {FaBars} from "react-icons/fa";


const showText = {
    hidden: {
        opacity: 0,
        x: -20,
        transition: {
            duration: 0.3,
        }
    },
    show: {
        opacity: 1,
        x:1,
        transition: {
            duration: 0.6,
        }
    }
}

const showLogo = {
    hidden: {
        opacity: 0,
        x: 30,
        transition: {
            duration: 0.3
        }
    },
    show: {
        opacity: 1,
        x:1,
        transition: {
            duration: 0.5,
            delay: 0.1
        }
    }
}

const Sidebar = ({children}) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggle = () => {
        setIsOpen(!isOpen);
    }

    return(
        <>
            <motion.div className={"sidebar-container"} animate={{width: isOpen ? "220px" : "60px", transition:{duration: 0.5, type:"spring", damping:15}}} initial={false}>
                <Row className={"h-100 flex"}>

                    <Col xs={12} className={"pt-3 text-nowrap"} style={{position: "relative"}}>
                        <AnimatePresence>
                            {isOpen && <motion.span className={"route-logo"} variants={showLogo} initial={"hidden"} animate={"show"} exit={"hidden"}><strong>IoT IP</strong></motion.span>}
                        </AnimatePresence>
                    <FaBars className={"me-3 float-end"} style={{fontSize: "30px"}} onClick={toggle} />

                    </Col>
                    <Col xs={12}>
                        {ROUTES.map((route) =>
                            <NavLink to={route.path} key={route.name} className={({isActive}) => "route-link mt-1 " + (isActive ? "active-link" : "")} onClick={() => setIsOpen(false)}>
                                <span className={"route-icon mx-3"}>{route.icon}</span>
                                <AnimatePresence>
                                    {isOpen && <motion.span className={"route-name"} variants={showText} initial={"hidden"} animate={"show"} exit={"hidden"}><strong>{route.name}</strong></motion.span>}*/}
                                </AnimatePresence>
                            </NavLink>
                        )}
                    </Col>
                    {/*<div className={"align-self-end"}>*/}
                    {/*    {user &&*/}
                    {/*        <div className={"route-link"} onClick={logout}>*/}
                    {/*            <span className={"route-icon mx-3"}><BiLogOut /></span>*/}
                    {/*            <AnimatePresence>*/}
                    {/*                {isOpen && <motion.span className={"route-name"} variants={showText} initial={"hidden"} animate={"show"} exit={"hidden"}><strong>{user.username}</strong></motion.span>}*!/*/}
                    {/*            </AnimatePresence>*/}
                    {/*        </div>*/}
                    {/*    }*/}
                    {/*</div>*/}
                </Row>
            </motion.div>
            <div style={{width: "calc(100% - 60px)", position: "absolute", top: 0, right:0, minHeight: "100vh"}} onClick={(e) => {setIsOpen(false)}} id={"main"}>
                <main className={"h-100"}>
                    {children}
                </main>
            </div>
        </>
    );
}

export default Sidebar