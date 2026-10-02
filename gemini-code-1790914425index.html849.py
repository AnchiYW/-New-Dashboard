import pandas as pd
import plotly.express as px
import plotly.io as pio

# 1. นำเข้าและเตรียมข้อมูล (เลือกเฉพาะคอลัมน์ที่จำเป็นเพื่อความรวดเร็ว)
print("กำลังโหลดข้อมูล...")
df = pd.read_excel("confirmed-cases-since-271064.xlsx", usecols=['announce_date', 'sex', 'province_of_isolation'])

# จัดการค่าว่าง
df['province_of_isolation'] = df['province_of_isolation'].fillna('ไม่ระบุ')
df['sex'] = df['sex'].fillna('ไม่ระบุ')

# 2. สร้างกราฟต่างๆ ด้วย Plotly
print("กำลังสร้างกราฟ...")
# กราฟที่ 1: แนวโน้มผู้ป่วยรายวัน
daily_cases = df.groupby('announce_date').size().reset_index(name='cases')
fig_trend = px.line(daily_cases, x='announce_date', y='cases', 
                    title='แนวโน้มผู้ป่วยยืนยันรายวัน', 
                    labels={'announce_date': 'วันที่', 'cases': 'จำนวนผู้ป่วย'})

# กราฟที่ 2: แผนภูมิแท่ง 10 อันดับจังหวัดที่พบผู้ป่วยสูงสุด (จำลองแทนแผนที่เพื่อความรวดเร็วและแม่นยำ)
top_provinces = df['province_of_isolation'].value_counts().head(10).reset_index()
top_provinces.columns = ['province', 'cases']
fig_prov = px.bar(top_provinces, x='province', y='cases', 
                  title='10 อันดับจังหวัดที่พบผู้ป่วยสูงสุด', 
                  labels={'province': 'จังหวัด', 'cases': 'จำนวนผู้ป่วย'},
                  color='cases', color_continuous_scale='Reds')

# กราฟที่ 3: สัดส่วนผู้ป่วยตามเพศ
sex_dist = df['sex'].value_counts().reset_index()
sex_dist.columns = ['sex', 'cases']
fig_sex = px.pie(sex_dist, names='sex', values='cases', title='สัดส่วนผู้ป่วยตามเพศ', hole=0.4)

# 3. แปลงกราฟเป็น HTML elements
# โหลด Plotly.js มาจาก CDN แค่ครั้งเดียวในกราฟแรก กราฟต่อไปตั้งค่าเป็น False เพื่อลดขนาดไฟล์
trend_html = pio.to_html(fig_trend, full_html=False, include_plotlyjs='cdn')
prov_html = pio.to_html(fig_prov, full_html=False, include_plotlyjs=False)
sex_html = pio.to_html(fig_sex, full_html=False, include_plotlyjs=False)

# 4. ประกอบร่างเป็นหน้าเว็บเพจสมบูรณ์
dashboard_html = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Epidemiological Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Sarabun', sans-serif; margin: 0; padding: 20px; background-color: #f4f7f6; }}
        h1 {{ text-align: center; color: #2c3e50; margin-bottom: 30px; }}
        .container {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; max-width: 1200px; margin: 0 auto; }}
        .card {{ background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); padding: 20px; width: 45%; min-width: 300px; flex-grow: 1; }}
        .full-width {{ width: 100%; }}
        .footer {{ text-align: center; margin-top: 40px; color: #7f8c8d; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>📊 รายงานสถานการณ์โรคระบาดวิทยา (Dashboard)</h1>
    <div class="container">
        <div class="card full-width">
            {trend_html}
        </div>
        <div class="card">
            {prov_html}
        </div>
        <div class="card">
            {sex_html}
        </div>
    </div>
    <div class="footer">
        อัปเดตข้อมูลล่าสุดเมื่อ: {df['announce_date'].max().strftime('%d/%m/%Y')}
    </div>
</body>
</html>
"""

# บันทึกเป็นไฟล์ HTML
with open("index.html", "w", encoding="utf-8") as f:
    f.write(dashboard_html)

print("สร้างไฟล์ index.html สำเร็จ! พร้อมนำไปอัปโหลดขึ้น GitHub Pages แล้ว")
