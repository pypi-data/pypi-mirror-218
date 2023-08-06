from .onion_server import main

version = __version__ = '0.0.3 Released 07-JULY-2023'

__version__ = ver = version.split()[0]


if __name__ == '__main__':
    # main()
    while True:
        action = main()
        if action != 'reboot':
            break
        