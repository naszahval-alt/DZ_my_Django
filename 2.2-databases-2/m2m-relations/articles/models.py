from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название тега")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")
    published_at = models.DateTimeField(verbose_name="Дата публикации")
    image = models.ImageField(null=True, blank=True, verbose_name="Изображение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-published_at']


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="scopes")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False, verbose_name="Основной раздел")

    class Meta:
        unique_together = ('article', 'tag')
        ordering = ['-is_main', 'tag__name']
