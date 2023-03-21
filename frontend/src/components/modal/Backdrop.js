import { motion } from "framer-motion";

const Backdrop = ({ children, onClick }) =>{
    return(
        <motion.div className={"backdrop"} onClick={onClick} initial={{opacity: 0}} animate={{opacity: 1, transition: {duration: 0.3}}} exit={{opacity: 0, transition: {duration: 0.4}}}>
            {children}
        </motion.div>
    )

};

export default Backdrop;