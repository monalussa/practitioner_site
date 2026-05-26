from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import (
    CharBlock,
    RichTextBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index
from wagtailseo.models import SeoMixin, TwitterCard


class QuoteBlock(StructBlock):
    text = TextBlock(label="Quote text")
    attribution = CharBlock(required=False, label="Attribution")

    class Meta:
        icon = "openquote"
        label = "Quote"
        template = "blocks/quote.html"


class TestimonialBlock(StructBlock):
    quote = TextBlock(label="Testimonial text")
    author_name = CharBlock(label="Author name")
    author_role = CharBlock(required=False, label="Role / description (e.g. 'Mother of two')")

    class Meta:
        icon = "user"
        label = "Testimonial"
        template = "blocks/testimonial.html"


class FeatureBlock(StructBlock):
    icon = CharBlock(label="Icon (emoji or symbol)", max_length=10)
    heading = CharBlock(label="Heading")
    text = TextBlock(label="Description")

    class Meta:
        icon = "pick"
        label = "Feature / step"
        template = "blocks/feature.html"


BODY_BLOCKS = [
    ("rich_text", RichTextBlock(label="Text")),
    ("image", ImageChooserBlock(label="Image")),
    ("quote", QuoteBlock()),
    ("testimonial", TestimonialBlock()),
    ("feature", FeatureBlock()),
]


class HomePage(SeoMixin, Page):
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.CharField(max_length=300, blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = RichTextField(blank=True)
    body = StreamField(BODY_BLOCKS, blank=True, use_json_field=True)

    promote_panels = SeoMixin.seo_panels
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_title"),
            FieldPanel("hero_subtitle"),
            FieldPanel("hero_image"),
        ], heading="Hero"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    def get_features(self):
        return [b for b in self.body if b.block_type == "feature"]

    def get_testimonials(self):
        return [b for b in self.body if b.block_type == "testimonial"]

    def get_recent_posts(self, count=2):
        from .models import BlogPostPage
        return BlogPostPage.objects.live().order_by("-published_date")[:count]

    seo_twitter_card = TwitterCard.SUMMARY
    seo_content_type = "website"

    class Meta:
        verbose_name = "Home page"


class AboutPage(SeoMixin, Page):
    body = StreamField(BODY_BLOCKS, use_json_field=True)

    promote_panels = SeoMixin.seo_panels
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    seo_content_type = "website"

    class Meta:
        verbose_name = "About page"


class ServicesIndexPage(SeoMixin, Page):
    intro = RichTextField(blank=True)

    promote_panels = SeoMixin.seo_panels
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["pages.ServicePage"]

    def get_services(self):
        return ServicePage.objects.live().descendant_of(self).order_by("title")

    class Meta:
        verbose_name = "Services index"


class ServicePage(SeoMixin, Page):
    tagline = models.CharField(max_length=250, blank=True)
    body = StreamField(BODY_BLOCKS, use_json_field=True)
    duration = models.CharField(max_length=80, blank=True, help_text='e.g. "60 minutes"')
    price_display = models.CharField(max_length=80, blank=True, help_text='e.g. "€80 / session"')
    cta_text = models.CharField(max_length=80, default="Book a session")
    cta_url = models.URLField(blank=True, help_text="Link to booking page or subdomain")

    promote_panels = SeoMixin.seo_panels
    content_panels = Page.content_panels + [
        FieldPanel("tagline"),
        FieldPanel("body"),
        MultiFieldPanel([
            FieldPanel("duration"),
            FieldPanel("price_display"),
            FieldPanel("cta_text"),
            FieldPanel("cta_url"),
        ], heading="Booking CTA"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("tagline"),
    ]

    parent_page_types = ["pages.ServicesIndexPage"]

    class Meta:
        verbose_name = "Service"


class BlogIndexPage(SeoMixin, Page):
    intro = RichTextField(blank=True)

    promote_panels = SeoMixin.seo_panels
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["pages.BlogPostPage"]

    def get_posts(self):
        return BlogPostPage.objects.live().descendant_of(self).order_by("-published_date")

    class Meta:
        verbose_name = "Blog index"


class BlogPostPage(SeoMixin, Page):
    published_date = models.DateField("Published date", null=True, blank=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short summary for listings and SEO")
    body = StreamField(BODY_BLOCKS, use_json_field=True)

    promote_panels = SeoMixin.seo_panels
    content_panels = Page.content_panels + [
        FieldPanel("published_date"),
        FieldPanel("featured_image"),
        FieldPanel("excerpt"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("excerpt"),
    ]

    parent_page_types = ["pages.BlogIndexPage"]

    class Meta:
        verbose_name = "Blog post"
        verbose_name_plural = "Blog posts"


class BookingPage(SeoMixin, Page):
    intro = RichTextField(blank=True)
    booking_url = models.URLField(
        blank=True,
        help_text="URL of Easy!Appointments booking subdomain, e.g. https://book.yourdomain.com",
    )
    embed_booking = models.BooleanField(
        default=False,
        help_text="Embed the booking widget as an iframe instead of linking out",
    )

    promote_panels = SeoMixin.seo_panels
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("booking_url"),
        FieldPanel("embed_booking"),
    ]

    class Meta:
        verbose_name = "Booking page"


class ContactPage(SeoMixin, Page):
    intro = RichTextField(blank=True)

    promote_panels = SeoMixin.seo_panels
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    class Meta:
        verbose_name = "Contact page"
