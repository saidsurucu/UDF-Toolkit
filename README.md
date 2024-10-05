# UDF Toolkit
 UYAP UDF dosya formatı ile ilgili çalışmalar
## UDF dosyasını DOCX formatına çevirmek için
```
python udf_to_docx.py input.udf
```
## UDF dosyasını PDF formatına çevirmek için
```
python udf_to_pdf.py input.udf
```
## DOCX dosyasını UDF formatına çevirmek için
```
python docx_to_udf.py input.docx
```
Not: En iyi sonucu almak için Windows'ta çalıştırılmalıdır. Bazı DOCX özelliklerini dönüştürmek için Windows kütüphaneleri gereklidir. MacOS ve Linux'ta sonuçlar farklı olabilir.
## PDF dosyasını (imaj olarak) UDF formatına çevirmek için
```
python scanned_pdf_to_udf.py input.pdf
```
# Teknik Bilgiye Sahip Olmayanlar İçin Windows'ta Kullanım Talimatları

Bu scriptlerin düzgün çalışabilmesi için Python'un sisteminizde kurulu olması gerekmektedir. Aşağıdaki adımları takip ederek Python'u yükleyebilirsiniz:

1. [Python'un resmi web sitesine](https://www.python.org/downloads/) gidin.
2. Sisteminizin işletim sistemine uygun Python sürümünü indirin (genellikle en son sürüm önerilir).
3. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin.


### 1. `install_requirements.bat`
- **Amaç**: `requirements.txt` dosyasında listelenen gerekli Python paketlerini yükler.
- **Nasıl Kullanılır**: `install_requirements.bat` scriptine çift tıklayın. Bu, `requirements.txt` dosyasında belirtilen tüm gerekli bağımlılıkları yükleyecektir.

### 1. `udf_to_docx.bat`
- **Amaç**: UDF dosyasını DOCX formatına dönüştürür.
- **Nasıl Kullanılır**: `.udf` dosyasını `udf_to_docx.bat` scriptinin üzerine sürükleyin. Script çalışacak ve girdi ile aynı dizinde bir `.docx` dosyası oluşturacaktır.

### 2. `udf_to_pdf.bat`
- **Amaç**: UDF dosyasını PDF formatına dönüştürür.
- **Nasıl Kullanılır**: `.udf` dosyasını `udf_to_pdf.bat` scriptinin üzerine sürükleyin. Script çalışacak ve girdi ile aynı dizinde bir `.pdf` dosyası oluşturacaktır.

### 3. `docx_to_udf.bat`
- **Amaç**: DOCX dosyasını UDF formatına dönüştürür.
- **Nasıl Kullanılır**: `.docx` dosyasını `docx_to_udf.bat` scriptinin üzerine sürükleyin. Script çalışacak ve girdi ile aynı dizinde bir `.udf` dosyası oluşturacaktır.

### 4. `scanned_pdf_to_udf.bat`
- **Amaç**: Tarama yapılmış bir PDF dosyasını UDF formatına dönüştürür.
- **Nasıl Kullanılır**: `.pdf` dosyasını `scanned_pdf_to_udf.bat` scriptinin üzerine sürükleyin. Script çalışacak ve girdi ile aynı dizinde bir `.udf` dosyası oluşturacaktır.


## UDF Formatı Dokümantasyonu
[Docs.md](./Docs.md)
