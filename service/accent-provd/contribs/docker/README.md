To run provd in a docker please run it like :

    docker run -p 69:69/udp -p 8666:8666 -p 8667:8667 -v /config/provd/:/etc/accent-provd/ -it accent-provd bash

and launch the accent-provd

    twistd -no -r epoll accent-provd -s -v

or

    docker run --name accent-provd -d -p 69:69/udp -p 8666:8666 -p 8667:8667 -v /config/provd/:/etc/accent-provd/ -t accent-provd
