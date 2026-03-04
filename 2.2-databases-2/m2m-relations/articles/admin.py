from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        main_scopes = 0
        for form in self.forms:
            # Убрали проверку form.is_deleted — оставляем только проверку is_main
            if form.cleaned_data.get('is_main'):
                main_scopes += 1
        if main_scopes != 1:
            raise ValidationError('Должен быть выбран ровно один основной раздел!')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1
    verbose_name = "Тег"
    verbose_name_plural = "Теги (разделы)"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'published_at']
    search_fields = ['title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
