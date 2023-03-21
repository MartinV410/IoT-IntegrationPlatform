import React from "react";
import {Col, Row, Button} from "react-bootstrap";
import {getProtocolIcon} from "../../utils";

const Protocol = ({protocol, text}) => {
    return(
        <div className={"card-gray p-4 h-100"}>
            <Row>
                <Col xs={12} className={"justify-content-center d-flex align-items-center"}>
                    <div className={"card-icon-big d-inline-flex"}>
                        {getProtocolIcon(protocol)}
                    </div>
                    <div className={"d-inline-flex"}>
                        <span style={{paddingLeft: "10px"}} className={"card-text-big"}><strong>{protocol}</strong></span>
                    </div>
                </Col>
                <Col xs={11} className={"my-3 position-relative"}>
                    <div className={"line"}></div>
                </Col>
                <Col xs={12} className={"text-center"}>
                    <span><strong>{text}</strong></span>
                </Col>
                {/*<Row className={"justify-content-center text-center mt-4"}>*/}
                {/*    {shortcuts.map((shortcut) =>*/}
                {/*        // <Col xs={12} md={6} lg={6} className={"mt-2"}>*/}
                {/*            <Button key={shortcut} variant={"secondary mt-2"} style={{width: "auto", marginLeft: "20px"}} onClick={() => choose_action(shortcut)}><strong>{shortcut}</strong></Button>*/}
                {/*        // </Col>*/}
                {/*    )}*/}
                {/*</Row>*/}
            </Row>
        </div>
    )
}

export default Protocol