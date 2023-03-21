import React, {useEffect, useState} from "react";
import {Row, Col, Button, Tooltip, OverlayTrigger} from "react-bootstrap"
import {JsonViewer} from "@textea/json-viewer";
import {getProtocolColor} from "../../utils";


const example = {
  string: 'this is a test string',
  integer: 42,
  array: [1, 2, 3, 'test', NaN],
  float: 3.14159,
  undefined,
  object: {
    'first-child': true,
    'second-child': false,
    'last-child': null,
  },
  string_number: '1234',
  date: new Date(),
};


const stripAction = (action) => {
    let stripped = {}

    if(action.name) {
        stripped[action.name] = {}
        if(action.allowed_args) {
            Object.keys(action.allowed_args).map((key, index) => {
                const data = action.allowed_args[key].data
                if (data) {
                    stripped[action.name][key] = data
                }
            })
        }
        return stripped
    }

    return action
}


const stripResponse = (response) => {
    const wanted_fields = ["protocol", "passed", "data", "message", "error"]
    let stripped = {}
    Object.keys(response).map((key, index) => {
        if(wanted_fields.some((wanted) => wanted === key)) {
            stripped[key] = response[key]
        }
    })
    return stripped
}

const formatDate = (date) => {
   const date_obj = new Date(date)
    return `${String(date_obj.getHours()).padStart(2, '0')}:${String(date_obj.getMinutes()).padStart(2, '0')}:${String(date_obj.getSeconds()).padStart(2, '0')} ${String(date_obj.getDate()).padStart(2, '0')}.${String(date_obj.getMonth()).padStart(2, '0')}.${date_obj.getFullYear()}`

}

const Response = ({message}) => {
    const [selectedField, setSelectedField] = useState("response")
    const [selectedData, setSelectedData] = useState()

    useEffect(() => {
        setSelectedData(selectData(selectedField))
    }, [selectedField])

    const selectData = () => {
        switch (selectedField) {
            case "response":
                return stripResponse(message).data
            case "action":
                return stripAction(message.action)
            case "full_response":
                return stripResponse(message)
            default:
                return stripResponse(message)
        }
    }

    return(
        <div className={"card-gray p-4 h-100"}>
            <Row className={"w-100"}>
                <Col xs={12} className={"align-items-center align-content-center d-flex"}>
                    <span className={"response-title align-middle"}><strong>Response</strong></span>
                    <div className={`message-box ${message.passed ? "status-success" : "status-error"} align-middle ms-3 ps-3 pe-4`}>
                        <span className={`response-text-big`}><strong>{message.passed ? "OK" : "ERR"}</strong></span>
                    </div>
                    <div className={`message-box ${getProtocolColor(message.protocol)} align-middle ms-2 ps-3 pe-4`}>
                        <span className={"response-text-big "}><strong>{message.protocol}</strong></span>
                    </div>
                    <div className={"message-box message-box-default align-middle ms-2 ps-3 pe-4"}>
                        <span className={"response-text-big"}><strong>{message.action.name}</strong></span>
                    </div>
                    <div className={"justify-se d-inline-flex align-middle ms-auto"}>
                        {message.response_date && message.request_date &&
                            <span className={"text-muted"}><strong>{message.response_date - message.request_date} ms</strong></span>
                        }
                    </div>
                </Col>
                <Col xs={12} className={"position-relative mt-2"}>
                    <div className={"line"}></div>
                </Col>
            </Row>
            <Row className={"mt-3 w-100"}>
                <Col xs={6} >
                    <span>{message.message}</span> <br/>
                    <span className={"text-danger"}>{message.error && message.error}</span>
                </Col>
                <Col xs={6} className={"position-relative"}>
                    <div className={"line-vertical"}></div>
                    <Row className={"ms-2"}>
                        <Col xs={12}>
                            {message.request_date &&
                            <>
                                <span className={"text-muted"}>response_start</span>
                                <span className={"float-end"}><strong>{formatDate(message.request_date)}</strong></span>
                            </>
                            }

                        </Col>
                    </Row>
                    <Row className={"ms-2"}>
                        <Col xs={12}>
                            <span className={"text-muted"}>response_end</span>
                            <span className={"float-end"}><strong>{formatDate(message.response_date)}</strong></span>
                        </Col>
                    </Row>
                    <Row className={"ms-2"}>
                        <Col xs={12}>
                            {message.http_status &&
                            <>
                                <span className={"text-muted"}>http_status</span>
                                <span className={"float-end"}><strong>{message.http_status}</strong></span>
                            </>
                            }

                        </Col>
                    </Row>
                    <Row className={"ms-2"}>
                        <Col xs={12}>
                            {message.http_status_text &&
                            <>
                                <span className={"text-muted"}>http_text</span>
                                <span className={"float-end"}><strong>{message.http_status_text}</strong></span>
                            </>
                            }

                        </Col>
                    </Row>
                </Col>
            </Row>
            <Row className={"mt-5"}>
                <Col xs={12}>
                    <Button variant={"secondary"} className={""} onClick={() => setSelectedField("response")}><strong>response</strong></Button>
                    <Button variant={"secondary"} className={"ms-1"} onClick={() => setSelectedField("action")}><strong>action</strong></Button>
                    <Button variant={"secondary"} className={"ms-1"} onClick={() => setSelectedField("full_response")}><strong>full response</strong></Button>
                </Col>
                <Col xs={12} >
                    <JsonViewer rootName={false} value={selectedData} theme="dark" defaultInspectDepth={1} />
                </Col>
            </Row>
        </div>
    )
}


export default Response