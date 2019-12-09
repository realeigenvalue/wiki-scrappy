# wiki-scrappy

A wikipedia web scrapper for movies and actors using scrapy and BeautifulSoup.  A python REST API for data generated from the web scraper using Flask.  A data visualization graph using NetworkX.

![Application Image1](wiki-scrappy-graph.png)
![Application Image2](wiki-scrappy-trends.png)

## Building

Prerequisites
- Python 2.7
- pip

```bash
sudo apt-get install python-tk
pip install Scrapy
pip install networkx
pip install beautifulsoup4
pip install Flask
pip install numpy
pip install matplotlib
pip install astroid
git clone https://github.com/realeigenvalue/wiki-scrappy.git
cd wiki-scrappy
python run_wiki-scrappy.py #runs the web scrapper
python generate_graph.py #generates graph visualization
python start_web_app.py #starts the python web app @ http://127.0.0.1:5000/
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
GNU GPLv3
