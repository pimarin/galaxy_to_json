#!/usr/bin/env python
import abromics_galaxy_json_extractor


def main():
    """
    Main function wich generate
    the argparse arguments depending of provided tool
    """
    abromics_galaxy_json_extractor.interfaces.generic_cli_interface()


if __name__ == "__main__":
    main()
