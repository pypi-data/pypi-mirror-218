import os

from typing import Optional, List, Generic, TypeVar
from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from jinja2 import Environment, FileSystemLoader

from adria.core.utils import mkdir


class Category(BaseModel):
    title: str


class SiteInfo(BaseModel):
    title: str
    lang_code: str = Field("en")
    company_name: Optional[str]
    domain: str

    @property
    def copyright(self) -> str:
        if self.company_name:
            return self.company_name

        return self.title


T = TypeVar("T")


class PageInfo(GenericModel, Generic[T]):
    title: str
    layout: str
    slug: str
    path: str
    tags: List[str]
    category: Optional[Category]

    context: T


class TemplateUtils(object):
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("."))

    def render_page(self, path: str, **context):
        template = self.env.get_template(path)
        return template.render(utils=self, **context)

    @property
    def year_now(self) -> int:
        return datetime.now().year


class BaseGenerator(object):
    def __init__(
            self,
            site_info: SiteInfo,
            utils: Optional[TemplateUtils] = None
    ):
        self.site_info = site_info
        if utils is None:
            self.utils = TemplateUtils()
        else:
            self.utils = utils

    @property
    def output_root(self):
        return os.path.join(os.getcwd(), "dist")

    def generate_page(self, page_info: PageInfo):
        html = self.utils.render_page(
            f"_layouts/{page_info.layout}",
            site=self.site_info.dict(),
            page=page_info.dict(),
            **page_info.context
        )

        path_buff = page_info.path.split("/")
        output_dir = os.path.join(self.output_root, *path_buff)
        mkdir(output_dir)

        with open(
            os.path.join(output_dir, f"{page_info.slug}.html"),
            "w"
        ) as f:
            f.write(html)
