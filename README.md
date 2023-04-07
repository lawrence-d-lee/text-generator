# NLP-Project

This is a dash app built with TensorFlow, which uses an LSTM (a type of neural network) to generate text in the style of estate agents.

To run the app, clone the repo to your desktop.

### Run the app using Docker (recommended)
```
1. cd NLP-Project
2. docker build . -t dash_app
3. docker run -p 8050:8050 dash_app
```
### Run the app without Docker
```
1. cd NLP-Project
2. python -m venv venv
3. venv\Scripts\activate
4. pip install -r requirements.txt
5. python dash_text_generator
```
Then, either click on the location given on the terminal or visit http://localhost:8050/ to view the app.
