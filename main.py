"""
main.py
Entry point for Gym Tracker
"""

from login import LoginApp
from database import Database
import customtkinter as ctk


def initialize():
    # Create database and tables if they don't exist
    Database()


def main():
    ctk.set_appearance_mode("dark")      # Options: "dark", "light", "system"
    ctk.set_default_color_theme("blue")

    initialize()

    LoginApp()


if __name__ == "__main__":
    main()
