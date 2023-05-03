import os
# os.environ['DATABASE_URL'] = 'postgresql://masters_app_user:AyvTx0G6KY0worz83Uw1UQRYghUJaLBl@dpg-ch955iukobicv5rll8ag-a.frankfurt-postgres.render.com/masters_app'

if str(os.getenv('HOME')).lower().find('users'):
    print(os.environ['USERNAME'])
    print(os.getenv('USERNAME'))
    print('ok')
else:
    print('pass')
# if str(getenv("HOME")).lower().find("users"):