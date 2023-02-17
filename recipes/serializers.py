from rest_framework import serializers
from core.models import Recipe
from core.models import Tag
from rest_framework.fields import CurrentUserDefault


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']
        read_only_fields = ['id']

    def create(self,validated_data):
        return Tag.objects.create(**validated_data)

    def update(self,instance,validated_data):
        tags = validated_data.pop('tags',None)

        title = validated_data['title']
        time_minutes = validated_data['time_minutes']
        price = validated_data['price']
        link = validated_data['link']
        description = validated_data['description']

        recipe = Recipe.objects.filter(pk=instance.pk).update(title=title,
                                                              time_minutes=time_minutes,
                                                              price = price,
                                                              link = link,
                                                              description=description)

        if tags:
            recipe.tags_set.remove(tags)
            recipe.save()
            for tag in tags:
                recipe.tags.add(tag)
                recipe.save()
        return recipe

class RecipeSerializer(serializers.ModelSerializer):
    """This serializer is used to list recipes"""
    class Meta:
        model = Recipe
        fields = ['id','title','time_minutes','price','link','user','tags']
        read_only_fields = ['id','user','image']

    def create(self,validated_data):
        tags = validated_data.pop('tags',[])
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        return recipe


class DetailRecipeSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description','image']
        read_only_fields = RecipeSerializer.Meta.read_only_fields


class ImageRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id','image']
        read_only_fields = ['id']
