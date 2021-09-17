from django.db.models import fields
from rest_framework import serializers
from .models import *


class SubmissionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    poll = serializers.SlugRelatedField(
        queryset=Poll.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(
        queryset=Question.objects.all(), slug_field='id')
    option = serializers.SlugRelatedField(
        queryset=Option.objects.all(), slug_field='id', allow_null=True, required=False)
    option_text = serializers.CharField(
        max_length=200, allow_null=True, required=False)
    userId = serializers.IntegerField()

    class Meta:
        model = Submission
        fields = '__all__'

        def create(self, validated_data):
            print('data', **validated_data)
            return Submission.objects.create(**validated_data)

        def update(self, instance, validated_data):
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance

        def validate(self, attrs):
            question_type = Question.objects.get(
                id=attrs['question'].id).question_type
            try:
                if question_type == "one" or question_type == "text":
                    obj = Submission.objects.get(question=attrs['question'].id, survey=attrs['poll'],
                                                 user_id=attrs['user_id'])
                elif question_type == "multiple":
                    obj = Submission.objects.get(question=attrs['question'].id, survey=attrs['poll'],
                                                 user_id=attrs['user_id'],
                                                 option=attrs['option'])
            except Submission.DoesNotExist:
                return attrs
            else:
                raise serializers.ValidationError('Уже ответил')


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.SlugRelatedField(
        queryset=Question.objects.all(), slug_field='id')
    option_text = serializers.CharField(max_length=200)

    def validate(self, attrs):
        try:
            obj = Option.objects.get(
                question=attrs['question'].id,  option_text=attrs['option_text'])
        except Option.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Выбор уже существует')

    class Meta:
        model = Option
        fields = "__all__"

    def create(self, validated_data):
        return Option.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    poll = serializers.SlugRelatedField(
        queryset=Poll.objects.all(), slug_field='id')
    text_q = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=200)
    options = OptionSerializer(many=True, read_only=True)

    def validate(self, attrs):
        type = attrs['type']
        if type == 'one' or type == 'multiple' or type == 'text':
            return attrs
        raise serializers.ValidationError(
            'Тип вопроса может быть только один(one), несколько(multiple) или текстовый(text)')

    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PollSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    startDate = serializers.DateField()
    finishDate = serializers.DateField()
    description = serializers.CharField(max_length=200)

    class Meta:
        model = Poll
        fields = "__all__"

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'startDate' in validated_data:
            raise serializers.ValidationError(
                {'startDate': 'Вы не можете изменять это поле.'})
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
