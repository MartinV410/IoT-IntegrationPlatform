import React, {useEffect, useState} from "react";
import {Col, Row, Tooltip, OverlayTrigger} from "react-bootstrap";

const Info = ({info}) => {

    const [apiRunning, setApiRunning] = useState(0);
    const [apiCount, setApiCount] = useState(0);

    const [protocolsRunning, setProtocolsRunning] = useState(0);
    const [protocolsCount, setProtocolsCount] = useState(0);

    useEffect(() => {
        if(info === undefined || info.length === 0) {
            return;
        }

        let apiRunning = 0;
        let apiCount = 0;
        let protocolsCount = 0;
        let protocolsRunning = 0;
        Object.keys(info).map((key_protocol) => {
            const protocol = info[key_protocol]
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
    }, [info])
    return (
        <div className={"card-gray p-4 h-100"}>
            <div className={"card-title"}>
                <span><strong>Info</strong></span>
            </div>

            <Row className={"mt-3"}>
                <Col xs={12}>
                    <span className={"text-muted"}><strong>Protocols</strong></span>
                    <span className={"float-end"}><strong>{protocolsRunning}/{protocolsCount}</strong></span>
                </Col>
                <Col xs={12}>
                    <span className={"text-muted"}><strong>API layers</strong></span>
                    <span className={"float-end"}><strong>{apiRunning}/{apiCount}</strong></span>
                </Col>
            </Row>
            <Row className={"mt-3"}>
                {info && Object.keys(info).map((key) => {
                    const protocol = info[key]

                    return(
                    <Col xs={12} key={key}>
                        <span className={"text-muted"}><strong>{key}</strong></span>
                        <OverlayTrigger placement="top" delay={{ show: 500, hide: 0 }} overlay={<Tooltip id={"send-action"}>ZMQ port for main communication</Tooltip>}>
                            <span className={"float-end"}><strong>{protocol.config.zmq_port}</strong></span>
                        </OverlayTrigger>
                    </Col>
                    )
                })}
            </Row>
        </div>
    )
}

export default Info