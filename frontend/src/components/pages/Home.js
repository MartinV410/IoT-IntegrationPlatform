import React, {useEffect, useState} from "react";
import {Container, Row, Col} from "react-bootstrap";
import ProtocolsState from "../cards/ProtocolsState";
import Config from "../cards/Config";
import Info from "../cards/Info"
import Messages from "../cards/Messages";
import Modal from "../modal/Modal";
import Response from "../cards/Response";
import {AnimatePresence} from "framer-motion";
import {client} from "../../api/client";


const ENDPOINT = "control/"



export default function Home() {

    const [messages, setMessages] = useState([]);
    const [selectedMessage, setSelectedMessage] = useState();
    const [show, setShow] = useState(false);

    const [protoInfo, setProtoInfo] = useState({})
    const [config, setConfig] = useState({})

    useEffect(() => {
        receiveInfo()
        receiveConfig()
    }, [])

    const receiveInfo = async () => {
        try {
            const response = await client.post(ENDPOINT, {"protocols_info": {}})
            setProtoInfo(response.data.data)
        } catch (err) {
            // not in 200 response range
            console.log(err)
        }
    }

    const receiveConfig = async () => {
        try {
            const response = await client.post(ENDPOINT, {"protocols_config": {}})
            setConfig(response.data.data)
        } catch (err) {
            // not in 200 response range
            console.log(err)
        }
    }

    const handleShowMessage = (message) => {
        setSelectedMessage(message)
        setShow(true)
    }

    useEffect(() => {
        messages.map((msg) => {
            if(!msg.sended) {
                sendAction(msg.action, msg.index)
            }
        })

    }, [messages])

    const sendAction = async(action, index) => {
        setMessages(m =>
            m.map((element) => {
                if(element.index === index) {
                    return {
                        ...element,
                        "direction": "to",
                        "sended": true
                    }
                }
                return element
            })
        )

        try {
            const response = await client.post(ENDPOINT, action)
            setMessages(m =>
                m.map((element) => {
                    if(element.index === index) {
                        return {
                            ...element,
                            "response_date": Date.now(),
                            "http_status": response.status,
                            "http_status_text": response.statusText,
                            ...response.data
                        }
                    }
                    return element
                })
            )
            receiveInfo()
            receiveConfig()
        } catch (err) {
            // not in 200 response range
            setMessages(m =>
                m.map((element) => {
                    if(element.index === index) {
                        return {
                            ...element,
                            "response_date": Date.now(),
                            "http_status": err.response?.status,
                            "http_status_text": err.response?.statusText,
                            "passed": false,
                            "message": err.response ? err.response?.statusText : ""
                        }
                    }
                    return element
            }))
        }
    }


    const handleSendAction = (action) => {
        setMessages(prevState => [...prevState, {"protocol": "Control", "request_date": Date.now(), "action": action, "index": messages.length, "sended": false}])
    }

    const saveConfig = (protoIdentifier, dictKey, value) => {
        handleSendAction({"update_config": {"identifier": protoIdentifier, "new_conf": {[dictKey]: value}}})
    }


    const setProtocolPower = async(state, identifier) => {
        let data = {}
        switch (state) {
            case "on":
                data = {
                    "protocol_start": {
                        "identifier": identifier
                    }
                }
                break;
            case "off":
                data = {
                    "protocol_stop": {
                        "identifier": identifier
                    }
                }
                break;
        }

        handleSendAction(data)
    }

    const setAPIPower = async(state, protocol_identifier, api_identifier) => {
        let data = {}
        switch (state) {
            case "on":
                data = {
                    "api_layer_start": {
                        "protocol_identifier": protocol_identifier,
                        "api_identifier": api_identifier
                    }
                }
                break;
            case "off":
                data = {
                    "api_layer_stop": {
                         "protocol_identifier": protocol_identifier,
                        "api_identifier": api_identifier
                    }
                }
                break;
        }
        handleSendAction(data)
    }

    const setProtocolsPower = (state) => {
        let data = {}
        switch (state) {
            case "on":
                data = {
                    "protocols_start": {}
                }
                break;
            case "off":
                data = {
                    "protocols_stop": {}
                }
                break;
        }

        handleSendAction(data)
    }

    const setAPIsPower = (state) => {
        let data = {}
        switch (state) {
            case "on":
                data = {
                    "api_layers_start": {}
                }
                break;
            case "off":
                data = {
                    "api_layers_stop": {}
                }
                break;
        }

        handleSendAction(data)
    }


    return(
        <div>
            <AnimatePresence mode={"wait"} onExitComplete={() => setShow(false)}>
                {show && selectedMessage &&
                    <Modal setShow={setShow}>
                        <Response message={selectedMessage} />
                    </Modal>
                }
            </AnimatePresence>
            <Container className={"justify-content-center"}>
                <Row className={"justify-content-center mt-5"}>
                    <Col lg={5} xl={3}>
                        <Info info={protoInfo} />
                    </Col>
                    <Col lg={7} xl={4} className={"mt-3 mt-lg-0"}>
                        <ProtocolsState protocols_info={protoInfo} setProtocolPower={setProtocolPower} setApiPower={setAPIPower} setProtocolsPower={setProtocolsPower} setAPIsPower={setAPIsPower} setAutostart={saveConfig} />
                    </Col>
                    <Col lg={12} xl={5} className={"mt-3 mt-xl-0"}>
                        <Config config={config} saveConf={saveConfig} />
                    </Col>
                    <Col xs={12} className={"mt-4"} style={{height: "500px"}}>
                        <Messages messages={messages} setMessages={setMessages} selectMessage={handleShowMessage} />
                    </Col>
                </Row>
            </Container>
        </div>
    )
}