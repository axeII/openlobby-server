from elasticsearch import NotFoundError
import graphene
from graphene import relay
from graphene.types.json import JSONString

from ..documents import ReportDoc
from .. import models
from .paginator import Paginator
from .. import search


def get_higlighted(hit, field):
    """Returns higlighted text of field if search is higlighted."""
    if hasattr(hit.meta, 'highlight') and field in hit.meta.highlight:
        return hit.meta.highlight[field][0]
    return hit[field] if field in hit else ''


class Report(graphene.ObjectType):
    author = graphene.Field(lambda: User)
    date = graphene.String()
    published = graphene.String()
    title = graphene.String()
    body = graphene.String()
    received_benefit = graphene.String()
    provided_benefit = graphene.String()
    our_participants = graphene.String()
    other_participants = graphene.String()
    extra = JSONString()

    class Meta:
        interfaces = (relay.Node, )

    @classmethod
    def from_es(cls, report, author=None):
        return cls(
            id=report.meta.id,
            author=author,
            date=report.date,
            published=report.published,
            title=get_higlighted(report, 'title'),
            body=get_higlighted(report, 'body'),
            received_benefit=get_higlighted(report, 'received_benefit'),
            provided_benefit=get_higlighted(report, 'provided_benefit'),
            our_participants=get_higlighted(report, 'our_participants'),
            other_participants=get_higlighted(report, 'other_participants'),
            extra=report.extra._d_,
        )

    @classmethod
    def get_node(cls, info, id):
        try:
            report = ReportDoc.get(id, using=info.context['es'], index=info.context['index'])
        except NotFoundError:
            return None

        author_type = cls._meta.fields['author'].type
        author = author_type.get_node(info, report.author_id)
        return cls.from_es(report, author)


class ReportConnection(relay.Connection):
    total_count = graphene.Int()

    class Meta:
        node = Report


class User(graphene.ObjectType):
    openid_uid = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()

    class Meta:
        interfaces = (relay.Node, )

    @classmethod
    def from_db(cls, user):
        return cls(
            id=user.id,
            openid_uid=user.openid_uid,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )

    @classmethod
    def get_node(cls, info, id):
        # TODO return only viewer
        try:
            return cls.from_db(models.User.objects.get(id=id))
        except models.User.DoesNotExist:
            return None


class Author(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    openid_uid = graphene.String()
    extra = JSONString()
    # TODO
    # reports = relay.ConnectionField(ReportConnection)

    class Meta:
        interfaces = (relay.Node, )

    @classmethod
    def from_db(cls, user):
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            openid_uid=user.openid_uid,
            extra=user.extra,
        )

    @classmethod
    def get_node(cls, info, id):
        try:
            return cls.from_db(models.User.objects.get(id=id, is_author=True))
        except models.User.DoesNotExist:
            return None

    # TODO
    """
    def resolve_reports(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        response = search.reports_by_author(self.id, paginator, **info.context)
        total = response.hits.total
        page_info = paginator.get_page_info(total)

        edges = []
        for i, report in enumerate(response):
            cursor = paginator.get_edge_cursor(i + 1)
            node = Report.from_es(report, author=self)
            edges.append(ReportConnection.Edge(node=node, cursor=cursor))

        return ReportConnection(page_info=page_info, edges=edges, total_count=total)
    """


class LoginShortcut(graphene.ObjectType):
    name = graphene.String()

    class Meta:
        interfaces = (relay.Node, )

    @classmethod
    def from_db(cls, openid_client):
        return cls(id=openid_client.id, name=openid_client.name)

    @classmethod
    def get_node(cls, info, id):
        try:
            client = models.OpenIdClient.objects.get(id=id)
            return cls.from_db(client)
        except models.OpenIdClient.DoesNotExist:
            return None
