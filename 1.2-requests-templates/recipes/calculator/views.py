from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
def recipe_view(request, recipe_name):
    context = {'recipe': {}}
    if recipe_name not in DATA:
        return render(request, 'calculator/index.html', context)
    recipe = DATA[recipe_name]
    servings = int(request.GET.get('servings', 1))
    scaled_recipe ={}
    for ingredient, amount in recipe.items():
        scaled_recipe[ingredient] = amount * servings

    context = {
        'recipe': scaled_recipe
    }

    return render(request, 'calculator/index.html', context)

def home_view(request):
    recipes_list = list(DATA.keys())
    context = {
        'message': 'Выберите рецепт:',
        'recipes': recipes_list
    }
    return render(request, 'calculator/index.html', context)
