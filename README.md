# Recipe Collector
This library will try to scrape recipe websites and get the information of the recipe. This work on a majority of websites. Give an url to the scraper and get back an instance of the `Recipe()` class with all the information about the recipe (if it was found).


## Usage
### Install the library
```
pip install recipeGetter
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

Some informations may not be present if the scraper was not succesful to find it or if the information was not present on the website.

## How it works
### Trivial case
A majority of popular recipe websites put data about the recipe in a `<script type="application/ld+json">` tag. They put it there because Google will improve the searching result if a website use this technique. The data is very easily pared and returned as a `RecipeTrivial()` instance.

### Complex case
When a website is not putting it's data in a `script` tag, the library will search the arbitrary html for the informations. Not all the data is accessible with this technique and only the ingredients, instructions, name of the recipe, description and author will be searched.

## License
[License](https://github.com/xavierhamel/recipeGetter/blob/main/LICENSE)




