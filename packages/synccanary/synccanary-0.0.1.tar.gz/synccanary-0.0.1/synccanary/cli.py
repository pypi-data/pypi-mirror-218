"""
The command-line interface for updating canary
"""
import argparse
from .synccanary import updateCanary


def main():
    parser = argparse.ArgumentParser(
        description="A package to publish latest canaries version in frontend"
    )
    updateCanary()

if __name__ == "__main__":
    main()