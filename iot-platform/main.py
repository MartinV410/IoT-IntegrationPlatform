from protocols.handler_all import HandlerAll
import logging

def main():
    handler = HandlerAll()
    handler.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

    


