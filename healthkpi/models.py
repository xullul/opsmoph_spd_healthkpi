from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class KpiGroup(models.Model):
    """กลุ่มข้อมูลที่การประเมิน"""
    name = models.CharField(max_length=255, verbose_name=_('ชื่อกลุ่ม'), unique=True)
    abbr = models.CharField(max_length=100, verbose_name=_('ชื่อย่อ'), null=True, blank=True)
    en_name = models.CharField(max_length=255, verbose_name=_('ชื่ออังกฤษ'), null=True, blank=True)

    class Meta:
        verbose_name = _('ชื่อกลุ่มการประเมิน')
        verbose_name_plural = _('ชื่อกลุ่มการประเมิน')
        db_table_comment = _('ชื่อกลุ่มการประเมิน หรือชื่อเดิม 4E')


class KpiLevel(models.Model):
    """
    ประเทศ
    รายจังหวัด
    เขตสุขภาพ
    กระทรวงสาธารณสุข
    กรมในสาสุข
    สป.สธ.
    """
    name = models.CharField(max_length=255, verbose_name=_('ชื่อ'), unique=True)
    code = models.CharField(max_length=5, verbose_name=_('รหัส'), unique=True)
    
    class Meta:
        verbose_name = _('ระดับการประเมิน')
        verbose_name_plural = _('ระดับการประเมิน')
        db_table_comment = _('ระดับการประเมิน เช่น ระดับเขตสุขภาพ หรือระดับจังหวัด เป็นต้น')


class Kpi(models.Model):
    user = models.ForeignKey(User, verbose_name=_('ผู้ใช้งานที่ได้สิทธิ์แก้ไข'), on_delete=models.RESTRICT, null=True, blank=True)
    year = models.PositiveSmallIntegerField(default=timezone.now().year + 543, verbose_name=_('ปีงบประมาณ'))
    ordering = models.PositiveSmallIntegerField(default=1, verbose_name=_('ลำดับ')) # เลขลำดับน้อยกว่าจะแสดงก่อน เท่ากันจะเรียงตามชื่อ
    name = models.CharField(max_length=255, verbose_name=_('ชื่อตัวชี้วัด'))
    group = models.ForeignKey(KpiGroup, on_delete=models.RESTRICT, verbose_name=KpiGroup._meta.verbose_name)
    level = models.ForeignKey(KpiLevel, on_delete=models.RESTRICT, verbose_name=KpiLevel._meta.verbose_name)
    goal = models.TextField(verbose_name=_('เป้าหมาย')) # รายละเอียดเป้าหมาย
    # ลิงค์ API ของ HDC "https://opendata.moph.go.th/api/report_data" 
    # หากว่างจะหมายถึงกรอกข้อมูลเอง ตรวจสอบรายการ API ที่ "https://opendata.moph.go.th/th/services/summary-table"
    hdc = models.URLField(verbose_name=_('hdc api endpoint'))
    quarter = models.PositiveSmallIntegerField(verbose_name=_('ไตรมาส'), choices=((1, '1'), (2, '2'), (3, '3'), (4, '4')))
    # ชื่อย่อตัวแปร(A-Z), ชื่อเต็มตัวแปร(รวมหน่วย), ค่าคงที่(บังคับค่าต้องเหมือนกันทุกไตรมาศ)
    # variables = models.JSONField(verbose_name=_('ตัวแปร'))
    formula = models.CharField(max_length=255, verbose_name=_('สูตรคำนวณรวม'), null=True, blank=True)
    result = models.FloatField(verbose_name=_('ผลลัพธ์'), default=0)
    expect = models.FloatField(verbose_name=_('ผลที่คาดหวัง'), default=0)
    # สูตรรวมไตรมาส 4 ต้องคำนวณไตรมาส 3, 2 และ 1 รวมกัน เป็นต้น
    accumulate_formula = models.CharField(max_length=255, verbose_name=_('สูตรรวมจากไตรมาสก่อน'), null=True, blank=True)
    # วิธีเปรียบเทียบ KPI ที่คาดหวังและผลลัพธ์ที่ได้ในไตรมาสนี้
    operator = models.CharField(
        max_length=2,
        verbose_name=_('วิธีเปรียบเทียบ KPI'),
        choices=(
            ('=', '='),
            ('>', '>'),
            ('>=', '>='),
            ('<', '<'),
            ('<=', '<='),
        ),
        null=True,
        blank=True,
    ) 
    # หน่วยการประเมิน เช่น อัตรา, ร้อยละ, ขั้นตอน เป็นต้น
    unit = models.CharField(max_length=100, verbose_name=_('หน่วยวัด'), null=True, blank=True)
    pdf = models.FileField(verbose_name=_('ไฟล์นิยามตัวชี้วัด'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('สร้างเมื่อ'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('อัพเดตเมื่อ'))
    
    class Meta:
        verbose_name = _('การประเมิน')
        verbose_name_plural = _('การประเมิน')
        db_table_comment = _('ผลการประเมินแบ่งตามปี และไตรมาส')
        unique_together = [['year', 'quarter']] # each year must only have 4 unique quarter


class Variable(models.Model):
    """Variables used in formula field in Kpi model"""
    name = models.CharField(max_length=255, verbose_name=_('ชื่อตัวแปร'))
    display_name = models.CharField(max_length=100, verbose_name=_('ชื่อที่แสดงในตาราง'))
    value = models.FloatField(verbose_name=_('ค่าตัวแปร'), default=0)
    is_constant = models.BooleanField(default=False, verbose_name=_('เป็นค่าคงที่')) # ถ้าจริง ไตรมาส 1 - 4 ต้องเป็นค่าเดียวกัน
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('สร้างเมื่อ'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('อัพเดตเมื่อ'))
    
    class Meta:
        verbose_name = _('ตัวแปร')
        verbose_name_plural = _('ตัวแปร')
        db_table_comment = _('ตัวแปรสำหรับใช้ในสูตรประมวลผลตาราง Kpi')