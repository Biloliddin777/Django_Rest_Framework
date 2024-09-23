from rest_framework import serializers
from olcha.models import Category, Group, Product


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['updated_at'] = instance.updated_at
        return representation


class CategorySerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    full_image_url = serializers.SerializerMethodField()
    groups_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'full_image_url', 'created_at', 'updated_at', 'groups_count', 'groups']

    def get_groups_count(self, obj):
        return obj.groups.count()

    def get_full_image_url(self, instance):
        if instance.image:
            request = self.context.get('request')
            return request.build_absolute_uri(instance.image.url) if request else None
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['updated_at'] = instance.updated_at
        return representation


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['updated_at'] = instance.updated_at
        return representation
