# UYAP UDF Dosya Formatı
## İçindekiler
1. [Genel Bakış](#genel-bakış)
2. [UDF Dosya Yapısı](#udf-dosya-yapısı)
3. [XML Yapısı](#xml-yapısı)
4. [Kök Eleman](#kök-eleman)
5. [Ana Bölümler](#ana-bölümler)
   - [İçerik Bölümü](#i̇çerik-bölümü)
   - [Özellikler Bölümü](#özellikler-bölümü)
   - [Elemanlar Bölümü](#elemanlar-bölümü)
   - [Stiller Bölümü](#stiller-bölümü)
6. [Detaylı Eleman Açıklamaları ve Özellik Örnekleri](#detaylı-eleman-açıklamaları-ve-özellik-örnekleri)
7. [Tam Örnek](#tam-örnek)
8. [En İyi Uygulamalar](#en-i̇yi-uygulamalar)
9. [Sıkça Sorulan Sorular](#sıkça-sorulan-sorular)

## Genel Bakış
Bu belge, belge şablonlama ve biçimlendirme için kullanılan UDF ve dahili XML formatının yapısını ve elemanlarını açıklar. Bu format, çeşitli biçimlendirme seçenekleri, tablolar, gömülü öğeler, üstbilgiler, altbilgiler ve listeler içeren zengin metin belgelerini temsil etmek için tasarlanmıştır.

## UDF Dosya Yapısı
UDF formatı, esasen belirli bir iç yapıya sahip bir ZIP arşividir:

1. UDF (ZIP) içindeki ana dosya `content.xml` olarak adlandırılır.
2. Bu `content.xml` dosyası, XML formatında gerçek belge içeriğini ve biçimlendirme bilgilerini içerir.
3. ZIP arşivinde diğer kaynaklar (örneğin, resimler veya ek meta veriler) de bulunabilir.

Bir UDF dosyasının içeriğini düzenlemek veya görüntülemek için:
1. Dosya uzantısını `.udf`'den `.zip`'e değiştirin
2. ZIP dosyasının içeriğini çıkarın
3. `content.xml` dosyasını açın ve düzenleyin
4. Düzenlenmiş dosyaları tekrar ZIP arşivine paketleyin
5. ZIP dosyasını tekrar `.udf` olarak yeniden adlandırın

## XML Yapısı
`content.xml` dosyası, aşağıda ayrıntılı olarak açıklayacağımız belirli bir XML yapısını takip eder.

## Kök Eleman
XML belgesinin kök elemanı, aşağıdaki özelliğe sahip `<template>`'dir:
- `format_id`: Formatın sürümü
  - Örnek: `format_id="1.8"`

## Ana Bölümler
`<template>` elemanı dört ana bölüm içerir:

1. `<content>`: Belgenin ham metin içeriği
2. `<properties>`: Belge genelindeki özellikler
3. `<elements>`: Belgenin yapısı ve biçimlendirmesi
4. `<styles>`: Belgede kullanılan metin stilleri

### İçerik Bölümü
`<content>` bölümü bir CDATA bloğu içine sarılmıştır ve belgenin ham metnini içerir. Bu, üstbilgiler, altbilgiler ve ana gövde metni dahil olmak üzere tüm metinsel içeriği içerir.

Örnek:
```xml
<content><![CDATA[
  Bu, belgenin ham içeriğidir.
  Özel karakterler dahil her türlü metni içerebilir.
]]></content>
```

### Özellikler Bölümü
`<properties>` elemanı, sayfa düzenini tanımlayan özelliklerle bir `<pageFormat>` elemanı içerir:

- `mediaSizeName`: Sayfa boyutunu tanımlar
  - Değerler: Standart kağıt boyutlarını temsil eden tamsayı
  - Örnek: `mediaSizeName="1"` (A4 boyutu)

- `leftMargin`, `rightMargin`, `topMargin`, `bottomMargin`: Sayfa kenar boşlukları (punto cinsinden)
  - Değerler: Ondalık sayılar
  - Örnek: `leftMargin="42.51968479156494"` (yaklaşık 1.5 cm)

- `paperOrientation`: Sayfa yönü
  - Değerler: Dikey için "1", yatay için "2"
  - Örnek: `paperOrientation="1"` (dikey)

- `headerFOffset`, `footerFOffset`: Üstbilgi ve altbilgi ofsetleri (punto cinsinden)
  - Değerler: Ondalık sayılar
  - Örnek: `headerFOffset="20.0"` (yaklaşık 0.7 cm)

Örnek:
```xml
<properties>
  <pageFormat mediaSizeName="1" leftMargin="42.51968479156494" rightMargin="42.51968479156494" topMargin="42.51968479156494" bottomMargin="70.8661413192749" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" />
</properties>
```

### Elemanlar Bölümü
`<elements>` bölümü, belgenin yapısını ve biçimlendirmesini tanımlar. Aşağıdaki elemanları içerebilir:

1. Üstbilgi
2. Altbilgi
3. Paragraf
4. İçerik
5. Tablo
6. Resim
7. Sekme

### Stiller Bölümü
`<styles>` bölümü, belgede kullanılan metin stillerini tanımlar:

- `name`: Stilin adı
- `description`: Stilin açıklaması
- `family`: Yazı tipi ailesi
- `size`: Yazı tipi boyutu (punto cinsinden)
- `bold`, `italic`: Metin stili
- `foreground`: Metin rengi (RGB formatında)
- `FONT_ATTRIBUTE_KEY`: Java Swing yazı tipi özelliği

Örnek:
```xml
<styles>
  <style name="default" description="Geçerli" family="Dialog" size="12" bold="false" italic="false" foreground="-13421773" FONT_ATTRIBUTE_KEY="javax.swing.plaf.FontUIResource[family=Dialog,name=Dialog,style=plain,size=12]" />
  <style name="hvl-default" family="Times New Roman" size="12" description="Gövde" />
</styles>
```

## Detaylı Eleman Açıklamaları ve Özellik Örnekleri

### Üstbilgi
`<header>` elemanı ile temsil edilir, üstbilgi içeriği için paragraflar içerir.

Örnek:
```xml
<header>
  <paragraph name="hvl-default" family="Times New Roman" size="12" description="Gövde">
    <content name="hvl-default" family="Times New Roman" size="12" description="Gövde" startOffset="0" length="14" />
  </paragraph>
</header>
```

### Altbilgi
`<footer>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `pageNumber-spec`: Sayfa numarası özelliği
  - Örnek: `pageNumber-spec="BSP32_40"`

- `pageNumber-color`: Sayfa numarası rengi (RGB formatında)
  - Örnek: `pageNumber-color="-16777216"` (siyah)

- `pageNumber-fontFace`: Sayfa numarası için yazı tipi
  - Örnek: `pageNumber-fontFace="Arial"`

- `pageNumber-fontSize`: Sayfa numarası için yazı tipi boyutu
  - Örnek: `pageNumber-fontSize="11"`

- `pageNumber-foreStr`: Sayfa numarasından önce gelen metin
  - Örnek: `pageNumber-foreStr="sayfa"`

- `pageNumber-pageStartNumStr`: Başlangıç sayfa numarası
  - Örnek: `pageNumber-pageStartNumStr="1"`

Örnek:
```xml
<footer pageNumber-spec="BSP32_40" pageNumber-color="-16777216" pageNumber-fontFace="Arial" pageNumber-fontSize="11" pageNumber-foreStr="sayfa" pageNumber-pageStartNumStr="1">
  <paragraph FirstLineIndent="2.5" family="Times New Roman" size="12">
    <content FirstLineIndent="2.5" family="Times New Roman" size="12" startOffset="822" length="-11" />
  </paragraph>
</footer>
```

### Paragraf
`<paragraph>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `Alignment`: Metin hizalama
  - Değerler: Sola için "0", ortaya için "1", sağa için "2", iki yana yasla için "3"
  - Örnek: `Alignment="3"` (iki yana yasla)

- `LeftIndent`, `RightIndent`: Girinti değerleri (punto cinsinden)
  - Örnek: `LeftIndent="36.0"` (yaklaşık 1.27 cm)

- `LineSpacing`: Satır aralığı
  - Değerler: Ondalık sayılar (1.0 tek aralık, 2.0 çift aralık)
  - Örnek: `LineSpacing="0.5"` (yarım aralık)

- `TabSet`: Sekme durak pozisyonları ve türleri
  - Örnek: `TabSet="36.0:0:0"` (36 puntoda sekme durağı, sola hizalı)

- `Bulleted`: Madde işaretli liste öğeleri için "true"
  - Örnek: `Bulleted="true"`

- `BulletType`: Madde işareti türü
  - Örnek: `BulletType="BULLET_TYPE_ELLIPSE"`

- `Numbered`: Numaralandırılmış liste öğeleri için "true"
  - Örnek: `Numbered="true"`

- `NumberType`: Numaralandırma türü
  - Örnek: `NumberType="NUMBER_TYPE_NUMBER_DOT"`

- `ListLevel`: Liste öğesinin girinti seviyesi
  - Örnek: `ListLevel="1"`

- `ListId`: Liste için tanımlayıcı
  - Örnek: `ListId="1"`

- `FirstLineIndent`: İlk satır girintisi
  - Örnek: `FirstLineIndent="2.5"`

Örnek:
```xml
<paragraph Alignment="3" LineSpacing="0.5" TabSet="36.0:0:0" LeftIndent="36.0" Bulleted="true" BulletType="BULLET_TYPE_ELLIPSE" ListLevel="1" ListId="1">
  <content startOffset="233" length="140" />
</paragraph>
```

### İçerik
`<content>` elemanı, belirli biçimlendirmeye sahip metni temsil eder:

- `size`: Yazı tipi boyutu (punto cinsinden)
  - Örnek: `size="12"`

- `bold`, `italic`, `underline`: Metin stili
  - Örnek: `bold="true"` `italic="false"` `underline="true"`

- `startOffset`, `length`: Ham içerikteki metnin konumu ve uzunluğu
  - Örnek: `startOffset="16" length="39"`

- `resolver`: Kullanılacak stil çözümleyiciyi belirtir
  - Örnek: `resolver="hvl-default"`

- `strikethrough`: Üstü çizili metin için "true"
  - Örnek: `strikethrough="true"`

- `subscript`: Alt simge metni için "true"
  - Örnek: `subscript="true"`

- `superscript`: Üst simge metni için "true"
  - Örnek: `superscript="true"`

- `background`: Arka plan rengi (RGB formatında)
  - Örnek: `background="-8239546"` (açık mavi)

- `foreground`: Metin rengi (RGB formatında)
  - Örnek: `foreground="-16777216"` (siyah)

Örnek:
```xml
<content bold="true" startOffset="16" length="39" />
<content strikethrough="true" startOffset="469" length="9" />
<content subscript="true" startOffset="484" length="3" />
<content superscript="true" startOffset="496" length="4" />
<content background="-8239546" foreground="-16777216" startOffset="545" length="13" />
```

### Tablo
Tablolar `<table>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `tableName`: Tablonun adı
  - Örnek: `tableName="Sabit"`

- `columnCount`: Sütun sayısı
  - Örnek: `columnCount="3"`

- `columnSpans`: Sütun genişlikleri
  - Örnek: `columnSpans="100,79,121"`

- `border`: Kenarlık stili
  - Örnek: `border="borderCell"`

Örnek:
```xml
<table tableName="Sabit" columnCount="3" columnSpans="100,79,121" border="borderCell">
  <row rowName="row1" rowType="dataRow">
    <cell>
      <paragraph>
        <content startOffset="787" length="1" />
      </paragraph>
    </cell>
  </row>
</table>
```

### Resim
Resimler `<image>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `family`: Resim yer tutucu için yazı tipi ailesi
  - Örnek: `family="Times New Roman"`

- `size`: Resim yer tutucu için yazı tipi boyutu
  - Örnek: `size="12"`

- `imageData`: Base64 ile kodlanmış resim verisi
  - Örnek: `imageData="iVBORw0KGgoAAAANSUhEUgAA..."`

Örnek:
```xml
<image family="Times New Roman" size="12" imageData="iVBORw0KGgoAAAANSUhEUgAA..." />
```

### Sekme
`<tab>` elemanı bir sekme karakterini temsil eder ve aşağıdaki özelliklere sahiptir:

- `startOffset`: Ham içerikteki sekmenin konumu
  - Örnek: `startOffset="130"`

- `length`: Tek bir sekme karakteri için her zaman 1'dir
  - Örnek: `length="1"`

Örnek:
```xml
<tab startOffset="130" length="1" />
```

