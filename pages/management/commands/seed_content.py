from datetime import date

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site


class Command(BaseCommand):
    help = "Seed initial content: home page, services, blog posts, booking, contact."

    def handle(self, *args, **options):
        from pages.models import (
            AboutPage, BlogIndexPage, BlogPostPage,
            BookingPage, ContactPage, HomePage,
            ServicePage, ServicesIndexPage,
        )

        root = Page.objects.filter(depth=1).first()
        if root is None:
            self.stderr.write("No root page found. Run migrations first.")
            return

        # ── Home Page ─────────────────────────────────────────────────
        # Remove the default Wagtail welcome page if it's blocking our slug
        plain_welcome = Page.objects.filter(slug="home", depth=2).first()
        if plain_welcome and plain_welcome.specific_class == Page:
            plain_welcome.delete()
            self.stdout.write("Removed default Wagtail welcome page.")

        if HomePage.objects.filter(slug="home").exists():
            self.stdout.write("HomePage already exists — skipping.")
            home = HomePage.objects.get(slug="home")
        else:
            home = HomePage(
                title="Home",
                slug="home",
                hero_title="Raise Emotionally Intelligent Kids — Starting With Yourself",
                hero_subtitle=(
                    "Conscious parenting begins when you understand what's driving your reactions. "
                    "Learn to break generational patterns and create the family connection "
                    "you've always wanted."
                ),
                intro=(
                    "<p>Most parenting advice focuses on changing your child's behaviour. "
                    "But what if the real transformation starts within you? "
                    "Conscious parenting coaching helps you develop emotional awareness, "
                    "heal inherited patterns, and respond to your children with intention "
                    "instead of instinct. Whether you're struggling with anger, repeating "
                    "patterns from your own childhood, or searching for a deeper connection "
                    "with your kids — you're in the right place.</p>"
                ),
                body=[
                    ("feature", {
                        "icon": "🌱",
                        "heading": "Build Awareness",
                        "text": (
                            "Understand your emotional triggers and the patterns you inherited. "
                            "Awareness is the first step toward lasting change."
                        ),
                    }),
                    ("feature", {
                        "icon": "💬",
                        "heading": "Develop New Skills",
                        "text": (
                            "Learn practical tools for staying calm, validating feelings, "
                            "and setting boundaries without shame or punishment."
                        ),
                    }),
                    ("feature", {
                        "icon": "🤝",
                        "heading": "Transform Your Relationship",
                        "text": (
                            "Build a deeper connection with your children — and yourself — "
                            "that lasts long beyond our sessions together."
                        ),
                    }),
                    ("testimonial", {
                        "quote": (
                            "I came in feeling like a failure as a parent. I leave each session "
                            "with more tools, more compassion for myself, and a completely "
                            "different relationship with my daughter."
                        ),
                        "author_name": "Anna M.",
                        "author_role": "Mother of two",
                    }),
                    ("testimonial", {
                        "quote": (
                            "The moment I understood that my son's behaviour was telling me "
                            "something about his emotions — not testing me — everything changed."
                        ),
                        "author_name": "Tomáš K.",
                        "author_role": "Father",
                    }),
                ],
                seo_title="Conscious Parenting Coach | Raise Emotionally Intelligent Kids",
                search_description=(
                    "Conscious parenting coaching to help you break generational patterns, "
                    "understand your child's behaviour, and build deeper family connection."
                ),
                show_in_menus=True,
            )
            root.add_child(instance=home)
            self.stdout.write(self.style.SUCCESS("✓ HomePage"))

        # Point default site at home page
        site = Site.objects.filter(is_default_site=True).first()
        if site is None:
            Site.objects.create(
                hostname="localhost",
                port=8000,
                root_page=home,
                is_default_site=True,
                site_name="Conscious Parenting Coach",
            )
            self.stdout.write(self.style.SUCCESS("✓ Site created → HomePage"))
        elif site.root_page_id != home.id:
            site.root_page = home
            site.save()
            self.stdout.write(self.style.SUCCESS("✓ Site root → HomePage"))

        # ── About ─────────────────────────────────────────────────────
        if not AboutPage.objects.filter(slug="about").exists():
            home.add_child(instance=AboutPage(
                title="About",
                slug="about",
                body=[
                    ("rich_text", (
                        "<h2>Hello, I'm your conscious parenting coach</h2>"
                        "<p>I work with parents who sense there's a different, more connected "
                        "way to raise their children — and who are ready to do the inner work "
                        "to get there. My approach is grounded in neuroscience, attachment "
                        "theory, and the principles of conscious parenting.</p>"
                        "<p>My own journey as a parent taught me that the most transformative "
                        "thing I could do for my children was to understand myself first. "
                        "That's the work I now support other parents to do.</p>"
                        "<h2>My approach</h2>"
                        "<p>Sessions are warm, non-judgmental, and deeply practical. "
                        "We explore what's really happening beneath the surface — in your "
                        "child's behaviour and in your own reactions — and build skills you "
                        "can use from the very next interaction.</p>"
                    )),
                ],
                seo_title="About | Conscious Parenting Coach",
                search_description=(
                    "Learn about my approach to conscious parenting coaching — "
                    "grounded in neuroscience, attachment theory, and deep compassion."
                ),
                show_in_menus=True,
            ))
            self.stdout.write(self.style.SUCCESS("✓ AboutPage"))

        # ── Services ──────────────────────────────────────────────────
        services_index = ServicesIndexPage.objects.filter(slug="services").first()
        if services_index is None:
            services_index = ServicesIndexPage(
                title="Services",
                slug="services",
                intro=(
                    "<p>Every family is different. Whether you're looking for a single "
                    "conversation or ongoing support, there's a path that fits where you are.</p>"
                ),
                seo_title="Coaching Services | Conscious Parenting Coach",
                search_description=(
                    "Explore conscious parenting coaching services: free discovery call "
                    "to a full 6-session coaching programme."
                ),
                show_in_menus=True,
            )
            home.add_child(instance=services_index)
            self.stdout.write(self.style.SUCCESS("✓ ServicesIndexPage"))

        if not ServicePage.objects.filter(slug="discovery-call").exists():
            services_index.add_child(instance=ServicePage(
                title="Free Discovery Call",
                slug="discovery-call",
                tagline="Not sure where to start? Let's talk.",
                body=[
                    ("rich_text", (
                        "<p>A free 30-minute conversation to understand what's happening "
                        "in your family and whether conscious parenting coaching is the "
                        "right fit for you. No pressure, no commitment — just an honest, "
                        "supportive conversation.</p>"
                        "<p><strong>What we cover:</strong></p>"
                        "<ul>"
                        "<li>What's feeling hardest right now in your parenting</li>"
                        "<li>What you're hoping for your family</li>"
                        "<li>How coaching works and what to expect</li>"
                        "</ul>"
                    )),
                ],
                duration="30 minutes",
                price_display="Free",
                cta_text="Book your free call",
                seo_title="Free Discovery Call | Conscious Parenting Coaching",
                search_description=(
                    "Book a free 30-minute discovery call to explore conscious parenting "
                    "coaching and find out if it's right for your family."
                ),
            ))
            self.stdout.write(self.style.SUCCESS("✓ ServicePage: Discovery Call"))

        if not ServicePage.objects.filter(slug="coaching-programme").exists():
            services_index.add_child(instance=ServicePage(
                title="1:1 Coaching Programme",
                slug="coaching-programme",
                tagline="Six sessions of deep, personal support.",
                body=[
                    ("rich_text", (
                        "<p>A focused six-session programme designed to help you understand "
                        "your emotional patterns, respond to your children from a grounded "
                        "place, and build a parenting approach that reflects your values.</p>"
                        "<p><strong>What's included:</strong></p>"
                        "<ul>"
                        "<li>6 × 60-minute sessions (online or in person)</li>"
                        "<li>Personalised reflection exercises between sessions</li>"
                        "<li>Email support throughout the programme</li>"
                        "<li>A tailored action plan for your family</li>"
                        "</ul>"
                    )),
                ],
                duration="6 × 60 minutes",
                price_display="From €480",
                cta_text="Book a discovery call first",
                seo_title="1:1 Coaching Programme | Conscious Parenting Coach",
                search_description=(
                    "A 6-session conscious parenting coaching programme to transform your "
                    "family relationships — online or in person."
                ),
            ))
            self.stdout.write(self.style.SUCCESS("✓ ServicePage: 1:1 Programme"))

        # ── Blog ──────────────────────────────────────────────────────
        blog_index = BlogIndexPage.objects.filter(slug="blog").first()
        if blog_index is None:
            blog_index = BlogIndexPage(
                title="Blog",
                slug="blog",
                intro="<p>Thoughts, tools, and real talk for parents on the conscious parenting path.</p>",
                seo_title="Conscious Parenting Blog | Articles & Insights",
                search_description=(
                    "Articles on conscious parenting, emotional intelligence, and breaking "
                    "generational patterns — for parents ready to do things differently."
                ),
                show_in_menus=True,
            )
            home.add_child(instance=blog_index)
            self.stdout.write(self.style.SUCCESS("✓ BlogIndexPage"))

        if not BlogPostPage.objects.filter(slug="why-your-child-acts-out").exists():
            blog_index.add_child(instance=BlogPostPage(
                title="Why Your Child Acts Out: The Emotional Truth Behind Behaviour",
                slug="why-your-child-acts-out",
                published_date=date(2026, 5, 1),
                excerpt=(
                    "When children misbehave, they're not being difficult — they're communicating "
                    "an emotion they don't yet have words for. Here's how to listen differently."
                ),
                body=[
                    ("rich_text", (
                        "<p>Most parents ask the same question when their child misbehaves: "
                        "<em>How do I fix this?</em> But conscious parenting asks something "
                        "different — and far more powerful: <em>What is my child actually feeling?</em></p>"
                        "<p>This shift from behaviour-focused to emotion-focused parenting is "
                        "transforming how families connect and resolve conflict. When your child "
                        "throws a tantrum, refuses to listen, or acts aggressively, these aren't "
                        "character flaws. They're signals — your child is struggling to understand "
                        "or express an emotion they don't yet have words for.</p>"
                        "<h2>The real reason behind the behaviour</h2>"
                        "<p>Neuroscience shows that when children haven't developed tools to manage "
                        "emotions, they act out. A three-year-old who hits a sibling isn't \"bad\" — "
                        "they're overwhelmed. A seven-year-old who refuses homework might be carrying "
                        "disappointment from earlier that day. A teenager who withdraws might be "
                        "processing shame they can't yet articulate.</p>"
                        "<p>Conscious parenting recognises that the behaviour you see is only the "
                        "tip of the iceberg. Beneath it lie feelings your child cannot manage alone: "
                        "jealousy, fear, powerlessness, or excitement they've been told to contain.</p>"
                        "<h2>The three-step emotional response</h2>"
                        "<p><strong>Pause before reacting.</strong> When frustration rises, your "
                        "child's behaviour has triggered something in you — perhaps your own fears "
                        "about being a \"good parent\". Create space: three deep breaths, or "
                        "stepping away briefly.</p>"
                        "<p><strong>Get curious instead of corrective.</strong> Ask: \"What were you "
                        "feeling when that happened?\" This teaches your child that feelings matter "
                        "and that they're safe exploring emotions with you.</p>"
                        "<p><strong>Validate first, set boundaries second.</strong> \"I see you're "
                        "really upset, and that makes sense.\" Connection comes before correction. "
                        "A child whose emotions are acknowledged is far more receptive to hearing "
                        "about better choices.</p>"
                        "<h2>Building emotional vocabulary</h2>"
                        "<p>Children learn emotional intelligence by watching you. When you model "
                        "naming your own emotions — <em>\"I'm feeling frustrated, so I'm going to "
                        "take a short break\"</em> — you teach them that feelings are normal, "
                        "manageable, and worthy of attention.</p>"
                        "<p>Conscious parenting isn't permissive; it's purposeful. The goal is "
                        "raising humans who understand their inner world, can express their needs "
                        "clearly, and build healthy relationships — not just compliance.</p>"
                        "<p>If you'd like support on this journey, "
                        "<a href=\"/booking/\">book a free discovery call</a> — "
                        "let's explore what's possible for your family.</p>"
                    )),
                ],
                seo_title="Why Your Child Acts Out: The Emotional Truth | Conscious Parenting Blog",
                search_description=(
                    "Learn why kids act out and how to respond with emotional intelligence. "
                    "Discover the conscious parenting approach that transforms behaviour struggles."
                ),
            ))
            self.stdout.write(self.style.SUCCESS("✓ Blog post 1"))

        if not BlogPostPage.objects.filter(slug="breaking-generational-parenting-patterns").exists():
            blog_index.add_child(instance=BlogPostPage(
                title="How to Break Generational Parenting Patterns and Heal Your Family",
                slug="breaking-generational-parenting-patterns",
                published_date=date(2026, 5, 15),
                excerpt=(
                    "Recognising 'I'm doing exactly what my parents did' is where healing begins. "
                    "Conscious parenting gives you the tools to write a new chapter for your family."
                ),
                body=[
                    ("rich_text", (
                        "<p>One of the most powerful moments in a parent's journey is this "
                        "realisation: <em>I'm doing exactly what my parents did — and I don't "
                        "want to.</em> This awareness is where healing begins, and it's the "
                        "foundation of what many call \"cycle-breaking\" parenting.</p>"
                        "<p>Generational patterns are beliefs, behaviours, and emotional reactions "
                        "passed down unconsciously through families. If you grew up hearing "
                        "\"crying is weakness\", you might struggle to let your child express sadness. "
                        "These patterns feel normal — because they're what you learned about parenting.</p>"
                        "<h2>Why breaking cycles matters</h2>"
                        "<p>When you break a generational pattern, you're not just changing your "
                        "parenting approach — you're healing your own childhood while protecting "
                        "your children's emotional development. Children raised with emotional "
                        "awareness develop stronger self-regulation, healthier relationships, "
                        "and greater resilience.</p>"
                        "<p>Breaking cycles means your children won't inherit your unprocessed pain. "
                        "Instead of passing wounds forward, you become the generation that says: "
                        "<em>This stops here. With me, things are different.</em></p>"
                        "<h2>Five essential steps</h2>"
                        "<p><strong>1. Recognise the patterns.</strong> Awareness is your first "
                        "superpower. Which of your parents' behaviours do you find yourself "
                        "repeating? Naming patterns removes their power over you.</p>"
                        "<p><strong>2. Understand the \"why\" without using it as an excuse.</strong> "
                        "Your parents did the best they could with what they had. Understanding "
                        "their context creates compassion — but understanding doesn't mean repeating. "
                        "You have choices they didn't.</p>"
                        "<p><strong>3. Heal your inner child.</strong> Before you can parent "
                        "differently, meet the unmet needs of your younger self — through therapy, "
                        "journalling, or simply acknowledging: <em>That hurt. I deserved better.</em></p>"
                        "<p><strong>4. Build your own parenting philosophy.</strong> Deliberately "
                        "choose your values. What kind of parent do you want to be? Let these "
                        "intentions guide your responses, not your automatic reactions.</p>"
                        "<p><strong>5. Expect setbacks and practise self-compassion.</strong> "
                        "You will slip into old patterns. What matters is your willingness to "
                        "notice, pause, and try again.</p>"
                        "<h2>The ripple effect</h2>"
                        "<p>Breaking generational cycles is perhaps the most loving thing you can "
                        "do for your family. The healing work you do today echoes through generations.</p>"
                        "<p>Ready to start? <a href=\"/booking/\">Book a free discovery call</a> "
                        "and let's take the first step together.</p>"
                    )),
                ],
                seo_title="How to Break Generational Parenting Patterns | Conscious Parenting Blog",
                search_description=(
                    "Discover how conscious parenting breaks generational trauma cycles. "
                    "Learn to heal your past while raising emotionally resilient children."
                ),
            ))
            self.stdout.write(self.style.SUCCESS("✓ Blog post 2"))

        # ── Booking ───────────────────────────────────────────────────
        if not BookingPage.objects.filter(slug="booking").exists():
            home.add_child(instance=BookingPage(
                title="Book a Session",
                slug="booking",
                intro=(
                    "<p>Ready to take the first step? Choose a time that works for you "
                    "and I'll be in touch to confirm. All sessions are available online "
                    "or in person in Prague.</p>"
                ),
                seo_title="Book a Coaching Session | Conscious Parenting Coach",
                search_description=(
                    "Book a free discovery call or a coaching session. "
                    "Online and in-person sessions available."
                ),
                show_in_menus=True,
            ))
            self.stdout.write(self.style.SUCCESS("✓ BookingPage"))

        # ── Contact ───────────────────────────────────────────────────
        if not ContactPage.objects.filter(slug="contact").exists():
            home.add_child(instance=ContactPage(
                title="Contact",
                slug="contact",
                intro=(
                    "<p>Have a question before booking? I'd love to hear from you. "
                    "I'll reply within 1–2 business days.</p>"
                ),
                seo_title="Contact | Conscious Parenting Coach",
                search_description=(
                    "Get in touch with a conscious parenting coach. "
                    "I'll reply within 1–2 business days."
                ),
                show_in_menus=True,
            ))
            self.stdout.write(self.style.SUCCESS("✓ ContactPage"))

        self.stdout.write(self.style.SUCCESS(
            "\nDone! Visit http://localhost:8000/ to see the site."
        ))
