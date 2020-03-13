# feeder-bot
 This is a tool called **feeder-bot** for automating updates of RSS feeds to your platform (receiver). 

### Quick Start

##### Requirements

``````shell
pip install -r requirements.txt
``````

##### Run [arXiv_twitter.py](arXiv_twitter.py)

``````shell
python arXiv_twitter -r 3600 -q bert+OR+nlp
``````

Where 

``````html
-r REQUEST_INTERVAL sending request to arXiv API every seconds of REQUEST_INTERVAL
-q the query for automatic retreival of latest papers from arxiv
``````

### Support of RSS feeds so far

- [arXiv](https://arxiv.org/)

### Support of receivers so far

- [Twitter](https://twitter.com/home)

### Examples

- How to listen to arXiv based on keywords and post identified updates to Twitter?

#### Updates

- 13/03/2020: Publish the first version of feeder-bot that can listen to updates from arXiv and automatically forward them to Twitter if updates found. You just need to specify the `ARXIV_QUERY` (that is used to the retrieve updates on arXiv) and `REQUEST_INTERVAL `(that refers to the time interval of requesting arXiv) to run the bot !

  