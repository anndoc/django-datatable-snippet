from braces.views import JSONResponseMixin, AjaxResponseMixin


class FilterMixin(JSONResponseMixin, AjaxResponseMixin):
    """
    Base class for search and filter for JQuery DataTable plugin
    """
    paginate_by = 100
    filter_data = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get_ajax(self, request, *args, **kwargs):
        self.draw = self.request.GET.get('draw', 1)
        return self.data_management_filter(self.request.GET)

    def get_queryset(self):
        if self.request.is_ajax():
            return super().get_queryset()
        return self.model.objects.none()

    def get_filtered_queryset(self, queryset):
        ordering_field = list(self.form_class.FIELDS.keys())[self.filter_data.get('sort_column') or 1]
        return queryset.order_by('{}{}'.format(self.filter_data.get('sort_asc', ''), ordering_field))

    def data_management_filter(self, data):
        form = self.form_class(data=data)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def paginate_queryset(self, queryset, page_size):
        start, length = self.filter_data.get('start', 0), self.filter_data.get('length', page_size)
        page = int(start / length) + 1 if int(start / length) >= 0 else 1
        self.kwargs[self.page_kwarg] = page
        return super().paginate_queryset(queryset, length)

    def form_valid(self, form):
        self.filter_data = form.cleaned_data
        total_records = self.get_queryset()
        self.object_list = self.get_filtered_queryset(total_records)
        context = self.get_context_data()
        return self.render_json_response({
            'draw': self.draw,
            'recordsTotal': total_records.count(),
            'recordsFiltered': self.object_list.count(),
            'data': self.get_filtered_data(context['object_list'])
        })

    def form_invalid(self, form):
        return self.render_json_response({
            'draw': self.draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'errors': form.errors
        })

    def get_filtered_data(self, object_list):
        """
        Setup results for data table. The blank line need for using `dataTables.responsive.min.js`
        :param object_list: queryset
        :return: a list of dictionary of formatting fields
            [{
                '': '',
                'title': obj.title,
                'type': obj.get_type_display().title(),
                ....................................................
            } for obj in object_list]
        """
        raise NotImplementedError
