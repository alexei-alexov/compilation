#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This script contains."""
import sys
import os



def main():
    """Main script part"""
    source_path = (input("Enter, please path to source files: ") or "src")
    with open(os.path.join(source_path, "source.py")) as source_file:
        for c in iter(lambda: source_file.read(1), None):
            print c


if __name__ == "__main__":
    main()