import {Col, Container, Row} from "react-bootstrap";
import {useEffect, useState} from "react";
import {client} from "../../api/client";


export default function BloodSaturation() {

    const [saturation, setSaturation] = useState({"red": 0, "ir": 0})

    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                const response = await client.post("max30102/", {"read_fifo": {}})
                setSaturation({"red": response.data.data["red"], "ir": response.data.data["ir"]})
            } catch (err) {
                // console.log(err)
                // setProtocolInfo({})
            }
        }, 5000)

        return() => clearInterval(interval)

    }, [])


    return (
        <Container className={""}>
            <Row className={"justify-content-center align-items-center min-vh-100"}>
                <Col xs={3} className={"card-gray text-center py-2 me-2"}>
                    <p className={"text-muted"}><strong>LED</strong></p>
                    <span className={"card-text-big"}><strong>{saturation.red}</strong></span>
                </Col>
                <Col xs={3} className={"card-gray text-center py-2"}>
                    <p className={"text-muted"}><strong>IR</strong></p>
                    <span className={"card-text-big"}><strong>{saturation.ir}</strong></span>
                </Col>
            </Row>
        </Container>
    )

}
