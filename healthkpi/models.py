from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class HealthZone(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('ชื่อเขตบริการสุขภาพ'))
    en_name = models.CharField(max_length=100, verbose_name=_('ชื่อภาษาอังกฤษ'))
    code = models.CharField(max_length=2, verbose_name=_('รหัสเขตบริการสุขภาพ'))
    
    class Meta:
        verbose_name = _('เขตบริการสุขภาพ')
        verbose_name_plural = _('เขตบริการสุขภาพ')
        db_table_comment = _('เขตบริการสุขภาพ')

    def __str__(self) -> str:
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('ชื่อภูมิภาค'))
    en_name = models.CharField(max_length=100, verbose_name=_('ชื่อภาษาอังกฤษ'))
    code = models.CharField(max_length=1, verbose_name=_('รหัสภูมิภาค'))
    
    class Meta:
        verbose_name = _('ภูมิภาค')
        verbose_name_plural = _('ภูมิภาค')
        db_table_comment = _('ภูมิภาค')

    def __str__(self) -> str:
        return self.name

class Province(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('ชื่อจังหวัด'))
    en_name = models.CharField(max_length=100, verbose_name=_('ชื่อภาษาอังกฤษ'), null=True, blank=True)
    code = models.CharField(max_length=2, verbose_name=_('รหัสจังหวัด'))
    region = models.ForeignKey(Region, on_delete=models.RESTRICT, verbose_name=Region._meta.verbose_name)
    health_zone = models.ForeignKey(HealthZone, on_delete=models.RESTRICT, verbose_name=HealthZone._meta.verbose_name)

    class Meta:
        verbose_name = _('จังหวัด')
        verbose_name_plural = _('จังหวัด')
        db_table_comment = _('จังหวัด')

    def __str__(self) -> str:
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('ขื่ออำเภอ'))
    en_name = models.CharField(max_length=100, verbose_name=_('ชื่อภาษาอังกฤษ'), null=True, blank=True)
    code = models.CharField(max_length=4, verbose_name=_('รหัสอำเภอ'))
    province = models.ForeignKey(Province, on_delete=models.RESTRICT, verbose_name=Province._meta.verbose_name)
    
    class Meta:
        verbose_name = _('อำเภอ')
        verbose_name_plural = _('อำเภอ')
        db_table_comment = _('อำเภอ')

    def __str__(self) -> str:
        return self.name


class SubDistrict(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('ขื่อตำบล'))
    en_name = models.CharField(max_length=100, verbose_name=_('ชื่อภาษาอังกฤษ'), null=True, blank=True)
    code = models.CharField(max_length=6, verbose_name=_('รหัสตำบล'))
    district = models.ForeignKey(District, on_delete=models.RESTRICT, verbose_name=District._meta.verbose_name)
    
    class Meta:
        verbose_name = _('ตำบล')
        verbose_name_plural = _('ตำบล')
        db_table_comment = _('ตำบล')

    def __str__(self) -> str:
        return self.name


class KpiGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('ชื่อกลุ่ม'), unique=True)
    abbr = models.CharField(max_length=100, verbose_name=_('ชื่อย่อ'), null=True, blank=True)
    en_name = models.CharField(max_length=255, verbose_name=_('ชื่ออังกฤษ'), null=True, blank=True)

    class Meta:
        verbose_name = _('ชื่อกลุ่มการประเมิน')
        verbose_name_plural = _('ชื่อกลุ่มการประเมิน')
        db_table_comment = _('ชื่อกลุ่มการประเมิน หรือ 4E')
    
    def __str__(self) -> str:
        return self.name


class KpiLevel(models.Model):
    """
    ระดับของ KPI โดยปัจจุบันได้แบ่งเป็นรายการต่อไปนี้
        ประเทศ, รายจังหวัด, เขตสุขภาพ, กระทรวงสาธารณสุข, กรมในสาสุข และ สป.สธ.
    """
    name = models.CharField(max_length=255, verbose_name=_('ชื่อ'), unique=True)
    code = models.CharField(max_length=5, verbose_name=_('รหัส'), unique=True)
    
    class Meta:
        verbose_name = _('ระดับการประเมิน')
        verbose_name_plural = _('ระดับการประเมิน')
        db_table_comment = _('ระดับการประเมิน เช่น ระดับเขตสุขภาพ หรือระดับจังหวัด เป็นต้น')

    def __str__(self) -> str:
        return self.name

class Kpi(models.Model):
    """
    ordering:
        เลขลำดับน้อยกว่าจะแสดงก่อน เท่ากันจะเรียงตามชื่อ
    goal:
        รายละเอียดเป้าหมาย, ลิงค์ API ของ HDC "https://opendata.moph.go.th/api/report_data" 
        หากว่างจะหมายถึงกรอกข้อมูลเอง ตรวจสอบรายการ API ที่ "https://opendata.moph.go.th/th/services/summary-table"
    formula:
        ชื่อย่อตัวแปร(A-Z), ชื่อเต็มตัวแปร(รวมหน่วย), ค่าคงที่(บังคับค่าต้องเหมือนกันทุกไตรมาศ)
    accumulate_formula:
        สูตรรวมไตรมาส 4 ต้องคำนวณไตรมาส 3, 2 และ 1 รวมกัน เป็นต้น
    operator:
        วิธีเปรียบเทียบ KPI ที่คาดหวังและผลลัพธ์ที่ได้ในไตรมาสนี้
    unit:
        หน่วยการประเมิน เช่น อัตรา, ร้อยละ, ขั้นตอน เป็นต้น
    """
    user = models.ForeignKey(User, verbose_name=_('ผู้ใช้งานที่ได้สิทธิ์แก้ไข'), on_delete=models.RESTRICT, null=True, blank=True)
    year = models.PositiveSmallIntegerField(default=timezone.now().year + 543, verbose_name=_('ปีงบประมาณ'))
    ordering = models.PositiveSmallIntegerField(default=1, verbose_name=_('ลำดับ'))
    name = models.CharField(max_length=255, verbose_name=_('ชื่อตัวชี้วัด'))
    group = models.ForeignKey(KpiGroup, on_delete=models.RESTRICT, verbose_name=KpiGroup._meta.verbose_name)
    level = models.ForeignKey(KpiLevel, on_delete=models.RESTRICT, verbose_name=KpiLevel._meta.verbose_name)
    goal = models.TextField(verbose_name=_('เป้าหมาย'))
    hdc = models.URLField(verbose_name=_('hdc api endpoint'))
    quarter = models.PositiveSmallIntegerField(verbose_name=_('ไตรมาส'), choices=((1, '1'), (2, '2'), (3, '3'), (4, '4')))
    formula = models.CharField(max_length=255, verbose_name=_('สูตรคำนวณรวม'), null=True, blank=True)
    result = models.FloatField(verbose_name=_('ผลลัพธ์'), default=0)
    expect = models.FloatField(verbose_name=_('ผลที่คาดหวัง'), default=0)
    accumulate_formula = models.CharField(max_length=255, verbose_name=_('สูตรรวมจากไตรมาสก่อน'), null=True, blank=True)
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
    unit = models.CharField(max_length=100, verbose_name=_('หน่วยวัด'), null=True, blank=True)
    pdf = models.FileField(verbose_name=_('ไฟล์นิยามตัวชี้วัด'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('สร้างเมื่อ'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('อัพเดตเมื่อ'))
    
    class Meta:
        verbose_name = _('การประเมิน')
        verbose_name_plural = _('การประเมิน')
        db_table_comment = _('ผลการประเมินแบ่งตามปี และไตรมาส')
        unique_together = [['year', 'quarter']] # each year must only have 4 unique quarter

    def __str__(self) -> str:
        return self.name
    

class Variable(models.Model):
    """Variables used in formula field in Kpi model"""
    name = models.CharField(max_length=255, verbose_name=_('ชื่อตัวแปร'))
    display_name = models.CharField(max_length=100, verbose_name=_('ชื่อที่แสดงในตาราง'))
    value = models.FloatField(verbose_name=_('ค่าตัวแปร'), default=0)
    is_constant = models.BooleanField(default=False, verbose_name=_('เป็นค่าคงที่')) # if true, quarter 1 - 4 must have the same value
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('สร้างเมื่อ'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('อัพเดตเมื่อ'))
    
    class Meta:
        verbose_name = _('ตัวแปร')
        verbose_name_plural = _('ตัวแปร')
        db_table_comment = _('ตัวแปรสำหรับใช้ในสูตรประมวลผลตาราง Kpi')
    
    def __str__(self) -> str:
        return self.name