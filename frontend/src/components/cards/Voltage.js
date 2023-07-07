import {Col, Row} from "react-bootstrap";

export default function Voltage({title, value, unit}) {

    return(
        <Row className={"justify-content-center p-1"}>
            <Col xs={11} className={"text-center card-darkgray py-2"}>
                <span className={"text-muted"}><strong>{title}</strong></span>
                <p className={"m-0 card-text-big"}><strong>{value} {unit}</strong></p>
            </Col>
        </Row>
    )
}