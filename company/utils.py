from django.views.generic import ListView

from company.forms import NameSearchForm


class SearchMixin(ListView):
    class_name = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = NameSearchForm(
            initial={
                "name": name
            }
        )

        return context

    def get_queryset(self):
        form = NameSearchForm(self.request.GET)
        queryset = self.class_name.objects.all()

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset
