import asyncio

import graphene
import graphql_social_auth
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_relay import from_global_id

from api.decorators import validate_token

from .models import Task, User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'username': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'is_staff': ['exact']
        }
        interfaces = (relay.Node, )


class TaskNode(DjangoObjectType):
    class Meta:
        model = Task
        filter_fields = {'title': ['exact', 'icontains']}
        interfaces = (relay.Node, )


# タスクの作成
class CreateTaskMutation(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        content = graphene.String(required=False)
        task_image = Upload(required=False)

    task = graphene.Field(TaskNode)

    @validate_token
    def mutate_and_get_payload(root, info, **input):
        current_user = get_user_model().objects.get(
            email=input.get('request_user_email'))
        title = input.get('title')
        content = input.get('content')
        task = Task(
            create_user=current_user.id,
            title=title,
        )
        if content is not None:
            task.content = content
        task.save()
        return CreateTaskMutation(task=task)


# ミューテーション
class Mutation(graphene.ObjectType):
    # OAuth
    social_auth = graphql_social_auth.SocialAuth.Field()

    # タスク
    create_task = CreateTaskMutation.Field()


# クエリ
class Query(graphene.ObjectType):
    # ユーザー
    user = graphene.Field(UserNode, id=graphene.NonNull(graphene.ID))
    all_users = DjangoFilterConnectionField(UserNode)

    # タスク
    task = graphene.Field(TaskNode, id=graphene.NonNull(graphene.ID))
    my_all_tasks = DjangoFilterConnectionField(TaskNode)

    @validate_token
    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        # ↓デコレーターで追加されたemailにアクセス
        email = kwargs.get('request_user_email')
        return get_user_model().objects.get(email=email)
        # return get_user_model().objects.get(id=from_global_id(id)[1])

    def resolve_all_users(self, info, **kwargs):
        return get_user_model().objects.all()

    # タスク
    def resolve_task(self, info, **kwargs):
        id = kwargs.get('id')
        task = Task.objects.get(id=from_global_id(id)[1])
        return task

    @validate_token
    def resolve_my_all_tasks(self, info, **kwargs):
        login_user = get_user_model().objects.get(
            email=kwargs.get('request_user_email'))
        all_tasks = Task.objects.all()
        return all_tasks.filter(create_user=login_user.id)


# サブスクリプション
class Subscription(graphene.ObjectType):
    count_seconds = graphene.Float(up_to=graphene.Int())

    async def resolve_count_seconds(root, info, up_to):
        for i in range(up_to):
            yield i
            await asyncio.sleep(1.)
        yield up_to
