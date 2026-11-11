import os
DATABASE_URL=os.getenv('DATABASE_URL','mysql+pymysql://balance:balance_demo_2026@localhost:17719/sample_balance')
REDIS_URL=os.getenv('REDIS_URL','redis://localhost:6379/0')
JWT_SECRET=os.getenv('JWT_SECRET','balance-local-demo-change-before-sharing')
