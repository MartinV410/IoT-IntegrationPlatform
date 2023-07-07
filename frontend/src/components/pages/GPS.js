import {Col, Container, Row} from "react-bootstrap";
import {useEffect, useState} from "react";
import {client} from "../../api/client";


export default function GPS() {

    const [position, setPosition] = useState({"lat": 0, "lng": 0})

    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                const response = await client.post("neo/", {"get_position": {}})
                setPosition({"lat": response.data.data["lat"], "lng": response.data.data["lng"]})
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
                    <p className={"text-muted"}><strong>LATITUDE</strong></p>
                    <span className={"card-text-big"}><strong>{Math.round(position.lat * 100) / 100}</strong></span>
                </Col>
                <Col xs={3} className={"card-gray text-center py-2"}>
                    <p className={"text-muted"}><strong>LONGITUDE</strong></p>
                    <span className={"card-text-big"}><strong>{Math.round(position.lng * 100) / 100}</strong></span>
                </Col>
            </Row>
        </Container>
    )

}
