# Django JQuery DataTable plugin snippet

### Usage

* Define form class inherited from `BaseFilterForm`

        class TableFilterForm(BaseFilterForm):
            FIELDS = OrderedDict([
                ('', ''),
                ('title', _('Title')),
                ('type', _('Course Type')),
            ])

* Add to `views.py` and override `get_filtered_data` method

        class TableListView(FilterMixin, ListView):
            template_name = 'table_list.html'
            form_class = TableFilterForm
        
            def get_filtered_data(self, object_list):
                return [{
                    '': '',
                    'title': obj.title,
                    'course_type': obj.get_course_type_display().title(),
                } for obj in object_list]
            
* In template add js `jquery.dataTables.min.js`, `dataTables.responsive.min.js` 
and css `jquery.dataTables.min.css`, `responsive.dataTables.min.css`

* Setup DataTable 

        $('table').DataTable( {
            "scrollCollapse": true,
            "bLengthChange": false,
            "scrollY": true,
            "scrollX": false,
            "processing": true,
            "serverSide": true,
            "columns": [
                {"data": "", 'searchable': false, 'orderable': false, "className": "control"},
                {"data": "title"},
                {"data": "type"}
            ],
            fnServerParams: function ( aoData ) {
                if (aoData.order.length) {
                    aoData.sort_column = aoData.order[0]['column'];
                    aoData.sort_asc = aoData.order[0]['dir'] === 'asc' ? '' : '-';
                }
            },
            responsive: {
                details: {
                    type: 'column'
                }
            }
        });
