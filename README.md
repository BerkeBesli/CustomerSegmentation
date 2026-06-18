# FLO Customer Segmentation with RFM Analysis

## Proje Özeti
Bu proje, FLO veri seti üzerinde **RFM (Recency, Frequency, Monetary)** analizi uygulayarak çok kanallı (omnichannel) müşteri tabanını segmentlere ayıran bir Python uygulamasıdır. Temel amaç, online ve offline alışveriş verilerini entegre ederek kural tabanlı bir segmentasyon modeli oluşturmak ve hedeflenen pazarlama kampanyaları için müşteri ID listeleri üretmektir.

---

## Veri Seti Özellikleri
Kullanılan veri seti, 2020 - 2021 yılları arasında hem online hem de offline (Omnichannel) alışveriş yapan müşterilerin geçmiş işlem davranışlarından oluşmaktadır.

* **master_id:** Eşsiz müşteri numarası
* **order_channel:** Alışveriş platformu (Android, iOS, Desktop, Mobile, Offline)
* **last_order_channel:** En son alışverişin yapıldığı kanal
* **first_order_date:** İlk alışveriş tarihi
* **last_order_date:** Son alışveriş tarihi
* **last_order_date_online / offline:** Platform bazlı son alışveriş tarihleri
* **order_num_total_ever_online / offline:** Platform bazlı toplam işlem sayısı
* **customer_value_total_ever_online / offline:** Platform bazlı toplam harcama miktarı
* **interested_in_categories_12:** Son 12 ayda alışveriş yapılan kategoriler

---

## Metodoloji

Proje, üç ana veri işleme fonksiyonu üzerinden yürütülmektedir:

### 1. Veri Ön İşleme (`data_prep`)
* Omnichannel yapısına uygun olarak online ve offline metrikler toplanıp tekilleştirilir (`order_num_total`, `customer_value_total`).
* Zaman serisi analizi gerektiren "date" içerikli değişkenler `string` formatından `datetime` formatına dönüştürülür.

### 2. RFM Metriklerinin Hesaplanması (`create_rfm_segments`)
* **Recency:** En son alışveriş tarihinden analiz tarihine (veri setindeki son işlemden 2 gün sonrası) kadar geçen gün sayısı.
* **Frequency:** Müşterinin gerçekleştirdiği toplam işlem sayısı.
* **Monetary:** Müşterinin bıraktığı toplam parasal değer.

### 3. Skorlama ve Segmentasyon
* Sürekli R, F ve M değerleri `pd.qcut` kullanılarak 1 ile 5 arasında kategorik skorlara dönüştürülür. (Recency için ters skala uygulanır).
* R ve F skorları birleştirilerek iki haneli `RF_SCORE` elde edilir.
* Oluşturulan skorlar, **Regex (Düzenli İfadeler)** kullanılarak standart iş segmentlerine (Örn: *Sadıklar*, *Uykudalar*, *Yeni Müşteriler*) atanır.

---

## Çıktılar
Uygulama çalıştırıldığında, belirli iş kurallarına göre hedeflenen iki farklı müşteri grubu için aşağıdaki CSV dosyalarını üretir:

1. **`yeni_marka_hedef_müşteri_id.csv`**: "Şanlılar" veya "Sadıklar" segmentinde yer alan ve daha önce Kadın kategorisinden alışveriş yapmış müşteri ID'leri.
2. **`indirim_hedef_müşteri_ids.csv`**: "Kaybedilemezler", "Uyumak Üzereler" veya "Yeni Müşteriler" segmentlerinde bulunan, Erkek veya Çocuk kategorilerinden alışveriş yapmış hedef müşteri ID'leri.

---

## Kurulum ve Kullanım

### Gereksinimler
* Python 3.x
* pandas
* datetime

### Not: Scriptin hatasız çalışabilmesi için flo_data_20k.csv dosyasının betik ile aynı çalışma dizininde (working directory) bulunması gerekmektedir.

### Çalıştırma
Projeyi yerel ortamınızda çalıştırmak için terminal üzerinden aşağıdaki komutu kullanabilirsiniz:

```bash
python CustomerSegmentationProject.py
