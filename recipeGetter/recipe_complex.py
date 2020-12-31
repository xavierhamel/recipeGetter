from recipe import Recipe

class RecipeComplex(Recipe):
    ingredient_titles = ["ingredients", "ingredient", "ingrédient",
                         "ingrédients", "you will need", 
                         "vous aurez besoins"]
    instruction_titles = ["steps", "directions", "instructions",
                          "step", "direction", "instruction",
                          "étape", "étapes", "préparation",
                          "prép", "prep", "method", "méthode"]
    # TODO: Hints should be splited by language. The language can be found in the meta tag of the page.
    ingredient_hints = ["g", "kg", "tbs", "cups", "cup",
                        "tasses", "tasse", "c. à soupe",
                        "teaspoon", "tablespoon", "cuillère",
                        "1/2", "1/4", "oz", "oil", "huile",
                        "butter", "beurre"]
    instruction_hints = ["mix", "mélanger", "cook", "cuire",
                         "feu", "heat", "moyen-élevé",
                         "medium-high", "season",
                         "ingredients", "ingrédients", "saler"]

    def __init__(self, html):
        self._html = html
        self._section_tag_type = ["h1", "h2", "h3", "h4", "h5", "h6"]
        super().__init__()

    # The class will try to find the recipe informations in arbitrary HTML. For
    # every information we can make a few assumptions. This is not a perfect
    # method but can give good result. Not all data is supported (like prep and
    # cooking time). Also, page in other language than English or French will
    # not give good results.
    def parse(self):
        self.name = self._find_name()
        self.author = self._find_author()
        self.description = self._find_description()
        self.ingredients = self._find_ingredients()
        self.instructions = self._find_instructions()
        return self

    # The function will try to find the name of the recipe. It will first try
    # to find the og:title meta tag. If the tag was not found it will take the
    # title tag as the recipe is generally put in the title of the website.
    def _find_name(self):
        og_title = self._html.find("meta", attrs={"property", "og:title"})
        if not og_title == None:
            return og_title.attrs.get("content", "")
        else:
            return self._html.find("title").string

    def _find_description(self):
        description = self._html.find("meta", attrs={"name", "description"})
        if not description == None:
            return description.attrs.get("content", "")

    def _find_author(self):
        author = self._html.find("meta", attrs={"name", "author"})
        if not author == None:
            return author.attrs.get("content", "")

    # This function will try to find the section where ingredients are placed.
    # If found it will try to get all the ingredients
    def _find_ingredients(self):
        return self._find_section(self.ingredient_titles, self.ingredient_hints, 0, 75)

        
    def _find_instructions(self):
        instructions = self._find_section(self.instruction_titles, self.instruction_hints, 100, 500)
        return [{
            "name":"",
            "instructions":instructions
        }]
    # Every h1 to h6 will be search for a word like ingredient (or
    # instructions) (and variations in differrent languages). If the header
    # (h..) is found, return it. If a header was previously found, (for
    # ingredients) use the same type of header to search for instructions.
    def _find_section_title(self, keywords):
        for tag_type in self._section_tag_type:
            for header in self._html.find_all(tag_type):
                for keyword in keywords:
                    if not header.string == None and header.string.lower() == keyword:
                        self.section_tag_type = [header.name]
                        return header
        return None


    # This function will try to find keywords that are related to ingredients
    # (ml, g, cups, tasse, tbs, etc..) in the child of the given parent.
    # Every time a keyword is found, the immediat parent of the keyword is put
    # inside a list (it's tag and class). The most common tag and class with a
    # keyword will be selected and, with that, all tag with that class in a
    # same level will become ingredients.
    @staticmethod
    def _find_section_list(parent, hints, min_len, max_len):
        matches = []
        for tag in parent.find_all():
            text = tag.string
            if not text == None and len(text) < max_len and len(text) > min_len:
                for word in text.split(" "):
                    for hint in hints:
                        if hint == word:
                            if "class" in tag:
                                matches.append(f"{tag.name}:{tag['class'][0]}")
                            else:
                                # Not the best..
                                matches.append(f"{tag.name}")
        if len(matches) > 0:
            most_frequent = max(set(matches), key = matches.count).split(":")
            if len(most_frequent) == 2:
                return parent.find_all(most_frequent[0], attrs={"class":most_frequent[1]})
            elif len(most_frequent) > 0:
                return parent.find_all(most_frequent[0])
        else:
            return None


    # This function will try to find the list of element in the section
    # (ingredient or instructions) based on the position of the title of the
    # section. If the title of the section is not found, the function will
    # return nothing. If the section list is not found based on the parent of
    # the title, the next parent will be taken, if not found again, the
    # function will stop and nothing will be returned
    def _find_section(self, titles, hints, min_len, max_len):
        section_title = self._find_section_title(titles)
        if not section_title == None:
            section_list = self._find_section_list(section_title.parent, hints, min_len, max_len)
            if section_list == None:
                section_list = self._find_section_list(section_title.parent.parent, hints, min_len, max_len)
            if not section_list == None:
                section_list = list(map(lambda ingredient: ingredient.string,section_list))
                return section_list
        return []
