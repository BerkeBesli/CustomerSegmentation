# FLO Customer Segmentation with RFM Analysis

## Proje Özeti
Bu proje, FLO veri seti üzerinde RFM (Recency, Frequency, Monetary) analizi uygulayarak çok kanallı (omnichannel) müşteri tabanını segmentlere ayıran bir veri bilimi uygulamasıdır. Temel amaç, online ve offline alışveriş verilerini entegre ederek kural tabanlı bir segmentasyon modeli oluşturmak ve önceden belirlenmiş iş kurallarına göre hedeflenen pazarlama kampanyaları için müşteri ID listeleri üretmektir.

---

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
