###############################################################

# RFM ile Müşteri Segmentasyonu

###############################################################

# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırmak ve segmentlere göre pazarlama stratejileri geliştirmek.

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak
# yapan müşterilerin geçmiş alışveriş davranışlarından elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

import pandas as pd
import datetime as dt

# Pandas görüntüleme ayarları
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 500)


def data_prep(dataframe):

    # Hem online hem offline alışveriş yapan omnichannel müşterilerden yeni değişkenler üretme
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]

    # Gerekli değişkenleri date tipine çevirme
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    return dataframe
def create_rfm_segments(dataframe):

    # Analiz tarihi -> Son tarihten 2 gün sonrası
    today_date = dataframe["last_order_date"].max() + dt.timedelta(days=2)

    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]
    rfm["recency"] = (today_date - dataframe["last_order_date"]).dt.days
    rfm["frequency"] = dataframe["order_num_total"]
    rfm["monetary"] = dataframe["customer_value_total"]

    # RF ve RFM Skorlarının Hesaplanması
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

    # RF Skorlarının Segment Olarak Tanımlanması
    seg_map = {
        r'[1-2][1-2]': 'Uykudalar',
        r'[1-2][3-4]': 'Riskteler',
        r'[1-2]5': 'Kaybedilemezler',
        r'3[1-2]': 'Uyumak Üzereler',
        r'33': 'İlgilenilmeliler',
        r'[3-4][4-5]': 'Sadıklar',
        r'41': 'Potansiyelliler',
        r'51': 'Yeni Müşteriler',
        r'[4-5][2-3]': 'Şöhret Peşinde',
        r'5[4-5]': 'Şanlılar'
    }

    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

    return rfm
def main():
    df_ = pd.read_csv("flo_data_20k.csv")
    df = df_.copy()                          ### Hata yapılırsa buradan verisetinin ilk halinde dönülebilir

    print("################# İlk 10 Gözlem #################")
    print(df.head(10))
    print("\n################# Değişken İsimleri #################")
    print(df.columns)
    print("\n################# Genel İstatistik #################")
    print(df.describe().T)
    print("\n################# Boş Değerler #################")
    print(df.isnull().sum())
    print("\n################# Değişken Tipleri #################")
    print(df.info())


    df = data_prep(df)

    # Müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımı
    print("\n################# Kritik Dağılım #################")
    print(df.groupby("order_channel").agg({
        "master_id": "count",
        "order_num_total": "mean",
        "customer_value_total": "mean"
    }))

    print("\n################# En Fazla Kazanç Getiren İlk 10 Müşteri #################")
    print(df.sort_values("customer_value_total", ascending=False)[["master_id", "customer_value_total"]].head(10))

    print("\n################# En Fazla Sipariş Veren İlk 10 Müşteri #################")
    print(df.sort_values("order_num_total", ascending=False)[["master_id", "order_num_total"]].head(10))

    rfm = create_rfm_segments(df)

    print("\n################# Segment Bazlı RFM Ortalamaları #################")
    print(rfm.groupby("segment").agg({"recency": "mean", "frequency": "mean", "monetary": "mean"}))

    final_df = pd.merge(df, rfm, left_on="master_id", right_on="customer_id")

    # Yeni kadın ayakkabı markası için hedef kitle
    # Hedef: Şanlılar veya Sadıklar segmentinde ve kadın kategorisinden alışveriş yapanlar
    target_segments_a = final_df[
        (final_df["segment"].isin(["Şanlılar", "Sadıklar"])) &
        (final_df["interested_in_categories_12"].str.contains("KADIN", na=False))
        ]
    target_segments_a["customer_id"].to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
    print("\nKadın kategorisi hedef müşteri ID'leri 'yeni_marka_hedef_müşteri_id.csv' olarak kaydedildi.")

    # Erkek ve Çocuk ürünlerinde %40 indirim için hedef kitle
    # Hedef: Kaybedilmezler, Uyumak Üzereler, Yeni Müşteriler segmentlerinden birinde ve erkek ya da çocuk kategorisinden alışveriş yapanlar
    target_segments_b = final_df[
        (final_df["segment"].isin(["Kaybedilemezler", "Uyumak Üzereler", "Yeni Müşteriler"])) &
        ((final_df["interested_in_categories_12"].str.contains("ERKEK", na=False)) |
         (final_df["interested_in_categories_12"].str.contains("COCUK", na=False)))
        ]
    target_segments_b["customer_id"].to_csv("indirim_hedef_müşteri_ids.csv", index=False)
    print("İndirim hedef müşteri ID'leri 'indirim_hedef_müşteri_ids.csv' olarak kaydedildi.")


if __name__ == "__main__":
    main()