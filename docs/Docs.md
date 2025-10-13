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
6.  [Detaylı Eleman Açıklamaları ve Özellik Örnekleri](#detaylı-eleman-açıklamaları-ve-özellik-örnekleri)
    * [Üstbilgi (`<header>`)](#üstbilgi-header)
    * [Altbilgi (`<footer>`)](#altbilgi-footer)
    * [Paragraf (`<paragraph>`)](#paragraf-paragraph)
    * [İçerik (`<content>` elemanı)](#içerik-content-elemanı)
    * [Resim (`<image>`)](#resim-image)
    * [Tablo (`<table>`)](#tablo-table)
    * [Satır (`<row>`)](#satır-row)
    * [Hücre (`<cell>`)](#hücre-cell)
    * [Sekme (`<tab>`)](#sekme-tab)
    * [Boşluk (`<space>`)](#boşluk-space)
    * [Sayfa Sonu (`<page-break>`)](#sayfa-sonu-page-break)
    * [Alan (`<field>`) (Varsayımsal)](#alan-field-varsayımsal)

## Genel Bakış

Bu belge, belge şablonlama ve biçimlendirme için kullanılan UYAP UDF (Ulusal Yargı Ağı Projesi Doküman Formatı) ve dahili XML formatının yapısını ve elemanlarını açıklar. Bu format, çeşitli biçimlendirme seçenekleri, tablolar, gömülü öğeler, üstbilgiler, altbilgiler ve listeler içeren zengin metin belgelerini temsil etmek için tasarlanmıştır.

## UDF Dosya Yapısı

UDF formatı, esasen belirli bir iç yapıya sahip bir ZIP arşividir:

1.  UDF (ZIP) içindeki ana dosya `content.xml` olarak adlandırılır.
2.  Bu `content.xml` dosyası, XML formatında gerçek belge içeriğini ve biçimlendirme bilgilerini içerir.
3.  ZIP arşivinde diğer kaynaklar da bulunabilir. Örneğin, `content.xml` içinde base64 olarak kodlanmamış büyük resim dosyaları ayrı olarak saklanabilir ve `content.xml`'den referans verilebilir (ancak `<image imageData="...">` elemanı base64 gömülü resimleri destekler).

Bir UDF dosyasının içeriğini düzenlemek veya görüntülemek için:

1.  Dosya uzantısını `.udf`'den `.zip`'e değiştirin
2.  ZIP dosyasının içeriğini çıkarın
3.  `content.xml` dosyasını açın ve düzenleyin
4.  Düzenlenmiş dosyaları tekrar ZIP arşivine paketleyin
5.  ZIP dosyasını tekrar `.udf` olarak yeniden adlandırın

## XML Yapısı

`content.xml` dosyası, aşağıda ayrıntılı olarak açıklayacağımız belirli bir XML yapısını takip eder.

## Kök Eleman

XML belgesinin kök elemanı, aşağıdaki özelliğe sahip `<template>`'dir:

  - `format_id`: Formatın sürümü
      * Örnek: `format_id="1.8"`
  - `webID`: Belge için web tabanlı bir kimlik (isteğe bağlı).
  - `institutionID`: Kurum kimliği (isteğe bağlı).
  - `isTemplate`: Belgenin bir şablon olup olmadığını belirtir (`true`/`false`).
  - `description`: Dokümanın genel bir açıklaması.

## Ana Bölümler

`<template>` elemanı genellikle dört ana bölüm içerir. UYAP sisteminin şablonlama yeteneklerine bağlı olarak bir `<data>` bölümü de bulunabilir:

1.  `<content>`: Belgenin ham metin içeriği
2.  `<properties>`: Belge genelindeki özellikler
3.  `<elements>`: Belgenin yapısı ve biçimlendirmesi
4.  `<styles>`: Belgede kullanılan metin stilleri
5.  `<data>` (Varsayımsal): Şablon belgelerde, alanları doldurmak için kullanılacak verileri içerebilir. Yapısı UYAP'a özgü olabilir.

### İçerik Bölümü (`<content>`)

`<content>` bölümü bir CDATA bloğu içine sarılmıştır ve belgenin ham metnini içerir. Bu, üstbilgiler, altbilgiler ve ana gövde metni dahil olmak üzere tüm metinsel içeriği içerir.

Örnek:

```xml
<content><![CDATA[
  Bu, belgenin ham içeriğidir.
  Özel karakterler dahil her türlü metni içerebilir.
]]></content>
```

**Önemli Not:** İçerik bölümü, tüm metinsel verileri içeren tek bir havuz olarak çalışır. `<elements>` bölümündeki `<content>` elemanları, `startOffset` ve `length` özellikleri ile bu içerik havuzundaki belirli metin parçalarını referans alır.

### Özellikler Bölümü (`<properties>`)

`<properties>` elemanı, sayfa düzenini tanımlayan özelliklerle bir `<pageFormat>` elemanı içerir:

  - **`<pageFormat>` Elemanı:**

      * `mediaSizeName`: Sayfa boyutunu tanımlar.
          * Değerler: Standart kağıt boyutlarını temsil eden tamsayı veya string (örn: "A4", "LETTER").
          * Örnek: `mediaSizeName="A4"`
      * `leftMargin`, `rightMargin`, `topMargin`, `bottomMargin`: Sayfa kenar boşlukları (genellikle punto veya UYAP'a özgü birim cinsinden).
          * Değerler: Ondalık sayılar.
          * Örnek: `leftMargin="70.86"` (yaklaşık 2.5 cm)
      * `paperOrientation`: Sayfa yönü.
          * Değerler: Dikey için "portrait" veya "1", yatay için "landscape" veya "2".
          * Örnek: `paperOrientation="portrait"`
      * `headerFOffset`, `footerFOffset`: Üstbilgi ve altbilginin sayfa kenarından uzaklığı (offset).
          * Değerler: Ondalık sayılar.
          * Örnek: `headerFOffset="30.0"`
      * `pageBorderType`: Sayfa kenarlığının türü (örn: "single", "double", "none").
      * `pageBorderColor`: Sayfa kenarlığının rengi.
      * `pageBorderArt`: Sanatsal sayfa kenarlığı (eğer destekleniyorsa).
      * `pageBorderDisplayHorizontal`, `pageBorderDisplayVertical`, `pageBorderDisplayOnFirstPage`: Sayfa kenarlığının gösterim seçenekleri.
      * `pageBorderDistanceFrom`: Kenarlığın metinden veya sayfa kenarından uzaklığı.
      * `pageBorderTop`, `pageBorderBottom`, `pageBorderLeft`, `pageBorderRight`: Her bir kenar için kenarlık kalınlığı veya stili.
      * `pageColumns`: Sayfa üzerindeki sütun sayısı.
      * `pageColumnSpacing`: Sütunlar arası boşluk.

  - **`<bgImage>` Elemanı (Sayfa Arka Plan Resmi):**

      * `bgImageSource`: Görüntünün kaynak konumu (eğer ZIP içinde ayrı bir dosyaysa).
          * Örnek: `bgImageSource="/resources/images/background.jpg"`
      * `bgImageData`: Base64 kodlanmış görüntü verisi.
          * Örnek: `bgImageData="iVBORw0KGgoAAAANSUhEUgAA..."`
      * `bgImageBottomMargin`, `bgImageUpMargin`, `bgImageRightMargin`, `bgImageLeftMargin`: Arka plan görüntüsünün kenar boşlukları.
      * `bgImageAlign`: Arka plan resminin hizalanması (örn: "center", "tile").
      * `bgImageRepeat`: Arka plan resminin tekrarlanma şekli (örn: "repeat", "no-repeat").
      * `bgImageWatermark`: Resmin filigran olarak kullanılıp kullanılmayacağı (`true`/`false`).
      * `bgImageOpacity`: Resmin opaklığı (0.0 - 1.0).

  - **`<pageImage>` Elemanı (Özel Sayfa Görüntüleri/Filigranlar - UYAP `ac` sabitleriyle ilişkili):**

      * `pageImageClassName`: Kullanılacak özel `IPageImage` Java sınıfının adı (UYAP'a özgü).
      * `pageImageGradientData`: Gradyan bir sayfa resmi için veri (UYAP'a özgü).

Örnek:

```xml
<properties>
  <pageFormat mediaSizeName="A4" leftMargin="70.86" rightMargin="70.86" topMargin="56.69" bottomMargin="56.69" paperOrientation="portrait" headerFOffset="30.0" footerFOffset="30.0" />
  <bgImage bgImageData="iVBORw0KGgoAAAANSUhEUgAA..." bgImageAlign="center" bgImageRepeat="no-repeat" />
</properties>
```

### Elemanlar Bölümü (`<elements>`)

`<elements>` bölümü, belgenin yapısını ve biçimlendirmesini tanımlar. Aşağıdaki elemanları içerebilir:

1.  `<header>` (Üstbilgi)
2.  `<footer>` (Altbilgi)
3.  `<paragraph>` (Paragraf)
4.  `<content>` (Biçimli metin parçası - bu `<elements>` içindeki `<content>` elemanıdır, kök `<content>` CDATA bloğu değildir)
5.  `<table>` (Tablo)
6.  `<image>` (Resim)
7.  `<tab>` (Sekme karakteri)
8.  `<space>` (Boşluk karakteri)
9.  `<page-break>` (Sayfa Sonu)
10. `<field>` (Şablon Alanı - varsayımsal, UYAP'a özgü olabilir)

`<elements>` elemanı bir `resolver` özelliğine sahip olabilir, bu özellik belgenin hangi stil çözümleyiciyi (varsayılan stil setini) kullanacağını belirtir.
Örnek: `<elements resolver="hvl-default">`

### Stiller Bölümü (`<styles>`)

`<styles>` bölümü, belgede kullanılan metin stillerini tanımlar:

  - **`<style>` Elemanı:**
      * `name`: Stilin benzersiz adı (örn: "hvl-default", "Baslik1").
      * `description`: Stilin açıklaması.
      * `family`: Yazı tipi ailesi (örn: "Times New Roman", "Arial").
      * `size`: Yazı tipi boyutu (genellikle punto cinsinden).
      * `bold`, `italic`, `underline`, `strikethrough`: Metin stili (`true`/`false`).
      * `foreground`: Metin rengi (RGB formatında, genellikle işaretli bir tam sayı olarak).
      * `background`: Metin arka plan rengi (RGB formatında).
      * `subscript`, `superscript`: Alt simge, üst simge (`true`/`false`).
      * `parent`: Bu stilin miras aldığı başka bir stilin adı (hiyerarşik stil yönetimi için).
          * Örnek: `<style name="MyCustomStyle" parent="hvl-default" ... />`
      * `FONT_ATTRIBUTE_KEY`: Bu, bir UYAP Java Swing ayrıştırıcısının içsel bir detayı olabilir ve stilin Swing `Font` nesnesiyle nasıl eşleştiğini belirtebilir; genel UDF formatının bir parçası olmayabilir.

Örnek:

```xml
<styles>
  <style name="default" description="Varsayılan" family="Dialog" size="12" bold="false" italic="false" foreground="-13421773" />
  <style name="hvl-default" parent="default" family="Times New Roman" size="12" description="Gövde Metni" />
  <style name="Baslik1" parent="hvl-default" size="16" bold="true" foreground="-16777216" />
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

## Detaylı Eleman Açıklamaları ve Özellik Örnekleri

### Üstbilgi (`<header>`)

`<header>` elemanı ile temsil edilir, üstbilgi içeriği için paragraflar içerir.

Özellikler:

  - `background`: Üstbilgi arka plan rengi (RGB formatında).
      * Örnek: `background="-8323073"` (açık mavi)
  - `foreground`: Üstbilgi metin rengi (RGB formatında).
      * Örnek: `foreground="-16776961"` (mavi)

Örnek:

```xml
<header background="-8323073" foreground="-16776961">
  <paragraph Alignment="1"> <content family="Times New Roman" size="10" startOffset="0" length="25" /> </paragraph>
</header>
```

### Altbilgi (`<footer>`)

`<footer>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

  - `background`: Altbilgi arka plan rengi (RGB formatında).
  - `foreground`: Altbilgi metin rengi (RGB formatında).
  - `pageNumber-spec`: Sayfa numarası formatı ve konumu için özel bir belirteç (UYAP'a özgü olabilir).
      * Örnek: `pageNumber-spec="BSP32_40"`
  - `pageNumber-color`: Sayfa numarası rengi (RGB formatında).
  - `pageNumber-fontFace`: Sayfa numarası için yazı tipi.
  - `pageNumber-fontSize`: Sayfa numarası için yazı tipi boyutu.
  - `pageNumber-foreStr`: Sayfa numarasından önce gelen metin (örn: "Sayfa ").
  - `pageNumber-afterStr`: Sayfa numarasından sonra gelen metin (örn: " / ToplamSayfa").
  - `pageNumber-pageStartNumStr`: Başlangıç sayfa numarası.

Örnek:

```xml
<footer pageNumber-spec="PageNumCenter" pageNumber-color="-16777216" pageNumber-fontFace="Arial" pageNumber-fontSize="10" pageNumber-foreStr="Sayfa: ">
  <paragraph Alignment="2"> <content family="Arial" size="9" startOffset="26" length="15" /> </paragraph>
</footer>
```

### Paragraf (`<paragraph>`)

`<paragraph>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

  - `Alignment`: Metin hizalama.
      * Değerler: Sola için "0", ortaya için "1", sağa için "2", iki yana yasla için "3".
      * Örnek: `Alignment="3"` (iki yana yasla)
  - `LeftIndent`, `RightIndent`: Paragrafın sol ve sağ girintileri (punto cinsinden).
  - `FirstLineIndent`: İlk satır girintisi (punto cinsinden).
  - `SpaceBefore` (veya `SpaceAbove`), `SpaceAfter` (veya `SpaceBelow`): Paragraftan önceki ve sonraki boşluk (punto cinsinden).
  - `LineSpacing`: Satır aralığı (örn: 1.0 tek, 1.5, 2.0 çift).
  - `TabSet`: Sekme durak pozisyonları, hizalamaları ve öncü karakterleri (örn: "36.0:0:0,72.0:1:1" - 36pt sola hizalı, 72pt ortaya hizalı nokta öncülü).
  - `Bulleted`: Madde işaretli liste öğesi ise "true".
  - `BulletType`: Madde işareti türü (örn: "BULLET\_TYPE\_ELLIPSE", "BULLET\_TYPE\_SQUARE", veya UYAP'a özgü bir sabit).
  - `Numbered`: Numaralandırılmış liste öğesi ise "true".
  - `NumberType`: Numaralandırma türü (örn: "NUMBER\_TYPE\_NUMBER\_DOT", "NUMBER\_TYPE\_ROMAN\_UPPER", UYAP'a özgü).
  - `ListLevel`: Liste öğesinin girinti seviyesi (0'dan başlar).
  - `ListId`: Aynı listeye ait öğeleri gruplamak için bir tanımlayıcı.
  - `StartNumber`: Numaralandırılmış listeler için başlangıç numarası.
  - `ListRestart`: Bu seviyedeki listenin numarasının yeniden başlatılıp başlatılmayacağı.
  - `ListBulletFont`, `ListBulletColor`, `ListBulletSize`: Madde imi/numara için özel yazı tipi, renk ve boyut.
  - `ListStyleName`: Önceden tanımlanmış bir liste stiline referans.
  - `KeepWithNext`: Paragrafın bir sonraki paragrafla aynı sayfada tutulup tutulmayacağı (`true`/`false`).
  - `HangingIndent`: Asılı girinti miktarı (punto cinsinden).
  - `ParagraphGroupName`, `ParagraphGroupRepeatable`: Şablonlama için paragraf gruplama özellikleri (UYAP'a özgü).
  - `family`, `size`, `bold`, `italic`, vb.: Paragraf içindeki tüm metinler için varsayılan stil özellikleri (içerideki `<content>` elemanları bunları geçersiz kılabilir).

Örnek:

```xml
<paragraph Alignment="0" LeftIndent="36.0" LineSpacing="1.5" SpaceBefore="6.0" SpaceAfter="6.0" Bulleted="true" BulletType="BULLET_TYPE_FILLED_CIRCLE" ListLevel="0" ListId="1">
  <content startOffset="77" length="35" style="MyListStyle" /> </paragraph>
```

### İçerik (`<content>` elemanı)

`<elements>` içindeki `<content>` elemanı, belirli biçimlendirmeye sahip metin parçalarını temsil eder:

  - `startOffset`, `length`: Ana `<content>` CDATA bloğundaki metnin başlangıç konumu ve uzunluğu.
  - `family`, `size`, `bold`, `italic`, `underline`, `strikethrough`, `subscript`, `superscript`: Metin biçimlendirme özellikleri.
  - `foreground`, `background`: Metin ve arka plan rengi (RGB formatında).
  - `resolver`: Kullanılacak stil çözümleyiciyi (varsa).
  - `style`: `<styles>` bölümünde tanımlanmış bir stile referans.
      * Örnek: `style="VurguluMetin"`
  - **Alan Özellikleri (Eğer metin bir şablon alanıysa - UYAP `V` sabitleriyle ilişkili):**
      * `fieldName`: Alanın adı.
      * `fieldType`: Alanın türü (örn: "text", "date", "number", UYAP'a özgü).
      * `fieldVisible`: Alanın görünür olup olmadığı (`true`/`false`).
      * `fieldEditable`: Alanın düzenlenebilir olup olmadığı (`true`/`false`).
      * `fieldGroup`: Alanın ait olduğu grup.
      * `fieldDescription`: Alan için açıklama.
  - **Barkod Özellikleri (Eğer metin bir barkod ise - UYAP `V` sabitleriyle ilişkili):**
      * `barcodeData`: Barkodun içeriği olan veri.
      * `barcodeType`: Barkod türü (örn: "Code128", "QRCode").
  - `backgroundImageData`: Bu metin parçası için özel bir arka plan resmi (base64).

Örnek:

```xml
<paragraph>
  <content startOffset="100" length="10" style="NormalMetin" />
  <content startOffset="110" length="15" style="VurguluMetin" bold="true" foreground="-65536" /> <content startOffset="125" length="20" fieldName="MusteriAdi" fieldType="text" /> </paragraph>
```

### Resim (`<image>`)

Resimler `<image>` elemanı ile temsil edilir:

  - `imageData`: Base64 ile kodlanmış resim verisi.
  - `width`, `height`: Resmin görüntülenme genişliği ve yüksekliği (punto veya piksel).
  - `alignment`: Resmin hizalanması (paragraf içinde).
  - `description`: Resim için alternatif metin veya açıklama.
  - `family`, `size`: Eğer resim yüklenemezse gösterilecek yer tutucu metnin stili.

Örnek:

```xml
<paragraph Alignment="1"> <image imageData="iVBORw0KGgoAAAANSUhEUgAA..." width="200" height="150" description="Şirket Logosu" />
</paragraph>
```

### Tablo (`<table>`)

Tablolar `<table>` elemanı ile temsil edilir:

  - `tableName`: Tablonun adı (isteğe bağlı).
  - `columnCount`: Tablodaki sütun sayısı.
  - `columnSpans`: Her bir sütunun genişliğini tanımlayan virgülle ayrılmış değerler listesi (punto veya yüzde).
      * Örnek: `columnSpans="150,200,100"`
  - `width`: Tablonun toplam genişliği (isteğe bağlı, `columnSpans` genellikle yeterlidir).
  - `widthType`: Tablo genişliğinin türü (örn: "fixed", "percentage").
  - `border`: Tüm tablo için varsayılan kenarlık stili (örn: "borderCell", "borderOuter", "none"). Daha spesifik kenarlıklar hücre bazında tanımlanabilir.
  - `borderType`: Daha detaylı kenarlık tipi (UYAP'a özgü olabilir).
  - `borderColor`, `borderWidth`: Varsayılan kenarlık rengi ve kalınlığı.
  - `cellSpacing`, `cellPadding`: Hücreler arası boşluk ve hücre içi dolgu.
  - `alignment`: Tablonun sayfa üzerindeki hizalanması (örn: "left", "center", "right").

Örnek:

```xml
<table tableName="MusteriListesi" columnCount="3" columnSpans="50,*,100" border="borderCell" alignment="center">
  </table>
```

(Not: `*` sütun genişliği için "kalan alanı kullan" anlamına gelebilir, UDF formatına bağlıdır)

### Satır (`<row>`)

`<table>` içindeki satırlar `<row>` elemanı ile temsil edilir:

  - `rowName`: Satırın adı (isteğe bağlı).
  - `rowType`: Satırın türü (örn: "headerRow", "dataRow", "footerRow"). Başlık satırları sayfa sonlarında tekrarlanabilir.
  - `height`: Satırın sabit yüksekliği (punto).
  - `height_min`, `height_max`: Minimum ve maksimum satır yüksekliği.
  - `cantSplit`: Satırın sayfa sonlarında bölünemeyeceğini belirtir (`true`/`false`).

Örnek:

```xml
<row rowType="headerRow" height="30" cantSplit="true">
  </row>
```

### Hücre (`<cell>`)

`<row>` içindeki hücreler `<cell>` elemanı ile temsil edilir:

  - `width`: Hücrenin genişliği (eğer `<table>`deki `columnSpans`'ı geçersiz kılıyorsa).
  - `height`: Hücrenin yüksekliği (eğer `<row>`daki `height`'ı geçersiz kılıyorsa).
  - `bgColor` (veya `cellColor`): Hücrenin arka plan rengi (RGB formatında).
      * Örnek: `bgColor="-256"` (sarı)
  - `vAlign`: İçeriğin dikey hizalanması ("top", "middle", "bottom").
      * Örnek: `vAlign="middle"`
  - `hAlign` (veya `textAlign`): İçeriğin yatay hizalanması (hücre içindeki paragraflar bunu geçersiz kılabilir).
  - `colspan`: Hücrenin yatay olarak kaç sütun boyunca birleşeceği.
      * Örnek: `colspan="2"`
  - `rowspan`: Hücrenin dikey olarak kaç satır boyunca birleşeceği.
      * Örnek: `rowspan="3"`
  - `borderTop`, `borderBottom`, `borderLeft`, `borderRight`: Her bir kenar için stil, renk, kalınlık.
      * Örnek: `borderBottom="solid 1px #000000"`
  - `paddingTop`, `paddingBottom`, `paddingLeft`, `paddingRight`: Hücre içi dolgu miktarları.

Örnek:

```xml
<row>
  <cell width="150" height="50" bgColor="-256" vAlign="middle">
    <paragraph Alignment="1">
      <content startOffset="200" length="12" /> </paragraph>
  </cell>
  <cell colspan="2" vAlign="top">
    <paragraph>
      <content startOffset="212" length="25" /> </paragraph>
  </cell>
</row>
<row>
  <cell rowspan="2" bgColor="-16711681" vAlign="bottom">
    <paragraph Alignment="2">
      <content startOffset="237" length="22" /> </paragraph>
  </cell>
  <cell>
    <paragraph>
      <content startOffset="259" length="13" /> </paragraph>
  </cell>
  <cell>
    <paragraph>
      <content startOffset="272" length="13" /> </paragraph>
  </cell>
</row>
<row>
  <cell>
    <paragraph>
      <content startOffset="285" length="13" /> </paragraph>
  </cell>
  <cell>
    <paragraph>
      <content startOffset="298" length="13" /> </paragraph>
  </cell>
</row>
```

### Sekme (`<tab>`)

`<tab>` elemanı bir sekme karakterini temsil eder:

  - `startOffset`, `length`: Ana `<content>` CDATA bloğundaki konumu. `length` genellikle 1'dir.

Örnek:

```xml
<paragraph>
  <content startOffset="311" length="5" /> <tab startOffset="316" length="1" />
  <content startOffset="317" length="10" /> </paragraph>
```

### Boşluk (`<space>`)

`<space>` elemanı, genellikle `<content>` elemanları arasında ek bir boşluk (space karakteri) eklemek için kullanılır. `startOffset` ve `length` (genellikle 1) öznitelikleriyle ana CDATA bloğundaki bir boşluğu referans alabilir veya sadece anlamsal bir boşluk olarak var olabilir.

Örnek:

```xml
<paragraph>
  <content startOffset="327" length="4" /> <space startOffset="331" length="1" /> <content startOffset="332" length="4" /> </paragraph>
```

### Sayfa Sonu (`<page-break>`)

`<page-break>` elemanı, belgede o noktada yeni bir sayfaya geçilmesini zorlar. Genellikle içinde boş veya kısa bir `<paragraph>` ve `<content>` elemanı barındırabilir.

Örnek:

```xml
<page-break>
  <paragraph>
    <content startOffset="336" length="0" /> </paragraph>
</page-break>
```

### Alan (`<field>`) (Varsayımsal)

Eğer UDF şablonlama için kullanılıyorsa, `<elements>` içinde `<field>` adında özel bir eleman bulunabilir. Bu eleman, `<data>` bölümünden veya harici bir kaynaktan gelen veriyle doldurulacak yer tutucuları temsil eder. Öznitelikleri `<content>` elemanının alan özelliklerine benzer olabilir:

  - `name` (veya `fieldName`): Alanın benzersiz adı.
  - `type` (veya `fieldType`): Alanın veri türü (örn: "text", "date", "image").
  - `default`: Veri bulunamazsa gösterilecek varsayılan değer.
  - Formatlama öznitelikleri (font, size, color vb.).

Örnek (tamamen varsayımsal):

```xml
<paragraph>
  <content startOffset="350" length="10" /> <field name="MusteriAdi" type="text" startOffset="360" length="0" style="AlanStili" /> </paragraph>
```

**Not:** `<field>` elemanının varlığı ve yapısı UYAP sisteminin özel uygulamasına bağlıdır. Genellikle bu tür alanlar `<content>` elemanlarına eklenmiş özel özniteliklerle de (yukarıda `<content>` bölümünde belirtildiği gibi `fieldName` vb.) temsil edilebilir.
