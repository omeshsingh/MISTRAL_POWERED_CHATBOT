# Mistral AI-based WhatsApp Chatbot

This project implements a WhatsApp chatbot using the Mistral AI model. It leverages the `transformers` library for model interaction and Selenium for automating WhatsApp Web interactions.

## Features

* Sends and receives messages through WhatsApp Web.
* Uses Mistral AI for generating responses to user messages.
* Continuous interaction loop for ongoing chat.

## Requirements

* Python 3.7+
* `transformers`
* `selenium`
* `webdriver_manager`
* `bitsandbytes`
* A Mistral AI API key.
* Chromium or Google Chrome browser.

## Installation

1. Install the necessary libraries:bash !pip install -U bitsandbytes !pip install transformers !pip install selenium !pip install webdriver_manager
2. Install Chromium:bash !apt-get update !apt install chromium-chromedriver

3. Set up Authentication:
 Replace `"YOUR_API_KEY"` in the code with your Mistral AI API key.


## Usage

1. Run the code in Google Colab.
2. Scan the QR code displayed in your browser to connect to WhatsApp Web.
3. The chatbot will start running and respond to incoming messages.

## Limitations

* Requires an active internet connection.
* Limited to the capabilities of Mistral AI
* WhatsApp Web might change its HTML structure, potentially requiring updates to the Selenium-based interactions.

## Disclaimer

This project is for educational and demonstration purposes only. Use at your own risk.
