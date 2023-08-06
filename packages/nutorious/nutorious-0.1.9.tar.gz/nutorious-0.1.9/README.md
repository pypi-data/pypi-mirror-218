Nutorious
=========

Nutorious is a command-line tool to track your nutrition in plaintext files. This includes the usual kcal, protein, carbs, fats, but also any other ingredient of your choosing, i.e. sugar, salt, etc. I was inspired by the https://plaintextaccounting.org/, when at some point I wanted to start counting calories and realized that none of the phone apps are flexible/easy-to-use enough for my needs, especially after trying plaintext for accouting. Another inspiration came from [Calorific](https://github.com/peterkeen/calorific) to use simple yaml format for the journal files. The Calorific is a great tool, but I wanted a bit better UX.


### Installation
Nutorious is available in PyPI, so it can be installed the usual way using the `pip` command:
```bash
pip install --upgrade nutorious
```

### Journal
Nutorious is using simple yml files for tracking. The CLI let's you specify the journal directory that will be recursively scanned for all .yml files. The `config.yml`, if present, will be treated as a custom configuration file (see below), other files will be parsed in no particular order and merged together to form a full final journal.

Example can be found in the directory [journal-example](https://github.com/dzmitry-paulenka/nutorious/tree/master/journal-example)

Journal files should have next format:
```yaml
yyyy-mm-dd:
  <food-or-meal-name>:
    - <food-spec-entry-1>
    - <food-spec-entry-2>
```

Example:
```yaml
# using some date in the past to define common food, that doesn't change
1970-07-07:
  # next lines use the simplicity of yaml to specify the food-spec
  
  # proteins
  egg: [ 77.5 kcal, 6.3 prot, 0 carb, 5.3 fat, 50g, countable ]
  eggs: [ 77.5 kcal, 6.3 prot, 0 carb, 5.3 fat, 50g, countable ]
  chicken: [ 115 kcal, 21.2 prot, 0.0 carb, 2.6 fat ]
  roasted-chicken: [ 100 chicken, 75g ]
  salmon: [ 142 kcal, 19.8 prot, 0.0 carb, 6.3 fat ]

  # carbs
  spaget: [ 351 kcal, 14 prot, 70 carb, 1 fat ]
  rice: [ 344 kcal, 6.7 prot, 78.9 carb, 0.7 fat ]
  # ... similar for other common products
  
2023-05-30:
  bread: [ 310 kcal, 10.8 prot, 37.7 carb, 11.6 fat ]

  salad:
    - 300 cabbage
    - 100 carrot
    - 200 pepper
    - 20 oil
    - 2x

  breakfast:
    - 50 bread
    - 50 avocado
    - 1 egg
    - 10 oil
  
  lunch:
    - 1 salad
    - 100 rice
    - 200 roasted-chicken
```

So top level entries are the journaling dates. Second levels are the food name or a meal name. Meal names can be specified in the config, and by default are **breakfast, lunch, snack and dinner**, everything else is considered a custom food item. Meals are treated differently in the reports, but the specification is exactly the same. And third level is the list of food specification entries.


#### Food specificiation
The food/meal specification can include the following items:
* **[amount] [food-name]** - food ingredient. Means that this food item contains this amount of other food/component.
```yaml
- 1 egg
- 100 rice
```
* **countable** - mark this food item as countable. Meaning that referenced amounts of this item in other foods will be computed not on a gramm ratio, but on a number ratio. This is useful for countable items like eggs.
```yaml
  egg: [ 77.5 kcal, 6.3 prot, 5.3 fat, 50g, countable ]
```
* **[amount]x** - mark this food item as countable and specify the base amount of resulting items. I.e. divide all specified ingredients to this many "portions" to compute a 1 base item contents. Usefull for equal portioning of prepared food.
```yaml
  steak:
    - 500 beef
    - 20 oil
    - 20 balsamic
    - 10 salt
    - 2x
```
* **[amount]g** - specify a resulting weight of the food. This can be used for measuring the food after the preparation, when you can't use simple portioning. 
```yaml
  egg-rice:
    - 200 rice
    - 3 eggs
    - 600g # gets bigger after preparation
```

#### Food weight
If weight is not specified explicitly, it uses next heuristic to determine a weight:
* **100g** for the food, that only contains "undefined" references. This is useful for adding numbers directly from labels as they usually go on the base of 100g.
```yaml
  bread: [ 310 kcal, 10.8 prot, 37.7 carb, 11.6 fat ]
```
* **sum of ingredients** for the food, that contains previously defined/weighted ingredients.
```yaml
  # default weight of 1 "salad item" is (300 + 100 + 200 + 20) / 2 = 310
  salad:
    - 300 cabbage
    - 100 carrot
    - 200 pepper
    - 20 oil
    - 2x
```

#### Food registry
After the food is defined it can be referenced on current or any future dates. 
```yaml
2023-03-03:
  egg-rice:
    - 200 rice
    - 3 eggs
    - 600g # gets bigger after preparation
  lunch:
    - 200 egg-rice

2023-03-04:
  lunch:
    - 200 egg-rice # leftovers

2023-03-05:
  lunch:
    - 200 egg-rice # more leftovers
```

If the food is redefined, all future references will use this new version. The idea is that usually you have just one "bread" in your kitchen, but it can have different contents. So once the old one is finished and you bought the new one, you just add it with the same name "bread".
```yaml
2023-03-03:
  bread: [ 200 kcal, 7.6 prot, 42.7 carb, 9 fat ]
  breakfast:
    - 50 bread # 100 kcal 

2023-03-04:
  breakfast:
    - 50 bread # still 100 kcal 

2023-03-05:
  bread: [ 300 kcal, 10.8 prot, 37.7 carb, 11.6 fat ]
  breakfast:
    - 50 bread # 150 kcal 
```

### Usage
```
$ nutorious report --help
Usage: nutorious report [OPTIONS]

  Shows report on a date, closest to specified date.

Options:
  --journal_path, --j DIRECTORY  Path to the journal directory. Default:
                                 current directory.
  --date, --d [%Y-%m-%d]         Date of the report. Default is 'today'.
  --watch, --w                   Show live view of the report and update it,
                                 when journal files change.
  --help                         Show this message and exit.
```

Example usage:

![example-journal](assets/journal-example.png)


### Configuration
If journal directory contains file named `config.yml`, it will be treated as a custom configuration file. This file will be merged on top of the default one to determine the full final configuration.

The default configuration file is [here](https://github.com/dzmitry-paulenka/nutorious/blob/master/src/nutorious/config/default.yml) and looks like this:
```yaml
meals:
  - breakfast
  - lunch
  - snack
  - dinner

ui:
  daily:
    # title on top of the report table, substitutes "{dt}" with the date of the report
    title: Nutrition report on {dt}
    columns:
      # the ingredient name to show in the column
      - data: title
        # title to show in the table header
        title: Title
        # styling, as supported by rich - https://rich.readthedocs.io/en/stable/style.html
        style: cyan
        # justification, 'right' be default
        justify: left
      - data: amount
        title: Amount
        style: green
      - data: kcal
        title: Kcal
        style: blue
      - data: prot
        title: Protein
        style: white
      - data: carb
        title: Carbs
        style: yellow
      - data: fat
        title: Fat
        style: red
```