# FLO Customer Segmentation with RFM Analysis

## Proje Özeti
Bu proje, FLO veri seti üzerinde RFM (Recency, Frequency, Monetary) analizi uygulayarak çok kanallı (omnichannel) müşteri tabanını segmentlere ayıran bir veri bilimi uygulamasıdır. Temel amaç, online ve offline alışveriş verilerini entegre ederek kural tabanlı bir segmentasyon modeli oluşturmak ve önceden belirlenmiş iş kurallarına göre hedeflenen pazarlama kampanyaları için müşteri ID listeleri üretmektir.

## RFM Segmentasyon Matrisi 
Kod içerisindeki `seg_map` kurallarının görselleştirilmiş halidir. Dikey eksen **Recency (Yenilik)** skorunu, yatay eksen ise **Frequency (Sıklık)** skorunu temsil eder. Pazarlama stratejileri bu matrise göre belirlenir:

| Recency \ Frequency | F1 (En Az) | F2 | F3 | F4 | F5 (En Sık) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **R5 (En Yeni)** | Yeni Müşteriler | Şöhret Peşinde | Şöhret Peşinde | Şanlılar | Şanlılar |
| **R4** | Potansiyelliler | Şöhret Peşinde | Şöhret Peşinde | Sadıklar | Sadıklar |
| **R3** | Uyumak Üzereler | Uyumak Üzereler | İlgilenilmeliler | Sadıklar | Sadıklar |
| **R2** | Uykudalar | Uykudalar | Riskteler | Riskteler | Kaybedilemezler |
| **R1 (En Eski)** | Uykudalar | Uykudalar | Riskteler | Riskteler | Kaybedilemezler |

## Veri İşleme Akışı (Data Pipeline)
Verinin ham halinden hedef kitle listelerine (CSV) dönüşüm süreci aşağıdaki mimariyle işler:

```text
[Ham Veri: flo_data_20k.csv]
          │
          ▼
┌──────────────────────────────────────┐
│       data_prep(df)                  │
│ 1. Online + Offline Birleştirme      │ ──► (order_num_total & customer_value_total)
│ 2. Tarih Değişkeni Dönüşümleri       │
└──────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│    create_rfm_segments(df)           │
│ 1. Analiz Tarihine Göre Gün Hesabı   │ ──► Recency, Frequency, Monetary Metrikleri
│ 2. pd.qcut() ile 1-5 Arası Skorlama  │
│ 3. RF_SCORE Oluşturma (Örn: "54")    │
└──────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│      Segmentasyon & Filtreleme       │
│ 1. Regex ile Metinsel Segment Atama  │ ──► Matris Eşleşmesi ("Sadıklar" vb.)
│ 2. Kampanya Kurallarına Göre Filtre  │
└──────────────────────────────────────┘
          │
          ├────────────────────────────┐
          ▼                            ▼
┌────────────────────────────┐   ┌────────────────────────────┐
│ yeni_marka_hedef_müşteri.csv│   │ indirim_hedef_müşteri_ids.csv│
└────────────────────────────┘   └────────────────────────────┘
```

---

### Kurulum ve Kullanım
Not: Scriptin hatasız çalışabilmesi için flo_data_20k.csv dosyasının betik ile aynı çalışma dizininde (working directory) bulunması gerekmektedir.

### Gereksinimler
* Python 3.x
* pandas
* datetime

### Çalıştırma
Projeyi yerel ortamınızda çalıştırmak için terminal üzerinden aşağıdaki komutu kullanabilirsiniz:

```bash
python CustomerSegmentationProject.py
