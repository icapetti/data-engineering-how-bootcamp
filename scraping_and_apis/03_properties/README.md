## Topics covered:

- Logging
- Inspect
- Extract data from a real estate website

## Steps
- Extract data from a real estate website with pagination
- Create a dataframe with the data extracted
- Save the dataframe to a csv file
## Output
- A csv file like the following:
![Output Example](/img/output_example.png)

## Basic logging configuration
```python
# Get de logging object with the app name
log = logging.getLogger(__name__)
# Set the logging level
log.setLevel(logging.DEBUG)
# Set the logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Set logging channel to console
ch = logging.StreamHandler()
# Add the logging format to console channel
ch.setFormatter(formatter)
# Add the output channel to the logger
log.addHandler(ch)
```

In this example we have created a logger object with the name __name__. This is the name of the module.
We set the level and a format. Then, we created a channel. We can have more then one channel like console and a file, with different levels and formats. In this example, we created just one channel, to the console.

- Scraping
Target URL: http://www.vivareal.com.br

## Next steps
- [ ] Extract data from all pages
- [ ] Add city and state options
- [ ] Add loglevel options