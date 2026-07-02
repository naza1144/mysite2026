from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shopes.models import Category, Product


class Command(BaseCommand):
    help = 'Seed sample data for Shopes app'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Create categories
        categories = [
            ('อิเล็กทรอนิกส์', 'electronics'),
            ('แฟชั่น', 'fashion'),
            ('บ้านและสวน', 'home-garden'),
            ('สุขภาพและความงาม', 'beauty'),
            ('กีฬา', 'sports'),
            ('ของเล่น', 'toys'),
        ]

        for name, slug in categories:
            cat, created = Category.objects.get_or_create(name=name, slug=slug)
            if created:
                self.stdout.write(f'  Created category: {name}')

        # Create products
        products_data = [
            # Electronics
            ('หูฟังไร้สาย Bluetooth 5.3', 'headphone-bt53', 890, 50, 'electronics',
             'หูฟังไร้สายคุณภาพสูง รองรับ Bluetooth 5.3 เสียงคมชัด แบตเตอรี่ใช้งานได้นานถึง 30 ชั่วโมง'),
            ('Power Bank 20000mAh', 'powerbank-20000', 590, 30, 'electronics',
             'พาวเวอร์แบงค์ความจุ 20000mAh ชาร์จเร็ว รองรับ USB-C PD 20W'),
            ('ลำโพง Bluetooth พกพา', 'speaker-bt-portable', 450, 25, 'electronics',
             'ลำโพง Bluetooth ขนาดกะทัดรัด เสียงดัง กันน้ำ IPX7'),
            ('สายชาร์จ USB-C 1m', 'cable-usbc-1m', 99, 100, 'electronics',
             'สายชาร์จ USB-C คุณภาพดี ทนทาน รองรับชาร์จเร็ว'),
            ('เมาส์ไร้สาย', 'mouse-wireless', 350, 40, 'electronics',
             'เมาส์ไร้สาย Ergonomic เงียบ น้ำหนักเบา'),
            ('คีย์บอร์ด Bluetooth', 'keyboard-bt', 790, 20, 'electronics',
             'คีย์บอร์ด Bluetooth พับได้ ใช้กับมือถือและแท็บเล็ต'),

            # Fashion
            ('เสื้อยืดคอกลม Cotton', 'shirt-cotton-round', 250, 80, 'fashion',
             'เสื้อยืดคอกลม ผ้า Cotton 100% ใส่สบาย ระบายอากาศดี'),
            ('กางเกงยีนส์ขาตรง', 'jeans-straight', 690, 35, 'fashion',
             'กางเกงยีนส์ขาตรง ดีไซน์คลาสสิก ใส่ได้ทุกโอกาส'),
            ('รองเท้าผ้าใบแฟชั่น', 'sneakers-fashion', 890, 25, 'fashion',
             'รองเท้าผ้าใบสไตล์มินิมอล สวมใส่สบาย พื้นนุ่ม'),
            ('กระเป๋าสะพายข้าง', 'bag-crossbody', 450, 40, 'fashion',
             'กระเป๋าสะพายข้างหนังเทียม ดีไซน์เก๋ ใส่ของได้เยอะ'),
            ('หมวกแก็ป', 'cap-hat', 199, 60, 'fashion',
             'หมวกแก็ปผ้าฝ้าย ปรับขนาดได้ สีสันสดใส'),

            # Home & Garden
            ('กระถางต้นไม้เซรามิก', 'pot-ceramic', 180, 45, 'home-garden',
             'กระถางต้นไม้เซรามิกคุณภาพดี มีรูระบายน้ำ'),
            ('ชั้นวางของอเนกประสงค์', 'shelf-multipurpose', 1200, 15, 'home-garden',
             'ชั้นวางของ 5 ชั้น เหล็กเคลือบสี แข็งแรง รับน้ำหนักได้ดี'),
            ('โคมไฟตั้งโต๊ะ LED', 'lamp-desk-led', 350, 30, 'home-garden',
             'โคมไฟตั้งโต๊ะ LED ปรับแสงได้ 3 ระดับ ประหยัดไฟ'),
            ('พรมเช็ดเท้า', 'mat-doormat', 120, 70, 'home-garden',
             'พรมเช็ดเท้าผ้าไมโครไฟเบอร์ ซับน้ำได้ดี ล้างง่าย'),

            # Beauty
            ('เซรั่มวิตามินซี', 'serum-vitamin-c', 350, 40, 'beauty',
             'เซรั่มวิตามินซีเข้มข้น ช่วยให้ผิวกระจ่างใส ลดเลือนจุดด่างดำ'),
            ('ครีมกันแดด SPF50+', 'sunscreen-spf50', 290, 50, 'beauty',
             'ครีมกันแดดเนื้อบางเบา SPF50+ PA+++ ปกป้องผิวจากรังสี UVA/UVB'),
            ('ลิปสติกเนื้อแมท', 'lipstick-matte', 199, 60, 'beauty',
             'ลิปสติกเนื้อแมท ติดทนนาน สีสวย หลายเฉดสี'),
            ('แปรงแต่งหน้าเซ็ต 5 ชิ้น', 'brush-set-5pcs', 250, 35, 'beauty',
             'แปรงแต่งหน้าคุณภาพดี ขนนุ่ม ครบเซ็ตสำหรับแต่งหน้า'),

            # Sports
            ('เสื้อกีฬาผ้า Dry-Fit', 'shirt-dryfit', 299, 50, 'sports',
             'เสื้อกีฬาผ้า Dry-Fit ระบายเหงื่อดี สวมใส่สบาย'),
            ('เชือกกระโดด', 'jump-rope', 150, 40, 'sports',
             'เชือกกระโดดปรับความยาวได้ ด้ามจับโฟมนุ่ม'),
            ('ถุงมือฟิตเนส', 'gloves-fitness', 220, 30, 'sports',
             'ถุงมือฟิตเนสกันลื่น ป้องกันมือพอง'),
            ('ขวดน้ำกีฬา 750ml', 'water-bottle-750ml', 180, 55, 'sports',
             'ขวดน้ำกีฬาพลาสติก Tritan ปลอดสาร BPA ฝาเปิดง่าย'),

            # Toys
            ('ตุ๊กตาหมีนุ่ม', 'teddy-bear-soft', 350, 25, 'toys',
             'ตุ๊กตาหมีขนนุ่ม ขนาด 30 ซม. น่ากอด'),
            ('บล็อกไม้ต่อรูป', 'wooden-blocks', 280, 20, 'toys',
             'บล็อกไม้ต่อรูป 100 ชิ้น เสริมสร้างจินตนาการ'),
            ('รถของเล่นบังคับ', 'rc-car', 450, 15, 'toys',
             'รถของเล่นบังคับวิทยุ ความเร็วสูง แบตเตอรี่ชาร์จได้'),
        ]

        for name, slug, price, stock, category_slug, description in products_data:
            cat = Category.objects.get(slug=category_slug)
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'price': price,
                    'stock': stock,
                    'category': cat,
                    'description': description,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Seeded {Category.objects.count()} categories and {Product.objects.count()} products!'))
