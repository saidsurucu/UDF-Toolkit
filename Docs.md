# UYAP UDF Dosya Formatı

## İçindekiler

1.  [Genel Bakış](#genel-bakış)
2.  [UDF Dosya Yapısı](#udf-dosya-yapısı)
3.  [XML Yapısı](#xml-yapısı)
4.  [Kök Eleman](#kök-eleman)
5.  [Ana Bölümler](#ana-bölümler)
    * [İçerik Bölümü (`<content>`)](#içerik-bölümü-content)
    * [Özellikler Bölümü (`<properties>`)](#özellikler-bölümü-properties)
    * [Elemanlar Bölümü (`<elements>`)](#elemanlar-bölümü-elements)
    * [Stiller Bölümü (`<styles>`)](#stiller-bölümü-styles)
    * [Veri Bölümü (`<data>`) (Varsayımsal)](#veri-bölümü-data-varsayımsal)
6.  [Detaylı Eleman Açıklamaları](#detaylı-eleman-açıklamaları)
    * [Üstbilgi (`<header>`)](#üstbilgi-header)
    * [Altbilgi (`<footer>`)](#altbilgi-footer)
    * [Paragraf (`<paragraph>`)](#paragraf-paragraph)
    * [İçerik (`<content>` elemanı)](#içerik-content-elemanı)
    * [Resim (`<image>`)](#resim-image)
    * [Sekme (`<tab>`)](#sekme-tab)
    * [Tablo (`<table>`)](#tablo-table)
    * [Satır (`<row>`)](#satır-row)
    * [Hücre (`<cell>`)](#hücre-cell)
    * [Boşluk (`<space>`)](#boşluk-space)
    * [Sayfa Sonu (`<page-break>`)](#sayfa-sonu-page-break)
    * [Alan (`<field>`) (Varsayımsal)](#alan-field-varsayımsal)
7.  [Renk Kodlama Sistemi](#renk-kodlama-sistemi)
8.  [Özel Karakterler](#özel-karakterler)

## Genel Bakış

Bu belge, UYAP UDF (Ulusal Yargı Ağı Projesi Doküman Formatı) dosya formatının yapısını ve elemanlarını açıklar. Bu format, zengin metin belgelerini (tablolar, gömülü resimler, üstbilgiler, altbilgiler, listeler vb.) temsil etmek için tasarlanmıştır.

## UDF Dosya Yapısı

UDF dosyası, Deflate sıkıştırmalı bir **ZIP arşividir**. İçinde tek bir dosya bulunur:

- `content.xml` — Belgenin tüm içerik ve biçimlendirme bilgilerini taşıyan XML dosyası

Bir UDF dosyasını düzenlemek için:

1. Uzantıyı `.udf` → `.zip` olarak değiştirin
2. ZIP içeriğini çıkarın
3. `content.xml` dosyasını düzenleyin
4. Tekrar ZIP olarak paketleyin
5. Uzantıyı `.zip` → `.udf` olarak değiştirin

## XML Yapısı

`content.xml` UTF-8 kodlamalı bir XML dosyasıdır. `<?xml ?>` bildiriminden sonra boşluk bırakılmaz. Tüm özellik değerleri çift tırnak içindedir.

## Kök Eleman

```xml
<template format_id="1.8">
```

- `format_id`: Format sürümü (her zaman `"1.8"`)

## Ana Bölümler

`<template>` elemanı genellikle dört ana bölüm içerir. UYAP sisteminin şablonlama yeteneklerine bağlı olarak bir `<data>` bölümü de bulunabilir:

1. `<content>` — Ham metin havuzu
2. `<properties>` — Sayfa özellikleri
3. `<elements>` — Belge yapısı ve biçimlendirme
4. `<styles>` — Stil tanımları
5. `<data>` (Varsayımsal) — Şablon belgelerde, alanları doldurmak için kullanılacak verileri içerebilir

### İçerik Bölümü (`<content>`)

Belgenin tüm düz metni tek bir CDATA bloğunda tutulur:

```xml
<content><![CDATA[Üstbilgi metni\nGövde metni\nAltbilgi metni]]></content>
```

**Kritik kurallar:**

- Tüm metin tek bir havuzda saklanır: önce üstbilgi, sonra gövde, en son altbilgi metni
- `<elements>` bölümündeki elemanlar bu havuzdaki metni `startOffset` ve `length` ile referans alır
- Offset ve length **karakter sayısı** (rune) cinsindendir, byte değil. Türkçe karakterler ve emoji dahil her karakter 1 sayılır
- Offset 0'dan başlar
- Paragraflar arası `\n` (satır sonu) karakteri ile ayrılır
- Resim yer tutucusu için `\uFFFC` (Object Replacement Character) kullanılır

**Örnek:**

CDATA = `"Merhaba\nDünya"` ise:
- "Merhaba" → `startOffset="0"`, `length="7"`
- "\n" → `startOffset="7"`, `length="1"`
- "Dünya" → `startOffset="8"`, `length="5"`

### Özellikler Bölümü (`<properties>`)

#### `<pageFormat>` Elemanı

Sayfa düzenini tanımlar. Tüm değerler **punto** cinsindendir.

```xml
<pageFormat
  mediaSizeName="1"
  leftMargin="42.52"
  rightMargin="28.35"
  topMargin="14.17"
  bottomMargin="14.17"
  paperOrientation="1"
  headerFOffset="20.0"
  footerFOffset="20.0"
/>
```

| Özellik | Açıklama | Varsayılan |
|---------|----------|------------|
| `mediaSizeName` | Kağıt boyutu (1 = A4) | `"1"` |
| `leftMargin` | Sol kenar boşluğu (pt) | `42.52` |
| `rightMargin` | Sağ kenar boşluğu (pt) | `28.35` |
| `topMargin` | Üst kenar boşluğu (pt) | `14.17` |
| `bottomMargin` | Alt kenar boşluğu (pt) | `14.17` |
| `paperOrientation` | 0 = yatay, 1 = dikey | `"1"` |
| `headerFOffset` | Üstbilgi offset (pt) | `20.0` |
| `footerFOffset` | Altbilgi offset (pt) | `20.0` |

**A4 sayfa boyutu:** 595.28 × 841.89 punto (210 × 297 mm)

#### `<bgImage>` Elemanı (Arka Plan Resmi)

```xml
<bgImage
  bgImageSource=""
  bgImageData="[base64 kodlu resim]"
  bgImageBottomMargin="42.0"
  bgImageUpMargin="42.0"
  bgImageRigtMargin="42.0"
  bgImageLeftMargin="42.0"
/>
```

> **Not:** `bgImageRigtMargin` yazım hatası değildir — UYAP uyumluluğu için bu şekilde yazılmalıdır.

### Elemanlar Bölümü (`<elements>`)

```xml
<elements resolver="hvl-default">
  <header>...</header>
  <paragraph>...</paragraph>
  <table>...</table>
  <page-break>...</page-break>
  <footer>...</footer>
</elements>
```

`resolver` özelliği varsayılan stil çözümleyiciyi belirtir.

### Stiller Bölümü (`<styles>`)

```xml
<styles>
  <style name="default" description="Geçerli" family="Dialog" size="12"
         bold="false" italic="false" foreground="-13421773"
         FONT_ATTRIBUTE_KEY="javax.swing.plaf.FontUIResource[...]" />
  <style name="hvl-default" family="Times New Roman" size="12" description="Gövde" />
</styles>
```

### Veri Bölümü (`<data>`) (Varsayımsal)

Eğer UDF dosyası bir şablon olarak kullanılıyorsa, `<elements>` bölümündeki `<field>` elemanlarını doldurmak için bir `<data>` bölümü bulunabilir. Bu bölümün yapısı genellikle UYAP sistemine özgüdür ve XML veya başka bir formatta olabilir.

Örnek (tamamen varsayımsal):

```xml
<data>
  <record>
    <adi>Ahmet</adi>
    <soyadi>Yılmaz</soyadi>
    <davaNo>2023/123</davaNo>
  </record>
</data>
```

## Detaylı Eleman Açıklamaları

### Üstbilgi (`<header>`)

Üstbilgi paragraflar ve resimler içerebilir:

```xml
<header>
  <paragraph family="Times New Roman" size="12" description="Gövde">
    <image imageData="[base64]" width="220.0" height="172.0" startOffset="0" length="1" />
    <content startOffset="0" length="10" family="Times New Roman" size="12" />
  </paragraph>
</header>
```

### Altbilgi (`<footer>`)

Altbilgi, sayfa numarası özellikleri taşıyabilir:

```xml
<footer pageNumber-spec="BSP32_40"
        pageNumber-fontBold="false"
        pageNumber-fontItalic="false"
        pageNumber-fontFace="Arial"
        pageNumber-fontSize="11"
        pageNumber-color="-16777216">
  <paragraph>
    <content startOffset="0" length="1" family="Arial" size="11" />
  </paragraph>
</footer>
```

| Özellik | Açıklama |
|---------|----------|
| `pageNumber-spec` | Sayfa numarası format belirteci |
| `pageNumber-fontFace` | Yazı tipi |
| `pageNumber-fontSize` | Yazı tipi boyutu (pt) |
| `pageNumber-fontBold` | Kalın (`true`/`false`) |
| `pageNumber-fontItalic` | İtalik (`true`/`false`) |
| `pageNumber-color` | Renk (işaretli ARGB tam sayı) |

### Paragraf (`<paragraph>`)

```xml
<paragraph
  Alignment="0"
  LeftIndent="25.0"
  RightIndent="0.0"
  FirstLineIndent="0.0"
  LineSpacing="0.0"
  SpaceAbove="0.0"
  SpaceBelow="0.0"
  TabSet="36.0:0:0,72.0:0:0"
>
  <content ... />
  <image ... />
  <tab ... />
</paragraph>
```

| Özellik | Açıklama | Not |
|---------|----------|-----|
| `Alignment` | 0=sol, 1=orta, 2=sağ, 3=iki yana yasla | |
| `LeftIndent` | Sol girinti (pt) | Her zaman mevcut |
| `RightIndent` | Sağ girinti (pt) | Her zaman mevcut |
| `FirstLineIndent` | İlk satır girintisi (pt) | İsteğe bağlı |
| `LineSpacing` | Satır aralığı çarpanı (ör: 0.15 = 1.15x) | İsteğe bağlı |
| `SpaceAbove` | Paragraf öncesi boşluk (pt) | İsteğe bağlı |
| `SpaceBelow` | Paragraf sonrası boşluk (pt) | İsteğe bağlı |
| `TabSet` | Sekme durakları: `pozisyon:hiza:öncü` | İsteğe bağlı |

**TabSet formatı:** `"36.0:0:0,72.0:0:0"` — Her durak `pozisyon:hizalama:öncü` şeklinde, virgülle ayrılır.
- Hizalama: 0=sol, 1=orta, 2=sağ, 3=ondalık
- Öncü: 0=yok, 1=nokta, 2=tire

#### Liste Özellikleri

Numaralı ve madde işaretli listeler paragraf düzeyinde tanımlanır:

```xml
<!-- Numaralı liste -->
<paragraph Numbered="true" NumberType="NUMBER_TYPE_NUMBER_DOT" ListId="1" ListLevel="0">

<!-- Madde işaretli liste -->
<paragraph Bulleted="true" BulletType="BULLET_TYPE_ELLIPSE" ListId="2" ListLevel="0">
```

**Numara Türleri:**

| Değer | Gösterim |
|-------|----------|
| `NUMBER_TYPE_NUMBER_DOT` | 1. 2. 3. |
| `NUMBER_TYPE_NUMBER_PARENTHESIS` | 1) 2) 3) |
| `NUMBER_TYPE_CHAR_SMALL_DOT` | a. b. c. |
| `NUMBER_TYPE_CHAR_SMALL_PARENTHESIS` | a) b) c) |
| `NUMBER_TYPE_CHAR_BIG_DOT` | A. B. C. |
| `NUMBER_TYPE_CHAR_BIG_PARENTHESIS` | A) B) C) |
| `NUMBER_TYPE_ROMAN_SMALL_DOT` | i. ii. iii. |
| `NUMBER_TYPE_ROMAN_SMALL_PARENTHESIS` | i) ii) iii) |
| `NUMBER_TYPE_ROMAN_BIG_DOT` | I. II. III. |
| `NUMBER_TYPE_ROMAN_BIG_PARENTHESIS` | I) II) III) |

**Madde İşareti Türleri:**

| Değer | Sembol |
|-------|--------|
| `BULLET_TYPE_ELLIPSE` | • |
| `BULLET_TYPE_RECTANGLE` | ■ |
| `BULLET_TYPE_ARROW` | ➤ |
| `BULLET_TYPE_DIAMOND` | ◆ |
| `BULLET_TYPE_DIAMOND_2` | ◊ |
| `BULLET_TYPE_TRIANGLE` | ▲ |
| `BULLET_TYPE_RECTANGLE_D` | □ |

Ek liste özellikleri: `ListId` (liste grubu), `ListLevel` (girinti seviyesi, 0'dan başlar), `SecListTypeLevel1` (çok seviyeli listelerde ikincil tür).

### İçerik (`<content>` elemanı)

Paragraf içindeki biçimli metin parçasını temsil eder:

```xml
<content
  startOffset="0"
  length="5"
  family="Times New Roman"
  size="11"
  bold="true"
  italic="true"
  underline="true"
  foreground="-16777216"
  background="-1"
/>
```

| Özellik | Açıklama |
|---------|----------|
| `startOffset` | CDATA'daki başlangıç karakter pozisyonu |
| `length` | Karakter uzunluğu |
| `family` | Yazı tipi ailesi |
| `size` | Yazı tipi boyutu (pt) |
| `bold` | Kalın (`true`/`false`) |
| `italic` | İtalik (`true`/`false`) |
| `underline` | Altı çizili (`true`/`false`) |
| `foreground` | Metin rengi (işaretli ARGB tam sayı) |
| `background` | Arka plan rengi (işaretli ARGB tam sayı) |

**Boş paragraf:** İçerik yoksa sıfır genişlikli boşluk (U+200B) kullanılır ve `length="1"` olur.

```xml
<content startOffset="0" length="1" family="Times New Roman" size="10" />
```

### Resim (`<image>`)

```xml
<image
  imageData="[base64 kodlu JPEG/PNG]"
  startOffset="0"
  length="1"
  width="200.0"
  height="150.0"
/>
```

| Özellik | Açıklama |
|---------|----------|
| `imageData` | Base64 kodlu resim verisi (JPEG veya PNG) |
| `startOffset` | CDATA'daki pozisyon (U+FFFC karakteri) |
| `length` | Her zaman `1` |
| `width` | Genişlik (pt) |
| `height` | Yükseklik (pt) |

**Boyut dönüşümü:** DOCX'teki EMU biriminden punto'ya: `EMU × (72 / 914400) = pt`

**Kalite ayarları:** İmzalar ve vektörel resimler (EMF/WMF) %95, diğer resimler %90 JPEG kalitesinde saklanır. Maksimum boyut 1500×1500 piksel.

### Sekme (`<tab>`)

```xml
<tab
  startOffset="0"
  length="1"
  family="Times New Roman"
  size="10"
/>
```

CDATA'da `\t` (U+0009) karakterine karşılık gelir, `length` her zaman `1`'dir.

### Tablo (`<table>`)

```xml
<table
  tableName="Sabit"
  columnCount="3"
  columnSpans="100.0,150.0,200.0"
  border="borderCell"
>
  <row>
    <cell>
      <paragraph>...</paragraph>
    </cell>
  </row>
</table>
```

| Özellik | Açıklama |
|---------|----------|
| `tableName` | Tablo adı (isteğe bağlı) |
| `columnCount` | Sütun sayısı |
| `columnSpans` | Sütun genişlikleri, virgülle ayrılmış (pt) |
| `border` | `"borderCell"` veya `"borderTable"` |

### Satır (`<row>`)

```xml
<row
  rowName="row1"
  rowType="dataRow"
  border="borderTable"
  height="20.0"
>
```

| Özellik | Açıklama |
|---------|----------|
| `rowName` | Satır adı (isteğe bağlı) |
| `rowType` | `"dataRow"`, `"headerRow"` |
| `border` | Kenarlık türü (birleştirilmiş hücrelerde) |
| `height` | Satır yüksekliği (pt), ayırıcı satırlar için `0.0` |

### Hücre (`<cell>`)

Hücreler paragraflar ve iç içe tablolar içerebilir:

```xml
<cell
  colspan="1"
  align="top"
  fillColor="16777215"
  border="borderCell"
  borderStyle="borderStyle-solid"
  borderWidth="1.0"
  borderColor="-16777216"
  borderSpec="15"
>
  <paragraph>...</paragraph>
</cell>
```

| Özellik | Açıklama |
|---------|----------|
| `colspan` | Sütun birleştirme sayısı |
| `align` | Dikey hizalama: `"top"`, `"vcenter"`, `"bottom"` |
| `fillColor` | Dolgu rengi (işaretli ARGB tam sayı) |
| `border` | `"borderCell"`, `"borderNone"` |
| `borderStyle` | `"borderStyle-solid"`, `"borderStyle-dotted"`, `"borderStyle-dashed"`, `"borderStyle-double"` |
| `borderWidth` | Kenarlık kalınlığı (pt) |
| `borderColor` | Kenarlık rengi (işaretli ARGB tam sayı) |
| `borderSpec` | Bitwise kenarlık belirteci (aşağıya bakın) |

**borderSpec değerleri (bitwise):**

| Bit | Kenar |
|-----|-------|
| 1 | Üst |
| 2 | Sağ |
| 4 | Alt |
| 8 | Sol |

Örnek: `15` = tüm kenarlar (1+2+4+8), `5` = üst+alt (1+4)

**Varsayılan hücre dolgusu:** Sol 5.4 pt, sağ 5.4 pt

### Boşluk (`<space>`)

`<space>` elemanı, `<content>` elemanları arasında ek bir boşluk karakteri eklemek için kullanılır. `startOffset` ve `length` (genellikle 1) öznitelikleriyle ana CDATA bloğundaki bir boşluğu referans alabilir.

```xml
<paragraph>
  <content startOffset="327" length="4" />
  <space startOffset="331" length="1" />
  <content startOffset="332" length="4" />
</paragraph>
```

### Sayfa Sonu (`<page-break>`)

```xml
<page-break>
  <paragraph>
    <content startOffset="0" length="1" />
  </paragraph>
</page-break>
```

### Alan (`<field>`) (Varsayımsal)

Eğer UDF şablonlama için kullanılıyorsa, `<elements>` içinde `<field>` adında özel bir eleman bulunabilir. Bu eleman, `<data>` bölümünden veya harici bir kaynaktan gelen veriyle doldurulacak yer tutucuları temsil eder:

- `name` (veya `fieldName`): Alanın benzersiz adı
- `type` (veya `fieldType`): Alanın veri türü (örn: "text", "date", "image")
- `default`: Veri bulunamazsa gösterilecek varsayılan değer
- Formatlama öznitelikleri (font, size, color vb.)

```xml
<paragraph>
  <content startOffset="350" length="10" />
  <field name="MusteriAdi" type="text" startOffset="360" length="0" style="AlanStili" />
</paragraph>
```

**Not:** `<field>` elemanının varlığı ve yapısı UYAP sisteminin özel uygulamasına bağlıdır. Bu tür alanlar `<content>` elemanlarına eklenmiş özel özniteliklerle (`fieldName`, `fieldType`, `fieldEditable` vb.) de temsil edilebilir.

## Renk Kodlama Sistemi

UDF'de renkler **işaretli 32-bit ARGB tam sayı** olarak saklanır.

**Dönüşüm formülü:**

```
Hex #RRGGBB → ARGB = 0xFF000000 | (R << 16) | (G << 8) | B → signed int32
```

**Yaygın değerler:**

| Renk | Hex | ARGB Tam Sayı |
|------|-----|---------------|
| Siyah | `#000000` | `-16777216` |
| Beyaz | `#FFFFFF` | `-1` |
| Kırmızı | `#FF0000` | `-65536` |

## Özel Karakterler

| Karakter | Unicode | Kullanım |
|----------|---------|----------|
| Resim yer tutucusu | U+FFFC | CDATA'da resim pozisyonu |
| Sekme | U+0009 (`\t`) | Sekme karakteri |
| Satır sonu | U+000A (`\n`) | Paragraflar arası ayırıcı |
| Sıfır genişlikli boşluk | U+200B | Boş paragraf işaretçisi |

## Varsayılan Değerler

| Özellik | Değer |
|---------|-------|
| Varsayılan yazı tipi | Times New Roman |
| Varsayılan boyut | 11 pt |
| Varsayılan metin rengi | -16777216 (siyah) |
| A4 genişlik | 595.28 pt (210 mm) |
| A4 yükseklik | 841.89 pt (297 mm) |
