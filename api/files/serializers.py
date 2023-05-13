from rest_framework import serializers
from core.models import FileInfo


class FileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')

    class Meta:
        model = FileInfo
        fields = [
            'id',
            'file_id',
            'file_name',
            'description',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'file_id', 'file_name', 'owner', 'created_at', 'updated_at', 'updated_by']


# TODO try to use it
# class FileSerializer(serializers.HyperlinkedRelatedField):
#     # We define these as class attributes, so we don't need to pass them as arguments.
#     view_name = 'file-detail'
#     queryset = FileInfo.objects.all()
#
#     def get_url(self, obj, view_name, request, format):
#         print('#########')
#
#         print(obj)
#         print(view_name)
#         # return Response()
#         url_kwargs = {
#             'organization_slug': obj.file_id,
#             'customer_pk': obj.pk
#         }
#         return reverse(view_name, kwargs=url_kwargs, request=request, format=format)
#
#     # def get_object(self, view_name, view_args, view_kwargs):
#     #     lookup_kwargs = {
#     #         'organization__slug': view_kwargs['organization_slug'],
#     #         'pk': view_kwargs['customer_pk']
#     #     }
#     #     return self.get_queryset().get(**lookup_kwargs)
