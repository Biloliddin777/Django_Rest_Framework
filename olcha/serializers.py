from django.db.models import Avg
from rest_framework import serializers
from olcha.models import Category, Group, Product, Image, Comment


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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()



    class Meta:
        model = Product
        fields = '__all__'

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.users_like.filter(id=request.user.id).exists()
        return False

    def get_average_rating(self, obj):
        average = obj.comments.aggregate(Avg('rating'))['rating__avg']
        return round(average, 2) if average else 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['updated_at'] = instance.updated_at
        return representation
