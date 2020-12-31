import isodate
from recipe import Recipe

class RecipeTrivial(Recipe):
    # This function will find the informtion needed (like ingredients and
    # instructions) in the json data.
    def parse(self, data):
        # self.recipe_ingredients = []
        # self.recipe_instructions = []

        self.name = data.get("name", "unknown")
        self.author = self._parse_author(data.get("author"))
        self.category = data.get("recipeCategory", "unknown")
        self.description = data.get("description", "")
        self.yeild = data.get("recipeYeild", 0)
        self.prep_time = self._parse_duration(data.get("prepTime", "PT0M"))
        self.cook_time = self._parse_duration(data.get("cookTime", "PT0M"))
        self.image = self._parse_images(data.get("image"))
        self.instructions = self._parse_instructions(data.get("recipeInstructions"))
        self.ingredients = data.get("recipeIngredient", [])
        return self

    # This function will get the author name depending if it is a person or an
    # organization.
    @staticmethod
    def _parse_author(author):
        if author.get("@type") == "Person":
            return author.get("name")
        elif author.get("@type") == "Organization":
            return author.get("legalName")
        else:
            return None

    # This function will parse the duration from the ISO 8601 format to a
    # number of minutes. parse_duration return a timedelta which the number of
    # seconds is taken and divided by 60 to have a number of minutes
    @staticmethod
    def _parse_duration(duration):
        isodate.parse_duration(duration).seconds // 60

    # The function will check if multiple image's urls are given (in a list) or
    # only one image url is given (directly a str)
    @staticmethod
    def _parse_images(images):
        if isinstance(images, list):
            return images[0]
        else:
            return images

    # This function will take a list of steps or sections and will transform it
    # into a list of section(s) with steps inside them. Each section is an
    # element in the sections list. A section is a dictionnary with 2 keys: a
    # name and a list of steps. If there is no name for a section, the section
    # name will be empty ("").
    @staticmethod
    def _parse_instructions(steps_sections):
        sections = []
        global_section_index = None
        for step_section in steps_sections:
            if step_section.get("@type") == "HowToStep":
                if global_section_index == None:
                    global_section_index = len(sections)
                    sections.append({"steps":[], "name":""})
                sections[global_section_index]["steps"].append(step_section.get("text", ""))

            elif step_section.get("@type") == "HowToSection":
                steps = []
                for step in step_section.get("itemListElement"):
                    steps.append(step.get("text", ""))
                sections.append({"steps":steps, "name":step_section.get("name", "unknown")})

        return sections

