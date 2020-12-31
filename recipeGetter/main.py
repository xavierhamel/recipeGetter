# A scraper that, given an url, can parse the page and detect the ingredients
# and instructions in a page. It return the ingredients and instructions in a
# list and the informations about the recipe in a dictionnary (?)
#
# Easy case :
# To find the data we must first scrape the page for a script tag with the type
# "application/ld+json". This is a tag that is used by google to parse the data
# of recipes. If a recipe website wants to show their recipe in an enhance
# result, they must use this, therefore about 75% of cooking website use this.
#
# Hard case :
# The other 25% will be parsed in a different way where the arbitrary HTML will
# be analyzed. The technique is described more in depth in recipe_complex.py

import requests
import json
from bs4 import BeautifulSoup
from recipeGetter.recipe_trivial import RecipeTrivial
from recipeGetter.recipe_complex import RecipeComplex
from recipeGetter.recipe import Recipe

class RecipeScraper:
    def __init__(self, url):
        self.url = url
        self.content = None
        self.html = None
        self.error = None
        self.trivial_content = None
        self.recipe = None

    def scrape(self):
        self._scrape_content()
        if self.error == None:
            self.html = BeautifulSoup(self.content, 'html.parser')
            # If the case is not trivial, this function will automatically try
            # to find information based on the arbitrary HTML and return a
            # "RecipeComplex" instead of a "RecipeTrivial" instance
            self.recipe = self._find_trivial_case()
            return self.recipe
        return Recipe()
        #return self.error

    # This function will scrape the website specified by the url given when the
    # class was instanciated and put the content of the response in
    # "self.content". If an error occur, bubble up the error
    def _scrape_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.content = response.content
        except requests.exceptions.RequestException as err:
            self.error = err

    # This function will first find if the current website is using putting
    # it's recipe in the metadata (in a script tag with the type
    # application/ld+json). If the tag is found, the data will be parsed, if
    # the tag is not found we will have some more work to do.
    def _find_trivial_case(self):
        scripts_tag = self.html.find_all("script", attrs={"type":"application/ld+json"})
        if len(scripts_tag) > 0:
            for script_tag in scripts_tag:
                data = json.loads(script_tag.string)
                # Every recipe that is supported must have a "@type":"Recipe"
                # at the root of the JSON tree
                if "@type" in data.keys() and data["@type"] == "Recipe":
                    self.trivial_content = data
                    break
        if self.trivial_content == None:
            return self._parse_recipe()
        else:
            return self._parse_trivial_case()

           
    def _parse_trivial_case(self):
        return RecipeTrivial().parse(self.trivial_content)

    # This function is called only if the recipe is not in metadata and is
    # therefore not a trivial case. This function has more chance to fail than
    # a trivial case because we try to find the information about the recipe in
    # the complete html page.
    def _parse_recipe(self):
        return RecipeComplex(self.html).parse()

       

recette = RecipeScraper("https://www.ricardocuisine.com/recettes/5335-sauce-a-spaghetti-la-meilleure")
infos = recette.scrape()
print(infos.ingredients)
print(infos.instructions)
