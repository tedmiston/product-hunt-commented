# Product Hunt Commented

A small bit of code to print every comment you've made on Product Hunt.

Because it [doesn't exist in the web app yet](https://twitter.com/rrhoover/status/567549206038978561).

## Setup

1. Create a virtual environment and install dependencies.  I like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) because it does both in one command.

	```
	git clone https://github.com/tedmiston/product-hunt-commented
	cd product-hunt-commented
	mkvirtualenv -a . -r requirements.txt product-hunt-commented
	```

## Quick start

1. Create a developer token in the [Product Hunt API Dashboard](https://www.producthunt.com/v1/oauth/applicationas).

2. Store it in an environment variable.  I use virtualenvwrapper's [postactivate script](http://virtualenvwrapper.readthedocs.org/en/latest/scripts.html).

	```
	export PRODUCT_HUNT_DEV_TOKEN=xxxyourkeyherexxx
	```
	
3. Run it.

	```
	$ python ph.py
	```

	Sample output:

	```
	Comments for Taylor Edmiston #6311 (@kicksopenminds)
	
	1.) on "Puzzly":
	> "Such puzzling. Much selfie.
	
	(Real question: What made you want to build Puzzly?)"
	
	2.) on "Newsly":
	> "I think you nailed the above-the-fold on the signup page: a nice short demo video and a registration that let's me jump straight to dibbing a name right away.  I use a few products like this myself already (Pinboard for articles, Disco for music, _______ for books/other media)."
	
	....
	```

The results will be printed to stdout, and stored locally in a shelve database called `my_comments.db`, which works as a cache.  Subsequent networking calls use ETags to ensure content will only be downloaded if it has changed.
