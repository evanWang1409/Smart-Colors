from django.db import models
import json

# Create your models here.
class color(models.Model):
    combination = models.TextField() # json of list of hexvalues
    # url = models.CharField(max_length=200)
    def __str__(self):
        return self.combination

    def getColors(self):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(self.combination)

class pic(models.Model):
    GENDER = (
        ('M', 'Men'),
        ('W', 'Women')
    )
    name = models.CharField(default="", max_length=200)
    url = models.TextField(default="", primary_key=True)
    gender = models.CharField(max_length=1, default="M", choices=GENDER)
    colors = models.ForeignKey(color, default="", on_delete=models.CASCADE) # colors within this picture

    def __str__(self):
        return "Name: %s, URL: %s, Gender: %s" % (self.name, self.url, self.gender)

    def __eq__(self, other):
        return self.url == other.url
        
    def getName(self):
        return self.name

    def getURL(self):
        return self.url

    def getGender(self):
        return self.gender

    def getColorSuggestions(self):
        return self.colors.getColors()

class userPhoto(models.Model):
    possibleColor = models.TextField() # json of possible colors
    photo = models.ImageField(upload_to='user')

    def __str__(self):
        return "Name: %s, URL: %s, Gender: %s" % (name, url, gender)

    def displayPhoto(self):
        pass

    def displayColor(self):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(self.possibleColor)