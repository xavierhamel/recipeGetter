# Recipe Collector
This library will try to scrape recipe websites and get the information of the recipe. This work on a majority of websites. Give an url to the scraper and get back an instance of the `Recipe()` class with all the information about the recipe (if it was found).


## Usage
### Install the library
```
pip install recipe-collector
```

### Scrape the recipe
```python
recipe = RecipeScraper(url)
infos = recipe.scrape()
# Informations available for the recipe
infos.name # The name of the recipe
infos.author # The name of the author of the recipe
infos.description # Description of the recipe
infos.yeild # Number of yeild that the recipe give
infos.category # The category of the recipe
infos.ingredients # Ingredients used in the recipe
infos.instructions # Instructions used in the recipe
infos.prep_time # Preping time of the recipe
infos.cook_time # Cooking time of the recipe
infos.image # A link to an image of the recipe
```

Some informations may not be present if the scraper was not succesful to find it or was not present on the website.



