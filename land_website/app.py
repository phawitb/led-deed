from flask import Flask
from folium import plugins
import folium
# import matplotlib.pyplot as plt
import random
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    # start_coords = (46.9540700, 142.7360300)
    # folium_map = folium.Map(location=start_coords, zoom_start=14)

    # df = pd.read_csv('data/data_gps.csv', delimiter ='|')
    df = pd.read_csv('https://raw.githubusercontent.com/phawitb/led-deed/main/land_website/data/data_gps.csv', delimiter ='|')
    df['label'] = df['link']
    deed_map = make_map(df)  #lat,long,type_prop,label

    return deed_map._repr_html_()

def int_to_number(a):
    a = str(a).split('.')[0]
    x = [a[-9:-6],a[-6:-3],a[-3:]]
    z = ''
    for index,i in enumerate(x):
        if i != '':
            z += i 
            if index != 2:
                z+=','
    return z 

def make_map(df):
    latitude = df['lat'].mean()
    longitude = df['long'].mean()

    deed_map = folium.Map(location = [latitude, longitude], zoom_start = 12)

    #creat group
    colors = [
        'red',
        'blue',
        'gray',
        'darkred',
        'lightred',
        'orange',
        'beige',
        'green',
        'darkgreen',
        'lightgreen',
        'darkblue',
        'lightblue',
        'purple',
        'darkpurple',
        'pink',
        'cadetblue',
        'lightgray',
        'black'
    ]
    list_group = df['type_prop'].unique().tolist()
#     list_colors = [ random.choice(colors) for i in range(len(list_group))]
    list_colors = ['blue','red','darkgreen','gray']
    groups = {}
    for group in list_group:
        groups[group] = folium.FeatureGroup(name=group).add_to(deed_map)

    
    folium.TileLayer(
      tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      attr = 'Esri',
      name = 'Satellite',
      ).add_to(deed_map)
    
    folium.TileLayer('openstreetmap').add_to(deed_map)
    folium.LayerControl().add_to(deed_map)

    for index, row in df.iterrows():
        def find_last_sta(bit_texts):
            def find_avi(bit_texts):
                for i,bit_text in enumerate(bit_texts):
                    for s in ['คลิกเข้าร่วม','ขายได้']:
                        if s in bit_text:
                            return s,bit_text

                return None,None

            def find_sta(bit_texts):
                for i,bit_text in enumerate(bit_texts):
                    stas = ['ถอนการยึด','งดขายส่งประกาศมิชอบ','งดขายไม่มีผู้สู้ราคา','โจทก์แถลงงดขาย','เจ้าพนักงานงดขาย','งดขาย','ขายได้']
                    for s in stas:
                        if s in bit_text:
                            return s,bit_text

                return None,None

            a,b = find_avi(bit_texts)
            if not a:
                bit_texts.reverse()
                a,b = find_sta(bit_texts)  
            return a,b.split()[0],b.split()[1]
        
        bit_texts = [row['bit_time1'],row['bit_time2'],row['bit_time3'],row['bit_time4'],row['bit_time5'],row['bit_time6']]
        staus,staus_no,staus_date = find_last_sta(bit_texts)

        lng = row['long']
        lat = row['lat']
        group = row['type_prop']
        label = row['label']
        price = int_to_number(row['price'])
        insta_post = row['label']+'#lg=1&slide=0'
        website = row['label']
        direction = f"https://www.google.co.th/maps/search/{row['lat']},+{row['long']}"
        size = [row['size1'],row['size2'],row['size3']]

        pub_html = folium.Html(f"""<p style="text-align: center;"><span style="font-family: Didot, serif; font-size: 21px;"></span></p>
        <p style="text-align: center;"><iframe src={insta_post}embed width="380" height="220" frameborder="0" scrolling="false" allowtransparency="true"></iframe>
        <p style="text-align: center;"><a href={website} target="_blank" title="website"><span style="font-family: Didot, serif; font-size: 17px;">{group} {size[0]}ไร่ {size[1]}งาน {size[2]}ตร.วา</span></a></p>
         <p style="text-align: center;"><a href={direction} target="_blank" title="นำทาง"><span style="font-family: Didot, serif; font-size: 17px;">Status: {staus} นัด {staus_no} {staus_date}</span></a></p>
        <p style="text-align: center;"><a href={direction} target="_blank" title="นำทาง"><span style="font-family: Didot, serif; font-size: 17px;">{price} บาท</span></a></p>
        """, script=True)
        popup = folium.Popup(pub_html, max_width=700)

        if str(lat)!='nan':
            n = list_group.index(group)
            color = list_colors[n]
        
            if staus == "คลิกเข้าร่วม":
                color_border = 'yellow'
                fill_opacity = 0.8
            else:
                color_border = 'grey'
                fill_opacity = 0.2
                
            if group=='ที่ดินพร้อมสิ่งปลูกสร้าง' and int(row['size1'])==0 and int(row['size2'])==0 and int(row['size3'])<40:
                color = 'purple'

            groups[group].add_child(
                folium.CircleMarker(
                     [lat, lng],
                     radius=7, 
                     color=color_border,
                     fill=True,
                     fill_color=color,
                     fill_opacity=fill_opacity,
                     popup=popup
                 )
            )
        
    return deed_map



if __name__ == '__main__':
    app.run(debug=True)