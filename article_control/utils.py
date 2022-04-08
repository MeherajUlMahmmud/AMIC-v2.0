from .models import *


def increaseViewCount(user, article):
    if article.article_totalViewCount is None:
        article.article_totalViewCount = 0
    article.article_totalViewCount = article.article_totalViewCount + 1
    article.save()

    return


def get_categories():
    return ArticleCategoryModel.objects.all()
