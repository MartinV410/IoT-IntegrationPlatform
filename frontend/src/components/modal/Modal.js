import {Container} from "react-bootstrap";
import {motion} from "framer-motion";
import Backdrop from "./Backdrop";


const modalAnimations = {
    visible: {
        //opacity: 1,
        scale: 1,
        transition: {
            duration: 0.3,
        }
    },
    hidden: {
        //opacity: 0,
        scale: 0.2,
    },
    exit: {
        opacity: 0,
//        transition: {
//            duration: 0.4,
//        }
         scale: 0.3,
         transition: {
             duration: 0.3,
         }
    }
};

export default function Modal(props) {

    return(
        <Backdrop onClick={() => props.setShow(false)}>
            <Container className={"modal_container"}>
                <motion.div variants={modalAnimations} initial={"hidden"} animate={"visible"} exit={"exit"} onClick={(e) => e.stopPropagation()}>
                    {props.children}
                </motion.div>
            </Container>
        </Backdrop>
    )
}
