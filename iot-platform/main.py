from protocols.handler_all import HandlerAll
import logging
s21_mac = '80:9F:F5:36:A9:55'


def main():
    handler = HandlerAll()
    handler.start()



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

    


