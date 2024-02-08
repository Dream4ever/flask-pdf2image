# Flask & pdf2image in Docker

This repo provides you with a dockerized pdf2image envrionment supported by Flask.

## Directly run Python script

Just run `python app.py` in terminal, and this application will be available at `http://127.0.0.1:5000/pdf2img`.

## Run in Docker

Cd to this folder and run `docker compose up` in terminal, then visit `http://127.0.0.1:5000/pdf2img`.

## Usage

Click input button to upload one or more PDF files, and wait to save converted JPG files zipped in file `images.zip`, JPG files belonging to each PDF file is in seperate folder named from PDF.

## Contribution

Feel free to commit issue and PR :)
