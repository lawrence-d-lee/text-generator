# Estate Agent Text Generator

This is a Plotly Dash app built with TensorFlow, which uses an LSTM (a type of neural network) to generate text in the style of estate agents.

### Run the app using Docker
Check Docker is installed (https://docs.docker.com/engine/install/) and running.
```
docker pull ghcr.io/lawrence-d-lee/text_generator:latest
docker run -p 8050:8050 ghcr.io/lawrence-d-lee/text_generator:latest
```
Then, either click on the location given on the terminal or visit http://localhost:8050/ to view the app.
