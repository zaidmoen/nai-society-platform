from django.core.management.base import BaseCommand
from apps.committees.models import Committee

COMMITTEES = [
    ("لجنة الأنشطة", "activities", "تنظيم الفعاليات واللقاءات الطلابية."),
    ("لجنة التقنية", "technology", "تطوير ودعم المنصات والأنشطة التقنية."),
    ("لجنة الإعلام", "media", "إنتاج المحتوى والتصميم والتغطية الإعلامية."),
    ("لجنة العلاقات العامة", "public-relations", "إدارة الشراكات والتواصل المؤسسي."),
    ("لجنة الأنشطة المتخصصة للذكاء الاصطناعي", "ai-activities", "تنظيم أنشطة وورش متخصصة في الذكاء الاصطناعي."),
]

class Command(BaseCommand):
    help = "Create or update NAI's five current committees."

    def handle(self, *args, **options):
        for name, slug, description in COMMITTEES:
            Committee.objects.update_or_create(slug=slug, defaults={"name": name, "description": description, "is_active": True})
            self.stdout.write(self.style.SUCCESS(f"Ready: {name}"))
