import React, {useEffect, useState} from "react";
import {Col, Row, Button, Tooltip, OverlayTrigger} from "react-bootstrap";
import {AiOutlinePoweroff} from "react-icons/ai";
import {TbSettingsAutomation} from "react-icons/tb";
import ProtocolStateRow from "../rows/ProtocolStateRow";

const ProtocolsState = ({protocols_info, setProtocolPower, setApiPower, setProtocolsPower, setAPIsPower, setAutostart}) => {

    const [apiRunning, setApiRunning] = useState(0);
    const [apiCount, setApiCount] = useState(0);

    const [protocolsRunning, setProtocolsRunning] = useState(0);
    const [protocolsCount, setProtocolsCount] = useState(0);

    useEffect(() => {
        if(protocols_info === undefined || protocols_info.length === 0) {
            return;
        }

        let apiRunning = 0;
        let apiCount = 0;
        let protocolsCount = 0;
        let protocolsRunning = 0;
        Object.keys(protocols_info).map((key_protocol) => {
            const protocol = protocols_info[key_protocol]
            protocolsCount += 1;
            if(protocol.running) {
                protocolsRunning += 1;
            }

            Object.keys(protocol["api_layers"]).map((key_api) => {
                const api = protocol["api_layers"][key_api]
                apiCount += 1;
                if(api.running) {
                    apiRunning += 1;
                }
            })
        })

        setApiCount(apiCount);
        setApiRunning(apiRunning);
        setProtocolsCount(protocolsCount);
        setProtocolsRunning(protocolsRunning);
    }, [protocols_info])

    return (
        <div className={"card-gray p-4 h-100"}>
            <div className={"card-title"}>
                <span><strong>Protocols state</strong></span>
            </div>

            <Row className={"h-100 mt-2"}>
                <Col xs={12}>
                    <Row className={"align-content-center mt-2"} style={{maxHeight: "250px", overflowY: "auto"}}>
                        {protocols_info && Object.keys(protocols_info).map((key_protocol, index) => {
                            const protocol = protocols_info[key_protocol]
                            return(
                            <Col xs={12} className={`bg-gray py-1 ${index > 0 ? "mt-2" : ""}`} style={{borderRadius: "5px"}} key={key_protocol}>
                                <ProtocolStateRow key_protocol={key_protocol} protocol={protocol} setProtocolPower={setProtocolPower} setAutostart={setAutostart} setApiPower={setApiPower}/>
                                {/*<Row>*/}
                                {/*    <Col xs={12} className={"d-flex align-items-center align-content-center"}>*/}
                                {/*        <span className={"h5"}><strong>{key_protocol}</strong></span>*/}
                                {/*        <div className={"ms-auto"}>*/}
                                {/*            <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-action"}>Protocol autostart is {protocol.running ? "on" : "off"} (click to turn {protocol.running ? "off" : "on"})</Tooltip>}>*/}
                                {/*                <TbSettingsAutomation className={`icon ${protocol.config["autostart"] ? "text-success" : "text-danger"}`} onClick={() => setAutostart(key_protocol, "autostart", !protocol.config["autostart"])} />*/}
                                {/*            </OverlayTrigger>*/}
                                {/*            <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-action"}>Protocol is currently {protocol.running ? "on" : "off"} (click to turn {protocol.running ? "off" : "on"})</Tooltip>}>*/}
                                {/*                <span className={`dot ${protocol.running ? "dot-on" : "dot-off"}`} onClick={() => setProtocolPower(protocol.running ? "off" : "on", key_protocol)}></span>*/}
                                {/*            </OverlayTrigger>*/}
                                {/*        </div>*/}

                                {/*    </Col>*/}
                                {/*    {*/}
                                {/*        Object.keys(protocol["api_layers"]).map((key_api) => {*/}
                                {/*            const api_layer = protocol["api_layers"][key_api]*/}
                                {/*            return(*/}
                                {/*            <Col xs={12} className={"d-flex align-items-center align-content-center position-relative"} key={key_protocol + key_api}>*/}
                                {/*                <div className={"ms-2 line-tree"}></div>*/}
                                {/*                <span className={"text-muted"}><strong>{key_api}</strong></span>*/}
                                {/*                <div className={"ms-auto"}>*/}
                                {/*                    <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-action"}>API layer autostart is {api_layer.running ? "on" : "off"} (click to turn {api_layer.running ? "off" : "on"})</Tooltip>}>*/}
                                {/*                        <TbSettingsAutomation className={`icon ${protocol.config[key_api + "_autostart"] ? "text-success" : "text-danger"}`} onClick={() => setAutostart(key_protocol, key_api + "_autostart", !protocol.config[key_api + "_autostart"])} />*/}
                                {/*                    </OverlayTrigger>*/}
                                {/*                    <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-action"}>API layer is currently {api_layer.running ? "on" : "off"} (click to turn {api_layer.running ? "off" : "on"})</Tooltip>}>*/}
                                {/*                        <span className={`dot ${api_layer.running ? "dot-on" : "dot-off"}`} onClick={() => setApiPower(api_layer.running ? "off" : "on", key_protocol, key_api)}></span>*/}
                                {/*                    </OverlayTrigger>*/}
                                {/*                </div>*/}
                                {/*            </Col>*/}
                                {/*            )*/}
                                {/*        })*/}
                                {/*    }*/}

                                {/*</Row>*/}
                            </Col>
                            )
                        })}
                    </Row>
                </Col>


                <Col xs={12} className={"align-self-end"}>
                    <Row className={"mt-4 align-self-end"}>
                        <Col x={6} className={"d-flex"}>
                            <div className={"d-inline-block"}>
                               <div>
                                   <span className={"text-muted small"}><strong>API layers:  {apiRunning}/{apiCount}</strong></span>
                               </div>
                                <div className={"d-flex mt-1"}>
                                    <OverlayTrigger placement="top" delay={{ show: 500, hide: 0 }} overlay={<Tooltip id={"send-action"}>Turn all API layers off</Tooltip>}>
                                        <Button variant={""} className={"button-danger"} onClick={() => setAPIsPower("off")}><AiOutlinePoweroff style={{marginBottom: "3px"}} /></Button>
                                    </OverlayTrigger>
                                    <OverlayTrigger placement="top" delay={{ show: 500, hide: 0 }} overlay={<Tooltip id={"send-action"}>Turn all API layers on</Tooltip>}>
                                        <Button variant={""} className={"button-green ms-auto"} onClick={() => setAPIsPower("on")}><AiOutlinePoweroff style={{marginBottom: "3px"}} /></Button>
                                    </OverlayTrigger>
                                </div>
                            </div>
                        </Col>
                        <Col xs={6} className={"text-end"}>
                            <div className={"d-inline-block"}>
                               <div>
                                   <span className={"text-muted small"}><strong>Protocols:  {protocolsRunning}/{protocolsCount}</strong></span>
                               </div>
                                <div className={"d-flex mt-1"}>
                                    <OverlayTrigger placement="top" delay={{ show: 500, hide: 0 }} overlay={<Tooltip id={"send-action"}>Turn all protocols off</Tooltip>}>
                                        <Button variant={""} className={"button-danger"} onClick={() => setProtocolsPower("off")}><AiOutlinePoweroff style={{marginBottom: "3px"}} /></Button>
                                    </OverlayTrigger>
                                    <OverlayTrigger placement="top" delay={{ show: 500, hide: 0 }} overlay={<Tooltip id={"send-action"}>Turn all protocols on</Tooltip>}>
                                        <Button variant={""} className={"button-green ms-auto"} onClick={() => setProtocolsPower("on")}><AiOutlinePoweroff style={{marginBottom: "3px"}} /></Button>
                                    </OverlayTrigger>
                                </div>
                            </div>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </div>
    )
}

export default ProtocolsState