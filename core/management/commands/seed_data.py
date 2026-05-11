from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import WorkerSkill, WorkerStats
from jobs.models import Job
from messaging.models import Conversation, Message
from payments.models import PaymentRecord, PaymentTransaction
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed GaonKaam with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding demo data...')

        # Create users
        users_data = [
            {'username': 'ram_shrestha', 'first_name': 'Ram', 'last_name': 'Shrestha',
             'phone': '9841234567', 'district': 'sindhupalchok', 'village': 'Bhumidanda',
             'role': 'both', 'rating': Decimal('4.8'), 'total_reviews': 23},
            {'username': 'hari_tamang', 'first_name': 'Hari Bahadur', 'last_name': 'Tamang',
             'phone': '9812345678', 'district': 'sindhupalchok', 'village': 'Thulosirubari',
             'role': 'worker', 'rating': Decimal('4.5'), 'total_reviews': 11},
            {'username': 'sita_rai', 'first_name': 'Sita', 'last_name': 'Rai',
             'phone': '9823456789', 'district': 'nuwakot', 'village': 'Dupcheshwar',
             'role': 'employer', 'rating': Decimal('4.7'), 'total_reviews': 8},
            {'username': 'maya_gurung', 'first_name': 'Maya', 'last_name': 'Gurung',
             'phone': '9834567890', 'district': 'kavrepalanchok', 'village': 'Banepa',
             'role': 'worker', 'rating': Decimal('4.3'), 'total_reviews': 5},
            {'username': 'bikram_magar', 'first_name': 'Bikram', 'last_name': 'Magar',
             'phone': '9845678901', 'district': 'makwanpur', 'village': 'Hetauda',
             'role': 'both', 'rating': Decimal('4.6'), 'total_reviews': 14},
        ]
        created_users = []
        for ud in users_data:
            user, created = User.objects.get_or_create(username=ud['username'], defaults=ud)
            if created:
                user.set_password('demo1234')
                user.save()
                self.stdout.write(f'  ✅ Created user: {user.username}')
            WorkerStats.objects.get_or_create(user=user)
            created_users.append(user)

        ram, hari, sita, maya, bikram = created_users

        # Skills
        skill_map = [
            (ram, ['farming', 'construction', 'irrigation', 'loading']),
            (hari, ['farming', 'irrigation', 'loading']),
            (sita, ['domestic', 'cooking']),
            (maya, ['farming', 'craft']),
            (bikram, ['construction', 'carpentry', 'loading', 'driving']),
        ]
        for user, skills in skill_map:
            for s in skills:
                WorkerSkill.objects.get_or_create(user=user, skill=s)

        # Jobs
        jobs_data = [
            {'posted_by': ram, 'title': 'Wheat Harvest Help Needed', 'description': 'Need 5 experienced workers for wheat harvest. Work starts at 6 AM, includes lunch. Bring own sickle. Payment daily in cash.',
             'work_type': 'farming', 'status': 'urgent', 'village': 'Bhumidanda', 'district': 'Sindhupalchok',
             'daily_wage': 800, 'workers_needed': 5, 'workers_filled': 2, 'duration': '3 days', 'meals_provided': True, 'tools_required': True},
            {'posted_by': sita, 'title': 'House Construction – Brick Layer', 'description': 'Building 2-storey house. Need experienced brick layers. Tools and accommodation provided.',
             'work_type': 'construction', 'status': 'open', 'village': 'Melamchi', 'district': 'Sindhupalchok',
             'daily_wage': 1100, 'workers_needed': 3, 'workers_filled': 1, 'duration': '2 weeks', 'transport_provided': True},
            {'posted_by': sita, 'title': 'Potato Plantation & Field Prep', 'description': 'Large potato field needs planting. Experience with terraced farming preferred.',
             'work_type': 'farming', 'status': 'urgent', 'village': 'Dupcheshwar', 'district': 'Nuwakot',
             'daily_wage': 900, 'workers_needed': 8, 'workers_filled': 3, 'duration': '1 week', 'meals_provided': True},
            {'posted_by': bikram, 'title': 'Road Material Loading & Unloading', 'description': 'Loading gravel and cement bags for road construction project. Hard physical work, good pay.',
             'work_type': 'loading', 'status': 'open', 'village': 'Banepa', 'district': 'Kavrepalanchok',
             'daily_wage': 850, 'workers_needed': 10, 'workers_filled': 4, 'duration': '2 days'},
            {'posted_by': ram, 'title': 'Irrigation Ditch Digging', 'description': 'Digging new irrigation channel for rice fields. 200m total. Need strong workers with own spades.',
             'work_type': 'irrigation', 'status': 'urgent', 'village': 'Thulosirubari', 'district': 'Sindhupalchok',
             'daily_wage': 750, 'workers_needed': 6, 'workers_filled': 1, 'duration': '5 days'},
            {'posted_by': sita, 'title': 'Domestic Cook & Helper', 'description': 'Looking for experienced cook and domestic helper for family of 5. Live-in option available.',
             'work_type': 'domestic', 'status': 'open', 'village': 'Bhotang', 'district': 'Sindhupalchok',
             'daily_wage': 700, 'workers_needed': 1, 'workers_filled': 0, 'duration': 'Long-term'},
            {'posted_by': bikram, 'title': 'Carpenter for Roof Framing', 'description': 'Experienced carpenter needed for traditional style roof framing. Must have own tools.',
             'work_type': 'carpentry', 'status': 'open', 'village': 'Hetauda', 'district': 'Makwanpur',
             'daily_wage': 1300, 'workers_needed': 2, 'workers_filled': 0, 'duration': '10 days'},
        ]
        created_jobs = []
        for jd in jobs_data:
            job, created = Job.objects.get_or_create(title=jd['title'], posted_by=jd['posted_by'], defaults={k: v for k, v in jd.items() if k != 'title'})
            if created:
                self.stdout.write(f'  ✅ Created job: {job.title}')
            created_jobs.append(job)

        # Conversations & Messages
        if not Conversation.objects.filter(participants=ram).filter(participants=hari).exists():
            conv = Conversation.objects.create(job=created_jobs[0])
            conv.participants.add(ram, hari)
            Message.objects.create(conversation=conv, sender=hari, content='Namaste! I saw your wheat harvest job. I have 5 years of farming experience. Can we discuss?')
            Message.objects.create(conversation=conv, sender=ram, content='Namaste Hari ji! Yes, we need 5 workers starting Thursday. Work is for 3 days.')
            Message.objects.create(conversation=conv, sender=hari, content='Perfect! I will bring 2 more friends. We will be there at 6 AM. Rs. 800/day confirmed? 🙏')
            Message.objects.create(conversation=conv, sender=ram, content='Yes confirmed! Rs. 800 per day including lunch. See you Thursday morning.')
            self.stdout.write('  ✅ Created conversation between Ram and Hari')

        if not Conversation.objects.filter(participants=ram).filter(participants=sita).exists():
            conv2 = Conversation.objects.create(job=created_jobs[1])
            conv2.participants.add(ram, sita)
            Message.objects.create(conversation=conv2, sender=sita, content='Hello Ram ji! We need a brick layer for house construction in Melamchi. Are you available?')
            Message.objects.create(conversation=conv2, sender=ram, content='Namaste! Yes I am available. I have experience with traditional stone and brick construction.')
            self.stdout.write('  ✅ Created conversation between Ram and Sita')

        # Payment records
        if not PaymentRecord.objects.filter(worker=hari, job=created_jobs[0]).exists():
            p = PaymentRecord.objects.create(
                job=created_jobs[0], worker=hari, employer=ram,
                total_amount=Decimal('2400'), amount_paid=Decimal('2400'),
                days_worked=3, daily_rate=Decimal('800'),
                status='paid', payment_method='cash'
            )
            PaymentTransaction.objects.create(payment_record=p, amount=Decimal('2400'), method='cash', note='Full payment after 3 days harvest work')
            stats, _ = WorkerStats.objects.get_or_create(user=hari)
            stats.jobs_completed += 1
            stats.total_earned += Decimal('2400')
            stats.save()
            self.stdout.write('  ✅ Created payment record')

        # Admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@gaonkaam.np', 'admin123')
            admin.first_name = 'Admin'
            admin.last_name = 'GaonKaam'
            admin.save()
            WorkerStats.objects.create(user=admin)
            self.stdout.write('  ✅ Created admin user (admin / admin123)')

        self.stdout.write(self.style.SUCCESS('\n🎉 Demo data seeded successfully!\n'))
        self.stdout.write('Demo accounts (password: demo1234):')
        self.stdout.write('  👤 ram_shrestha  – Worker & Employer')
        self.stdout.write('  👤 hari_tamang   – Worker')
        self.stdout.write('  👤 sita_rai      – Employer')
        self.stdout.write('  👤 bikram_magar  – Both')
        self.stdout.write('  🔑 admin / admin123 – Django Admin\n')
