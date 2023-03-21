import {Col, OverlayTrigger, Row, Tooltip} from "react-bootstrap";
import {TbSettingsAutomation} from "react-icons/tb";
import React from "react";


const ProtocolStateRow = ({key_protocol, protocol, setAutostart, setProtocolPower, setApiPower}) => {
    return(
        <Row>
            <Col xs={12} className={"d-flex align-items-center align-content-center"}>
                <span className={"h5"}><strong>{key_protocol}</strong></span>
                <div className={"ms-auto"}>
                        <TbSettingsAutomation className={`icon ${protocol.config["autostart"] ? "text-success" : "text-danger"}`} onClick={() => setAutostart(key_protocol, "autostart", !protocol.config["autostart"])} />
                    <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-action"}>Protocol is currently {protocol.running ? "on" : "off"} (click to turn {protocol.running ? "off" : "on"})</Tooltip>}>
                        <span className={`dot ${protocol.running ? "dot-on" : "dot-off"}`} onClick={() => setProtocolPower(protocol.running ? "off" : "on", key_protocol)}></span>
                    </OverlayTrigger>
                </div>

            </Col>
            {
                Object.keys(protocol["api_layers"]).map((key_api) => {
                    const api_layer = protocol["api_layers"][key_api]
                    return(
                    <Col xs={12} className={"d-flex align-items-center align-content-center position-relative"} key={key_protocol + key_api}>
                        <div className={"ms-2 line-tree"}></div>
                        <span className={"text-muted"}><strong>{key_api}</strong></span>
                        <div className={"ms-auto"}>
                            <TbSettingsAutomation className={`icon ${protocol.config[key_api + "_autostart"] ? "text-success" : "text-danger"}`} onClick={() => setAutostart(key_protocol, key_api + "_autostart", !protocol.config[key_api + "_autostart"])} />
                            <OverlayTrigger delay={{ show: 500, hide: 0 }} placement="top" overlay={<Tooltip id={"send-action"}>API layer is currently {api_layer.running ? "on" : "off"} (click to turn {api_layer.running ? "off" : "on"})</Tooltip>}>
                                <span className={`dot ${api_layer.running ? "dot-on" : "dot-off"}`} onClick={() => setApiPower(api_layer.running ? "off" : "on", key_protocol, key_api)}></span>
                            </OverlayTrigger>
                        </div>
                    </Col>
                    )
                })
            }

        </Row>
    )
}

export default ProtocolStateRow