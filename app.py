
"""
RUANG TEDUH PERPUSTAKAAN LOKER DKI JAKARTA V7.0 FINAL - CLEAN
- Sesuai mapping lu: Loker menyeluruh umum - judul tema bebas - pembatasan cuma wilayah 5 DKI Pusat Barat Timur Selatan Utara
- NIK DKI 31xxxx only - radius 10km onsite only - cegah imigrasi berlebihan - jangan bogah keluar DKI
- NO TRACKING OPTIONAL - direct WA/Email - lebih simpel
- FIX: No st.components.v1.html - pakai st.html + st.iframe (anti warning 2026-06-01)
- 1 sender: jugalachaliveret@gmail.com / dual admin cinhonest@gmail.com + asuveleikha@gmail.com
- Voice Web Speech API GRATIS - instant
"""

import streamlit as st
from datetime import date, datetime
import json, os, urllib.parse, smtplib, math
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIG - SEO GOOGLE HOMEPAGE
st.set_page_config(
    page_title="Ruang Teduh Perpustakaan Loker DKI Jakarta - Loker Umum FNB Logistik Kantoran Garmen",
    page_icon="📚",
    layout="wide",
    menu_items={'About': "Ruang Teduh Perpustakaan = Loker Umum DKI Jakarta - Belum jadi Matahari - Fungsi ke masyarakat - Pembatasan cuma wilayah 5 DKI"}
)

# GOOGLE VERIFICATION - BIAR GOOGLE HOMEPAGE MAU INDEX - KODE LU: k1KCE7SRCPe0rg3Bkc0KhOkuLXdBIeQrlg0RUrjTAfM
st.html('<meta name="google-site-verification" content="k1KCE7SRCPe0rg3Bkc0KhOkuLXdBIeQrlg0RUrjTAfM" />')
st.html('<meta name="description" content="Ruang Teduh Perpustakaan Loker DKI Jakarta - Loker menyeluruh umum FNB Logistik Kantoran Garmen Retail - Judul bebas pembatasan cuma wilayah 5 DKI Pusat Barat Timur Selatan Utara - NIK 31xxxx Radius 10km Onsite Only" />')
st.html('<meta name="keywords" content="loker DKI Jakarta, loker Jakarta Pusat, loker Jakarta Barat, loker Jakarta Timur, loker Jakarta Selatan, loker Jakarta Utara, ruang teduh perpustakaan, loker FNB, loker logistik, loker kantoran, loker garmen" />')

# SESSION CLEAN
if "member_data" not in st.session_state:
    st.session_state.member_data = {}
if "bursa_total" not in st.session_state:
    st.session_state.bursa_total = 12
if "bursa_aktif" not in st.session_state:
    st.session_state.bursa_aktif = 8
if "bursa_kerja" not in st.session_state:
    st.session_state.bursa_kerja = 4
if "bursa_hist" not in st.session_state:
    st.session_state.bursa_hist = [
        {"jam": "08:00", "vote": 2, "kerja": 0, "total": 2},
        {"jam": "09:00", "vote": 5, "kerja": 1, "total": 6},
        {"jam": "10:00", "vote": 8, "kerja": 2, "total": 10},
        {"jam": "11:00", "vote": 8, "kerja": 4, "total": 12},
    ]
if "bursa_log" not in st.session_state:
    st.session_state.bursa_log = []

WILAYAH_DKI = ["Jakarta Pusat", "Jakarta Barat", "Jakarta Timur", "Jakarta Selatan", "Jakarta Utara"]
KATEGORI_UMUM = ["FNB", "Logistik", "Kantoran", "Garmen", "Retail & Sales", "Cleaning & Security", "Lainnya"]

# DKI BOUNDS - biar gak bogah keluar DKI
DKI_BOUNDS = {"lat_min": -6.360, "lat_max": -6.075, "lon_min": 106.680, "lon_max": 106.987}

def is_nik_dki(nik):
    return nik.startswith("31") and len(nik) >= 10

def add_login_bursa():
    st.session_state.bursa_total += 1
    st.session_state.bursa_aktif += 1
    now = datetime.now().strftime("%H:%M")
    st.session_state.bursa_hist.append({"jam": now, "vote": st.session_state.bursa_aktif, "kerja": st.session_state.bursa_kerja, "total": st.session_state.bursa_total})
    if len(st.session_state.bursa_hist) > 12:
        st.session_state.bursa_hist = st.session_state.bursa_hist[-12:]

def kurang_bursa_share(email, alasan="share email"):
    if st.session_state.bursa_aktif > 0:
        st.session_state.bursa_aktif -= 1
        st.session_state.bursa_kerja += 1
        now = datetime.now().strftime("%H:%M")
        st.session_state.bursa_hist.append({"jam": now, "vote": st.session_state.bursa_aktif, "kerja": st.session_state.bursa_kerja, "total": st.session_state.bursa_total})
        st.session_state.bursa_log.append({"waktu": now, "ke": email, "alasan": alasan})
        if len(st.session_state.bursa_hist) > 12:
            st.session_state.bursa_hist = st.session_state.bursa_hist[-12:]

# VOICE - FIX NO components.html - pakai st.html
def voice_input_dki(label_key="voice_dki"):
    st.markdown("#### 🎙 Cerita Pengalaman - GRATIS Web Speech API (Tanpa Key)")
    html = f"""
    <div style="background:#E8F5E9; border:2px solid #4CAF50; border-radius:12px; padding:12px;">
        <button id="btn_{label_key}" onclick="startRec_{label_key}()" style="background:#4CAF50; color:white; border:none; padding:10px 18px; border-radius:20px; font-weight:800; cursor:pointer;">🎤 Klik Bicara - DKI</button>
        <div id="result_{label_key}" style="margin-top:10px; background:white; padding:10px; border-radius:8px; min-height:40px; font-size:13px;">Hasil akan muncul - copy ke kolom pengalaman...</div>
    </div>
    <script>
    function startRec_{label_key}(){{
        var btn=document.getElementById('btn_{label_key}');
        var res=document.getElementById('result_{label_key}');
        if(!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)){{ res.innerHTML='Pakai Chrome!'; return; }}
        var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
        var rec=new SR(); rec.lang='id-ID'; rec.interimResults=true;
        btn.innerHTML='🔴 Mendengarkan...'; rec.start();
        rec.onresult=function(e){{ var t=e.results[0][0].transcript; res.innerHTML='<b>✅ '+t+'</b><br><small>Copy paste ke kolom pengalaman!</small>'; btn.innerHTML='🎤 Klik Lagi'; }};
        rec.onerror=function(e){{ res.innerHTML='Error:'+e.error; }};
        rec.onend=function(){{ btn.innerHTML='🎤 Klik untuk Bicara Lagi'; }};
    }}
    </script>
    """
    st.html(html)

# TTS - FIX NO components.html
def tts_voice_dki(text, role, key_id):
    clean = text.replace('"','').replace("'","").replace("\n"," ")[:280]
    if not clean: clean="Halo selamat datang di Ruang Teduh Perpustakaan DKI"
    js_txt = json.dumps(clean)
    if role=="emp": bg="#FFEBEE"; border="#FF5252"; label="EMPLOYEE DKI"
    elif role=="ent": bg="#E8F5E9"; border="#4CAF50"; label="ENTREPRENEUR DKI"
    else: bg="#FFF9C4"; border="#FBC02D"; label="STORAGE DKI"
    html = f"""
    <div style="background:{bg}; border:2px solid {border}; border-radius:12px; padding:12px;">
        <div style="font-weight:800; font-size:11px;">🔊 {label}</div>
        <div style="background:white; border-radius:8px; padding:8px; font-size:11px; max-height:60px; overflow:auto; margin:8px 0;">{clean[:150]}...</div>
        <button onclick="speak_{key_id}()" style="background:{border}; color:white; border:none; padding:10px; border-radius:8px; font-weight:800; cursor:pointer; width:100%;">🔊 PUTAR SUARA</button>
        <div id="st_{key_id}" style="font-size:9px; text-align:center; margin-top:6px;">Siap</div>
    </div>
    <script>
        function speak_{key_id}(){{
            if('speechSynthesis' in window){{
                window.speechSynthesis.cancel();
                var u=new SpeechSynthesisUtterance({js_txt});
                u.rate=1.1; u.lang='id-ID';
                u.onstart=function(){{document.getElementById('st_{key_id}').innerHTML='🔊 Berbicara...';}};
                u.onend=function(){{document.getElementById('st_{key_id}').innerHTML='✅ Selesai';}};
                window.speechSynthesis.speak(u);
            }}
        }}
    </script>
    """
    st.html(html)

# EMAIL DUAL ADMIN - FIX
def send_email_dki(subject, body, role="both"):
    try:
        sender_email = st.secrets["email"]["sender_email"]
        sender_password = st.secrets["email"]["sender_password"]
        admin1 = st.secrets["email"]["admin1"]
        admin2 = st.secrets["email"]["admin2"]
    except Exception as e:
        return False, f"Secrets [email] belum lengkap: {e}"
    if "qwer tyui" in sender_password or len(sender_password) < 12:
        return False, "❌ sender_password masih PALSU - ganti App Password 16 huruf asli!"
    smtp_server = "smtp.office365.com" if "outlook.com" in sender_email or "hotmail.com" in sender_email else "smtp.gmail.com"
    recipients = [admin1] if role=="employee" else [admin2] if role=="entrepreneur" else [admin1, admin2]
    try:
        server = smtplib.SMTP(smtp_server, 587, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        for to_email in recipients:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True, f"✅ Terkirim ke {', '.join(recipients)}"
    except Exception as e:
        return False, f"❌ Gagal SMTP: {e}"

def generate_cv_text_dki(md):
    return f"""CV KOMPLIT DKI - RUANG TEDUH PERPUSTAKAAN V7.0 - {md.get('nama','')} - {md.get('jabatan','')}
Nama: {md.get('nama','')}
NIK DKI: {md.get('nik','')} (harus 31xxxx)
Tempat Lahir: {md.get('tempat','')}
Tgl Lahir: {md.get('tgl','')}
Umur: {md.get('umur','')}
Pendidikan: {md.get('pendidikan','')}
Pengalaman: {md.get('pengalaman','')}
Skill: {md.get('skill','')}
Kategori: {md.get('kategori','')} (FNB/Logistik/Kantoran/Garmen dll - bebas)
Wilayah: {md.get('wilayah','')} (hanya 5 DKI - Pusat Barat Timur Selatan Utara)
Email: {md.get('email','')}
WA: {md.get('wa','')}
Jabatan: {md.get('jabatan','')}
Bursa: Total {st.session_state.bursa_total} Aktif {st.session_state.bursa_aktif} Kerja {st.session_state.bursa_kerja}
Mapping: Radius 10km onsite only - cegah imigrasi berlebihan - DKI only
"""

def generate_mailto_dki(md):
    subject = f"CV DKI - {md.get('nama','')} - {md.get('jabatan','')} - {md.get('wilayah','')}"
    body = generate_cv_text_dki(md)
    return f"mailto:{st.secrets.get('email',{}).get('admin1','cinhonest@gmail.com')},{st.secrets.get('email',{}).get('admin2','asuveleikha@gmail.com')}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

def render_grafik_dki():
    hist = st.session_state.bursa_hist
    if not hist: return
    max_v = max([h["vote"] for h in hist] + [h["kerja"] for h in hist] + [1])
    html_g = '<div style="display:flex; gap:8px; align-items:end; height:90px; background:white; border:1px solid #E0E0E0; border-radius:12px; padding:12px;">'
    for h in hist:
        v_h = int(h["vote"] / max_v * 65)
        k_h = int(h["kerja"] / max_v * 65)
        html_g += f'<div style="flex:1; text-align:center;"><div style="display:flex; gap:3px; justify-content:center; align-items:end; height:70px;"><div style="width:45%; background:#FF5252; height:{v_h}px; border-radius:4px;"></div><div style="width:45%; background:#4CAF50; height:{k_h}px; border-radius:4px;"></div></div><div style="font-size:8px; margin-top:5px; font-weight:700;">{h["jam"]}</div></div>'
    html_g += '</div><div style="font-size:9px; color:#666; margin-top:6px;">🔴 Aktif | 🟢 Kerja - Grafik hanya di Putih - Kuning tanpa grafik hemat kuota</div>'
    st.html(html_g)

# STYLE
st.html("""
<style>
.lembar{border-radius:14px; padding:20px; margin-bottom:16px; border-left:4px dashed #bbb; background:white; box-shadow:2px 2px 8px rgba(0,0,0,0.06);}
.lembar-putih{border-top:5px solid #424242;}
.lembar-merah{background:#FFEBEE; border-top:5px solid #FF5252;}
.lembar-hijau{background:#E8F5E9; border-top:5px solid #4CAF50;}
.lembar-kuning{background:linear-gradient(135deg, #FFFDE7, #FFF9C4); border-top:5px solid #FBC02D;}
</style>
""")

st.html("""
<div style="text-align:center; padding:8px 0 12px 0;">
    <div style="font-size:10px; letter-spacing:2px; color:#888; font-weight:700;">RUANG TEDUH PERPUSTAKAAN LOKER DKI V7.0 - BELUM JADI MATAHARI - FUNGSI KE MASYARAKAT DKI - 5 WILAYAH ONLY</div>
    <div style="font-size:20px; font-weight:900;">📚 RUANG TEDUH PERPUSTAKAAN - LOKER MENYELURUH DKI JAKARTA - V7.0 FINAL CLEAN</div>
    <div style="font-size:10px; background:#1565C0; color:white; display:inline-block; padding:4px 12px; border-radius:20px; font-weight:800;">Judul Bebas | Pembatasan Cuma Wilayah 5 DKI Pusat Barat Timur Selatan Utara | NIK 31xxxx | Radius 10km Onsite Only | No Tracking Optional</div>
</div>
""")

# BURSA TOP
c1,c2,c3,c4 = st.columns(4)
c1.metric("TOTAL LOGIN", st.session_state.bursa_total)
c2.metric("BURSA AKTIF", st.session_state.bursa_aktif)
c3.metric("SUDAH KERJA", st.session_state.bursa_kerja)
persen = int(st.session_state.bursa_kerja/st.session_state.bursa_total*100) if st.session_state.bursa_total else 0
c4.metric("KONVERSI", f"{persen}%")

tab1, tab2, tab3, tab4 = st.tabs(["📄 PUTIH - FORM LOKER DKI + GRAFIK", "🔴 MERAH - EMPLOYEE DKI", "🟢 HIJAU - ENTREPRENEUR DKI", "📜 KUNING - STORAGE - NO GRAFIK"])

with tab1:
    st.html('<div class="lembar lembar-putih"><b>LEMBAR 1 - FORM LOKER DKI JAKARTA - JUDUL BEBAS - WILAYAH ONLY 5 DKI</b><br><small>Mapping: DKI Bounds lat -6.360 to -6.075 lon 106.680 to 106.987 | NIK harus 31xxxx | Radius 10km onsite only | Grafik hanya di sini</small></div>')
    st.markdown("#### 📈 Grafik Bursa - Hanya di Putih")
    render_grafik_dki()
    st.divider()
    voice_input_dki("pengalaman_dki")
    with st.form("form_dki_final"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap *", placeholder="Budi Setia")
            nik = st.text_input("NIK DKI * harus 31xxxx", placeholder="3171xxxxxxxxxxxx - wajib DKI")
        with col2:
            jabatan = st.selectbox("Jabatan *", ["Staff", "Supervisor", "Manager", "Brand Manager", "Usahawan / Entrepreneur"])
            wilayah = st.selectbox("Wilayah DKI * hanya 5 ini", WILAYAH_DKI)
        col3, col4 = st.columns(2)
        with col3:
            tempat = st.text_input("Tempat Lahir *", placeholder="Jakarta Barat")
            kategori = st.selectbox("Kategori Loker * bebas", KATEGORI_UMUM)
        with col4:
            tgl = st.date_input("Tgl Lahir *", value=date(1994,9,21))
        pendidikan = st.text_input("Pendidikan *", placeholder="S1 Akuntansi Trisakti")
        pengalaman = st.text_area("Pengalaman Kerja * bebas", placeholder="2020-2023 Auditor PT XYZ - bebas judul tema", height=85)
        skill = st.text_area("Skill * bebas di bawah pengalaman", placeholder="akuntansi, ERP, Excel - bebas", height=70)
        col5, col6 = st.columns(2)
        with col5:
            email = st.text_input("Email *", placeholder="cinhonest@gmail.com")
        with col6:
            wa = st.text_input("WA *", placeholder="081291904422")
        judul_bebas = st.text_input("Judul Loker Bebas * - tidak dibatasi", placeholder="Butuh Barista Jago Latte Art Jakarta Pusat - bebas tema")
        submit = st.form_submit_button("✅ SIMPAN CV DKI & MASUK BURSA - FINAL CLEAN", type="primary", use_container_width=True)
        if submit:
            if not nama or not nik or not is_nik_dki(nik):
                st.error("NIK harus DKI 31xxxx bro - mapping DKI only - jangan bogah keluar DKI!")
            elif not tempat or not email or not wa or not pengalaman:
                st.error("Lengkapi * bro - wajib CV komplit")
            else:
                is_emp = jabatan in ["Staff", "Supervisor"]
                st.session_state.member_data = {
                    "nama": nama, "nik": nik, "jabatan": jabatan, "wilayah": wilayah, "kategori": kategori,
                    "is_emp": is_emp, "is_ent": not is_emp,
                    "tempat": tempat, "tgl": tgl.strftime("%d-%m-%Y"), "umur": date.today().year - tgl.year,
                    "email": email, "wa": wa, "pendidikan": pendidikan,
                    "pengalaman": pengalaman, "skill": skill, "judul_bebas": judul_bebas
                }
                add_login_bursa()
                st.success(f"✅ CV DKI {nama} {wilayah} masuk Bursa! Total {st.session_state.bursa_total} Aktif {st.session_state.bursa_aktif}")
                st.balloons()
                md = st.session_state.member_data
                st.code(generate_cv_text_dki(md), language="text")
                st.link_button("📧 KIRIM CV DKI KE ADMIN", generate_mailto_dki(md), type="primary", use_container_width=True)

with tab2:
    st.html('<div class="lembar lembar-merah"><b>LEMBAR 2 - EMPLOYEE DKI - Staff & Supervisor - CV KOMPLIT DKI</b></div>')
    md = st.session_state.member_data if st.session_state.member_data else {"nama":"Contoh Budi","jabatan":"Staff","wilayah":"Jakarta Pusat","nik":"3171xxxx","tempat":"Jakarta Barat","tgl":"21-09-1994","umur":31,"email":"contoh@email.com","wa":"0812","pendidikan":"S1","pengalaman":"Audit","skill":"ERP","kategori":"Kantoran","judul_bebas":"Butuh Admin"}
    st.html(f'<div style="background:#FFCDD2; padding:8px; border-radius:8px; font-size:11px; font-weight:700;">✅ {md["nama"]} | {md["jabatan"]} | {md["wilayah"]} | NIK {md.get("nik","")} | Kategori {md.get("kategori","")}</div>')
    col_k, col_k2 = st.columns([1.2,0.8])
    with col_k:
        st.markdown(f"**CV DKI:** {md['nama']} - {md['wilayah']} - {md.get('judul_bebas','')}")
        tts_voice_dki(f"CV DKI {md['nama']} wilayah {md['wilayah']} kategori {md.get('kategori','')} jabatan {md['jabatan']}", "emp", "emp_dki")
        st.code(generate_cv_text_dki(md), language="text")
    with col_k2:
        st.metric("Aktif", st.session_state.bursa_aktif)
        st.metric("Kerja", st.session_state.bursa_kerja)
        st.caption("Grafik hanya di Putih - Kuning tanpa grafik hemat kuota")
        st.html('<div style="background:#E8F5E9; border:2px solid #4CAF50; border-radius:12px; padding:10px; font-size:11px;"><b>✅ Jujur</b> - sudah kerja?</div>')
        if st.session_state.member_data:
            if st.checkbox("Sudah Kerja - Jujur", key="jujur_emp_dki"):
                kurang_bursa_share(md['email'], "Jujur Employee DKI")
                st.success("Bursa -1 - makasih jujur!")

with tab3:
    st.html('<div class="lembar lembar-hijau"><b>LEMBAR 3 - ENTREPRENEUR DKI - Manager Brand Usahawan - Mirror Merah</b></div>')
    md = st.session_state.member_data if st.session_state.member_data else {"nama":"Contoh Sari Manager","jabatan":"Manager","wilayah":"Jakarta Selatan","nik":"3171xxxx","tempat":"Jakarta","tgl":"21-09-1994","umur":31,"email":"manager@email.com","wa":"0812","pendidikan":"S1 Manajemen","pengalaman":"Manager 2018-2024","skill":"Leadership","kategori":"Kantoran","judul_bebas":"Lowongan Manager"}
    st.html(f'<div style="background:#C8E6C9; padding:8px; border-radius:8px; font-size:11px; font-weight:700;">✅ {md["nama"]} | {md["jabatan"]} | {md["wilayah"]} | Entrepreneur Mirror</div>')
    col_k, col_k2 = st.columns([1.2,0.8])
    with col_k:
        tts_voice_dki(f"Entrepreneur DKI {md['nama']} wilayah {md['wilayah']}", "ent", "ent_dki")
        st.code(generate_cv_text_dki(md), language="text")
    with col_k2:
        st.metric("Aktif", st.session_state.bursa_aktif)
        st.metric("Kerja", st.session_state.bursa_kerja)

with tab4:
    st.html('<div class="lembar lembar-kuning"><b>LEMBAR 4 - STORAGE - TANPA GRAFIK - HEMAT KUOTA - DKI ONLY</b><br><small>Putih ada grafik - Kuning storage aja tanpa grafik</small></div>')
    st.html("""
    <div style="background:white; border:1px solid #A5D6A7; border-radius:12px; padding:12px; font-size:11px;">
    <b>Mapping DKI Jakarta Only - 5 Wilayah:</b><br>
    Pusat Barat Timur Selatan Utara saja - jangan sampai keluar DKI - bisa bogah - NIK 31xxxx only - Radius 10km onsite only - WFH off karena Jakarta kecil padat - Pabrik urusan kabupaten - ini loker umum FNB Logistik Kantoran Garmen Retail Cleaning - judul bebas - pembatasan cuma wilayah.
    </div>
    """)
    st.html("""
    <div style="background:white; border:2px solid #FF5252; border-radius:12px; padding:12px; font-size:11px; margin-top:10px;">
    <b>IBM BOB 2.0 - Tahap demi tahap:</b><br>
    Fase 1 Sekarang: Ruang Teduh Perpustakaan = Loker DKI Jakarta - landing segera - fungsi ke masyarakat<br>
    Fase 2 Kompetisi: Rename jadi Ruang Teduh Pustaka Matahari = Loker + SaaS SCM ERP - segala macam bidang usaha bisnis utamanya ERP - manufakturing belakangan - dikit demi sedikit - 2x24 jam
    </div>
    """)

st.html(f"""
<div style="background:white; border-radius:12px; padding:12px; border:1px solid #eee; text-align:center; font-size:9px; margin-top:14px;">
<div style="background:#1565C0; color:white; display:inline-block; padding:5px 14px; border-radius:20px; font-weight:800;">📚 V7.0 FINAL CLEAN • DKI ONLY 5 WILAYAH • JUDUL BEBAS WILAYAH ONLY • NO components.html • st.html + st.iframe • NO TRACKING OPTIONAL</div>
<div style="margin-top:6px;">Total {st.session_state.bursa_total} | Aktif {st.session_state.bursa_aktif} | Kerja {st.session_state.bursa_kerja} | Grafik hanya di Putih - Kuning tanpa grafik hemat kuota</div>
</div>
""")
