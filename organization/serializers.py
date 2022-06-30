from django.contrib.auth.models import Group
from rest_framework import serializers

from auth.serializers import UserSerializer
from .models import Organization

__all__ = [
    'OrganizationBasicSerializer',
    'NestedOrganizationBasicSerializer', 'OrganizationSerializer'
]

class OrganizationBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'slug', 'short_name', 'name', 'logo_url',
        ]


class NestedOrganizationBasicSerializer(OrganizationBasicSerializer):
    sub_orgs = serializers.SerializerMethodField()
    def get_sub_orgs(self, org):
        if org.is_leaf():
            return []
        return NestedOrganizationBasicSerializer(org.get_children(), many=True, read_only=True).data

    class Meta:
        model = Organization
        fields = [
            'slug', 'short_name', 'name', 'logo_url', 'sub_orgs',
        ]


class OrganizationSerializer(OrganizationBasicSerializer):
    suborg_count = serializers.SerializerMethodField()
    def get_suborg_count(self, inst):
        if getattr(inst, 'get_descendant_count', False):
            return inst.get_descendant_count()
        return 0

    class Meta:
        model = Organization
        fields = [
            'slug', 'short_name', 'name',
            'is_open', 'is_unlisted',
            'logo_url',
            'member_count', #'performance_points'
            'suborg_count',
        ]
        read_only_fields = ('member_count', 'suborg_count')
        # extra_kwargs = {
        #     'logo_url': {'read_only': True},
        #     'member_count': {'read_only': True},
        #     'suborg_count': {'read_only': True},
        # }


class OrganizationDetailSerializer(OrganizationSerializer):
    admins = serializers.SerializerMethodField()
    def get_admins(self, instance):
        from userprofile.serializers import UserProfileBasicSerializer
        return UserProfileBasicSerializer(instance.admins, many=True).data

    class Meta:
        model = Organization
        fields = [
            'slug', 'short_name', 'name', 'is_open',
            'logo_url',

            'admins', 'about', 'creation_date', 'slots',

            'member_count', #'performance_points'
            'suborg_count',
        ]
        read_only_fields = ('member_count', 'suborg_count')
