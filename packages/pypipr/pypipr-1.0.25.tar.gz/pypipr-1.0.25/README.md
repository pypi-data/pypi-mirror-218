
# About
The Python Package Index Project (pypipr)

pypi : https://pypi.org/project/pypipr


# Setup
Install with pip
```
pip install pypipr
```

Import with * for fastest access
```python
from pypipr.pypipr import *
```

# CONSTANT

`LINUX`

`WINDOWS`

# FUNCTION

## avg

`avg(i)`

Simple Average Function karena tidak disediakan oleh python  

```python  
n = [1, 22, 2, 3, 13, 2, 123, 12, 31, 2, 2, 12, 2, 1]  
print(avg(n))  
```

Output:
```py
16.285714285714285
```

## basename

`basename(path)`

Mengembalikan nama file dari path  

```python  
print(basename("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
file.py
```

## batch_calculate

`batch_calculate(pattern)`

Analisa perhitungan massal.  
Bisa digunakan untuk mencari alternatif terendah/tertinggi/dsb.  


```python  
iprint(batch_calculate("{1 10} m ** {1 3}"))  
```

Output:
```py
[('1 m ** 1', <Quantity(1, 'meter')>),
 ('1 m ** 2', <Quantity(1, 'meter ** 2')>),
 ('1 m ** 3', <Quantity(1, 'meter ** 3')>),
 ('2 m ** 1', <Quantity(2, 'meter')>),
 ('2 m ** 2', <Quantity(2, 'meter ** 2')>),
 ('2 m ** 3', <Quantity(2, 'meter ** 3')>),
 ('3 m ** 1', <Quantity(3, 'meter')>),
 ('3 m ** 2', <Quantity(3, 'meter ** 2')>),
 ('3 m ** 3', <Quantity(3, 'meter ** 3')>),
 ('4 m ** 1', <Quantity(4, 'meter')>),
 ('4 m ** 2', <Quantity(4, 'meter ** 2')>),
 ('4 m ** 3', <Quantity(4, 'meter ** 3')>),
 ('5 m ** 1', <Quantity(5, 'meter')>),
 ('5 m ** 2', <Quantity(5, 'meter ** 2')>),
 ('5 m ** 3', <Quantity(5, 'meter ** 3')>),
 ('6 m ** 1', <Quantity(6, 'meter')>),
 ('6 m ** 2', <Quantity(6, 'meter ** 2')>),
 ('6 m ** 3', <Quantity(6, 'meter ** 3')>),
 ('7 m ** 1', <Quantity(7, 'meter')>),
 ('7 m ** 2', <Quantity(7, 'meter ** 2')>),
 ('7 m ** 3', <Quantity(7, 'meter ** 3')>),
 ('8 m ** 1', <Quantity(8, 'meter')>),
 ('8 m ** 2', <Quantity(8, 'meter ** 2')>),
 ('8 m ** 3', <Quantity(8, 'meter ** 3')>),
 ('9 m ** 1', <Quantity(9, 'meter')>),
 ('9 m ** 2', <Quantity(9, 'meter ** 2')>),
 ('9 m ** 3', <Quantity(9, 'meter ** 3')>),
 ('10 m ** 1', <Quantity(10, 'meter')>),
 ('10 m ** 2', <Quantity(10, 'meter ** 2')>),
 ('10 m ** 3', <Quantity(10, 'meter ** 3')>)]
```

## batchmaker

`batchmaker(pattern: str)`

Alat Bantu untuk membuat teks yang berulang.  
Gunakan `{[start][separator][finish]([separator][step])}`.  
```  
[start] dan [finish]    -> bisa berupa huruf maupun angka  
([separator][step])     -> bersifat optional  
[separator]             -> selain huruf dan angka  
[step]                  -> berupa angka positif  
```  

```python  
s = "Urutan {1/6/3} dan {10:9} dan {j k} dan {Z - A - 15} saja."  
print(batchmaker(s))  
print(list(batchmaker(s)))  
```

Output:
```py
<generator object batchmaker at 0x79511e85e0>
['Urutan 1 dan 10 dan j dan Z saja.', 'Urutan 1 dan 10 dan j dan K saja.', 'Urutan 1 dan 10 dan k dan Z saja.', 'Urutan 1 dan 10 dan k dan K saja.', 'Urutan 1 dan 9 dan j dan Z saja.', 'Urutan 1 dan 9 dan j dan K saja.', 'Urutan 1 dan 9 dan k dan Z saja.', 'Urutan 1 dan 9 dan k dan K saja.', 'Urutan 4 dan 10 dan j dan Z saja.', 'Urutan 4 dan 10 dan j dan K saja.', 'Urutan 4 dan 10 dan k dan Z saja.', 'Urutan 4 dan 10 dan k dan K saja.', 'Urutan 4 dan 9 dan j dan Z saja.', 'Urutan 4 dan 9 dan j dan K saja.', 'Urutan 4 dan 9 dan k dan Z saja.', 'Urutan 4 dan 9 dan k dan K saja.']
```

## calculate

`calculate(teks)`

Mengembalikan hasil dari perhitungan teks menggunakan modul pint.  
Mendukung perhitungan matematika dasar dengan satuan.  

Return value:  
- Berupa class Quantity dari modul pint  

Format:  
- f"{result:~P}"            -> pretty  
- f"{result:~H}"            -> html  
- result.to_base_units()    -> SI  
- result.to_compact()       -> human readable  

```python  
fx = "3 meter * 10 cm * 3 km"  
res = calculate(fx)  
print(res)  
print(res.to_base_units())  
print(res.to_compact())  
print(f"{res:~P}")  
print(f"{res:~H}")  
```

Output:
```py
90 centimeter * kilometer * meter
900.0 meter ** 3
900.0 meter ** 3
90 cm·km·m
90 cm km m
```

## chunck_array

`chunck_array(array, size, start=0)`

Membagi array menjadi potongan-potongan dengan besaran yg diinginkan  

```python  
array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(chunck_array(array, 5))  
print(list(chunck_array(array, 5)))  
```

Output:
```py
<generator object chunck_array at 0x795148b940>
[[2, 3, 12, 3, 3], [42, 42, 1, 43, 2], [42, 41, 4, 24, 32], [42, 3, 12, 32, 42], [42]]
```

## console_run

`console_run(info, command=None, print_info=True, capture_output=False)`

Menjalankan command seperti menjalankan command di Command Terminal  

```py  
console_run('dir')  
console_run('ls')  
```

## create_folder

`create_folder(folder_name)`

Membuat folder.  
Membuat folder secara recursive dengan permission.  

```py  
create_folder("contoh_membuat_folder")  
create_folder("contoh/membuat/folder/recursive")  
create_folder("./contoh_membuat_folder/secara/recursive")  
```

## datetime_from_string

`datetime_from_string(iso_string, timezone='UTC')`

Parse iso_string menjadi datetime object  

```python  
print(datetime_from_string("2022-12-12 15:40:13").isoformat())  
print(datetime_from_string("2022-12-12 15:40:13", timezone="Asia/Jakarta").isoformat())  
```

Output:
```py
2022-12-12T15:40:13+00:00
2022-12-12T15:40:13+07:00
```

## datetime_now

`datetime_now(timezone=None)`

Memudahkan dalam membuat Datetime untuk suatu timezone tertentu  

```python  
print(datetime_now("Asia/Jakarta"))  
print(datetime_now("GMT"))  
print(datetime_now("Etc/GMT+7"))  
```

Output:
```py
2023-07-05 21:14:21.710195+07:00
2023-07-05 14:14:21.711959+00:00
2023-07-05 07:14:21.716702-07:00
```

## dict_first

`dict_first(d: dict, remove=False)`

Mengambil nilai (key, value) pertama dari dictionary dalam bentuk tuple.  

```python  
d = {  
    "key2": "value2",  
    "key3": "value3",  
    "key1": "value1",  
}  
print(dict_first(d, remove=True))  
print(dict_first(d))  
```

Output:
```py
('key2', 'value2')
('key3', 'value3')
```

## dirname

`dirname(path)`

Mengembalikan nama folder dari path.  
Tanpa trailing slash di akhir.  

```python  
print(dirname("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
/ini/nama/folder/ke
```

## exit_if_empty

`exit_if_empty(*args)`

Keluar dari program apabila seluruh variabel  
setara dengan empty  

```py  
var1 = None  
var2 = '0'  
exit_if_empty(var1, var2)  
```

## filter_empty

`filter_empty(iterable, zero_is_empty=True, str_strip=True)`

Mengembalikan iterabel yang hanya memiliki nilai  

```python  
var = [1, None, False, 0, "0", True, {}, ['eee']]  
print(filter_empty(var))  
```

Output:
```py
<generator object filter_empty at 0x795143ec50>
```

## get_class_method

`get_class_method(cls)`

Mengembalikan berupa tuple yg berisi list dari method dalam class  

```python  
class ExampleGetClassMethod:  
    def a():  
        return [x for x in range(10)]  

    def b():  
        return [x for x in range(10)]  

    def c():  
        return [x for x in range(10)]  

    def d():  
        return [x for x in range(10)]  

print(get_class_method(ExampleGetClassMethod))  
```

Output:
```py
<generator object get_class_method at 0x795143ee30>
```

## get_filemtime

`get_filemtime(filename)`

Mengambil informasi last modification time file dalam nano seconds  

```python  
print(get_filemtime(__file__))  
```

Output:
```py
1688488273961495610
```

## get_filesize

`get_filesize(filename)`

Mengambil informasi file size dalam bytes  

```python  
print(get_filesize(__file__))  
```

Output:
```py
17002
```

## github_pull

`github_pull()`

Menjalankan command `git pull`  

```py  
github_pull()  
```

## github_push

`github_push(commit_msg=None)`

Menjalankan command status, add, commit dan push  

```py  
github_push('Commit Message')  
```

## github_user

`github_user(email=None, name=None)`

Menyimpan email dan nama user secara global sehingga tidak perlu  
menginput nya setiap saat.  

```py  
github_user('my@emil.com', 'MyName')  
```

## idumps

`idumps(data, syntax='yaml', indent=4)`

Mengubah variabel data menjadi string untuk yang dapat dibaca untuk disimpan.  
String yang dihasilkan berbentuk syntax YAML/JSON/HTML.  

```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42]),  
}  
print(idumps(data))  
print(idumps(data, syntax='html'))  
```

Output:
```py
a: 123
l: !!python/tuple
- 12
- 23
-   - 12
    - 42
t:
- disini
- senang
- disana
- senang

<table>
    <tbody>
        <tr>
            <th>a</th>
            <td>
                <span>123</span>
            </td>
        </tr>
        <tr>
            <th>t</th>
            <td>
                <ul>
                    <li>
                        <span>disini</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                    <li>
                        <span>disana</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                </ul>
            </td>
        </tr>
        <tr>
            <th>l</th>
            <td>
                <ul>
                    <li>
                        <span>12</span>
                    </li>
                    <li>
                        <span>23</span>
                    </li>
                    <li>
                        <ul>
                            <li>
                                <span>12</span>
                            </li>
                            <li>
                                <span>42</span>
                            </li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

```

## idumps_html

`idumps_html(data, indent=None)`

Serialisasi python variabel menjadi HTML.  
```  
List -> <ul>...</ul>  
Dict -> <table>...</table>  
```  

```python  
data = {  
    'abc': 123,  
    'list': [1, 2, 3, 4, 5],  
    'dict': {'a': 1, 'b':2, 'c':3},  
}  
print(idumps_html(data))  
```

Output:
```py
<table>
  <tbody>
    <tr>
      <th>abc</th>
      <td>
        <span>123</span>
      </td>
    </tr>
    <tr>
      <th>list</th>
      <td>
        <ul>
          <li>
            <span>1</span>
          </li>
          <li>
            <span>2</span>
          </li>
          <li>
            <span>3</span>
          </li>
          <li>
            <span>4</span>
          </li>
          <li>
            <span>5</span>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <th>dict</th>
      <td>
        <table>
          <tbody>
            <tr>
              <th>a</th>
              <td>
                <span>1</span>
              </td>
            </tr>
            <tr>
              <th>b</th>
              <td>
                <span>2</span>
              </td>
            </tr>
            <tr>
              <th>c</th>
              <td>
                <span>3</span>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>

```

## iexec

`iexec(python_syntax, import_pypipr=True)`

improve exec() python function untuk mendapatkan outputnya  

```python  
print(iexec('print(9*9)'))  
```

Output:
```py
81

```

## ijoin

`ijoin(iterable, separator='', start='', end='', remove_empty=False, recursive=True, recursive_flat=False, str_strip=False)`

Simplify Python join functions like PHP function.  
Iterable bisa berupa sets, tuple, list, dictionary.  

```python  
arr = {'asd','dfs','weq','qweqw'}  
print(ijoin(arr, ', '))  

arr = '/ini/path/seperti/url/'.split('/')  
print(ijoin(arr, ','))  
print(ijoin(arr, ',', remove_empty=True))  

arr = {'a':'satu', 'b':(12, 34, 56), 'c':'tiga', 'd':'empat'}  
print(ijoin(arr, separator='</li>\n<li>', start='<li>', end='</li>', recursive_flat=True))  
print(ijoin(arr, separator='</div>\n<div>', start='<div>', end='</div>'))  
print(ijoin(10, ' '))  
```

Output:
```py
dfs, asd, qweqw, weq
,ini,path,seperti,url,
ini,path,seperti,url
<li>satu</li>
<li>12</li>
<li>34</li>
<li>56</li>
<li>tiga</li>
<li>empat</li>
<div>satu</div>
<div><div>12</div>
<div>34</div>
<div>56</div></div>
<div>tiga</div>
<div>empat</div>
10
```

## iloads

`iloads(data, syntax='yaml')`

Mengubah string data hasil dari idumps menjadi variabel.  
String data adalah berupa syntax YAML.  

```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42])  
}  
s = idumps(data)  
print(iloads(s))  
```

## iloads_html

`iloads_html(html)`

Mengambil data yang berupa list `<ul>`, dan table `<table>` dari html  
dan menjadikannya data python berupa list.  
setiap data yang ditemukan akan dibungkus dengan tuple sebagai separator.  
```  
list (<ul>)     -> list         -> list satu dimensi  
table (<table>) -> list[list]   -> list satu dimensi didalam list  
```  
apabila data berupa ul maka dapat dicek type(data) -> html_ul  
apabila data berupa ol maka dapat dicek type(data) -> html_ol  
apabila data berupa dl maka dapat dicek type(data) -> html_dl  
apabila data berupa table maka dapat dicek type(data) -> html_table  

```python  
pprint.pprint(iloads_html(iopen("https://harga-emas.org/")), depth=10)  
pprint.pprint(iloads_html(iopen("https://harga-emas.org/1-gram/")), depth=10)  
```

Output:
```py
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [['Harga Emas Hari Ini - Rabu, 05 Juli 2023'],
  ['Spot Emas USD↓1.923,90 (-0,58) / oz',
   'Kurs IDR15.140,00 / USD',
   'Emas IDR↓936.482 (-282) / gr'],
  ['LM Antam (Jual)↑1.058.000 (+4.000) / gr',
   'LM Antam (Beli)↑936.000 (+4.000) / gr']],
 [['Harga Emas Hari Ini'],
  ['Gram', 'Gedung Antam Jakarta', 'Pegadaian'],
  ['per Gram (Rp)', 'per Batangan (Rp)', 'per Gram (Rp)', 'per Batangan (Rp)'],
  ['1000',
   '999 (+4)',
   '998.600 (+4.000)',
   '1.019.465 (+5.125)',
   '1.019.465.000 (+5.125.000)'],
  ['500',
   '1.997 (+8)',
   '998.640 (+4.000)',
   '1.019.506 (+5.124)',
   '509.753.000 (+2.562.000)'],
  ['250',
   '3.996 (+16)',
   '999.060 (+4.000)',
   '1.019.940 (+5.128)',
   '254.985.000 (+1.282.000)'],
  ['100',
   '10.001 (+40)',
   '1.000.120 (+4.000)',
   '1.021.030 (+5.130)',
   '102.103.000 (+513.000)'],
  ['50',
   '20.018 (+80)',
   '1.000.900 (+4.000)',
   '1.021.840 (+5.140)',
   '51.092.000 (+257.000)'],
  ['25',
   '40.099 (+160)',
   '1.002.480 (+4.000)',
   '1.023.480 (+5.160)',
   '25.587.000 (+129.000)'],
  ['10',
   '100.750 (+400)',
   '1.007.500 (+4.000)',
   '1.028.600 (+5.100)',
   '10.286.000 (+51.000)'],
  ['5',
   '202.600 (+800)',
   '1.013.000 (+4.000)',
   '1.034.400 (+5.200)',
   '5.172.000 (+26.000)'],
  ['3',
   '339.889 (+1.333)',
   '1.019.667 (+4.000)',
   '1.041.333 (+5.333)',
   '3.124.000 (+16.000)'],
  ['2',
   '514.000 (+2.000)',
   '1.028.000 (+4.000)',
   '1.050.000 (+5.500)',
   '2.100.000 (+11.000)'],
  ['1',
   '1.058.000 (+4.000)',
   '1.058.000 (+4.000)',
   '1.081.000 (+5.000)',
   '1.081.000 (+5.000)'],
  ['0.5',
   '2.316.000 (+8.000)',
   '1.158.000 (+4.000)',
   '1.184.000 (+4.000)',
   '592.000 (+2.000)'],
  ['Update harga LM Antam :05 Juli 2023, pukul 08:25Harga pembelian kembali '
   ':Rp. 936.000/gram (+4.000)',
   'Update harga LM Pegadaian :04 Juli 2023']],
 [['Spot Harga Emas Hari Ini (Market Open)'],
  ['Satuan', 'USD', 'Kurs\xa0Dollar', 'IDR'],
  ['Ounce\xa0(oz)', '1.923,90 (-0,58)', '15.140,00', '29.127.846'],
  ['Gram\xa0(gr)', '61,85', '15.140,00', '936.482 (-282)'],
  ['Kilogram\xa0(kg)', '61.854,82', '15.140,00', '936.481.996'],
  ['Update harga emas :05 Juli 2023, pukul 21:14Update kurs :13 Febuari 2023, '
   'pukul 09:10']],
 [['Gram', 'UBS Gold 99.99%'],
  ['Jual', 'Beli'],
  ['/ Batang', '/ Gram', '/ Batang', '/ Gram'],
  ['100',
   '94.935.000 (-100.000)',
   '949.350 (-1.000)',
   '93.700.000 (+400.000)',
   '937.000 (+4.000)'],
  ['50',
   '47.520.000 (-50.000)',
   '950.400 (-1.000)',
   '46.850.000 (+200.000)',
   '937.000 (+4.000)'],
  ['25',
   '23.863.000 (-25.000)',
   '954.520 (-1.000)',
   '23.425.000 (+100.000)',
   '937.000 (+4.000)'],
  ['10',
   '9.595.000 (-10.000)',
   '959.500 (-1.000)',
   '9.370.000 (+40.000)',
   '937.000 (+4.000)'],
  ['5',
   '4.850.000 (-5.000)',
   '970.000 (-1.000)',
   '4.685.000 (+20.000)',
   '937.000 (+4.000)'],
  ['1',
   '1.003.000 (-1.000)',
   '1.003.000 (-1.000)',
   '937.000 (+4.000)',
   '937.000 (+4.000)'],
  ['', 'Update :05 Juli 2023, pukul 11:05']],
 [['Konversi Satuan'],
  ['Satuan', 'Ounce (oz)', 'Gram (gr)', 'Kilogram (kg)'],
  ['Ounce\xa0(oz)', '1', '31,1034767696', '0,0311034768'],
  ['Gram\xa0(gr)', '0,0321507466', '1', '0.001'],
  ['Kilogram\xa0(kg)', '32,1507466000', '1.000', '1']],
 [['Pergerakan Harga Emas Dunia'],
  ['Waktu', 'Emas'],
  ['Unit', 'USD', 'IDR'],
  ['Angka', '+/-', 'Angka', '+/-'],
  ['Hari Ini', 'Kurs', '', '', '15.140', '%'],
  ['oz', '1.924,48', '-0,58-0,03%', '29.136.627', '-8.781-0,03%'],
  ['gr', '61,87', '-0,02-0,03%', '936.764', '-282-0,03%'],
  ['30 Hari', 'Kurs', '', '', '15.140', '%'],
  ['oz', '1.958,40', '-34,50-1,76%', '29.650.176', '-522.330-1,76%'],
  ['gr', '62,96', '-1,11-1,76%', '953.275', '-16.793-1,76%'],
  ['2 Bulan', 'Kurs', '', '', '15.140', '%'],
  ['oz', '2.016,87', '-92,97-4,61%', '30.535.412', '-1.407.566-4,61%'],
  ['gr', '64,84', '-2,99-4,61', '981.736', '-45.254-4,61%'],
  ['6 Bulan', 'Kurs', '', '', '15.610', '-470-3,01%'],
  ['oz', '1.862,67', '+61,23+3,29%', '29.076.279', '+51.567+0,18%'],
  ['gr', '59,89', '+1,97+3,29%', '934.824', '+1.658+0,18%'],
  ['1 Tahun', 'Kurs', '', '', '14.960', '+180+1,20%'],
  ['oz', '1.767,13', '+156,77+8,87%', '26.436.265', '+2.691.581+10,18%'],
  ['gr', '56,81', '+5,04+8,87%', '849.946', '+86.536+10,18%'],
  ['2 Tahun', 'Kurs', '', '', '14.564', '+576+3,95%'],
  ['oz', '1.791,95', '+131,95+7,36%', '26.097.960', '+3.029.886+11,61%'],
  ['gr', '57,61', '+4,24+7,36%', '839.069', '+97.413+11,61%'],
  ['3 Tahun', 'Kurs', '', '', '14.566', '+574+3,94%'],
  ['oz', '1.775,30', '+148,60+8,37%', '25.859.020', '+3.268.826+12,64%'],
  ['gr', '57,08', '+4,78+8,37%', '831.387', '+105.095+12,64%'],
  ['5 Tahun', 'Kurs', '', '', '14.409', '+731+5,07%'],
  ['oz', '1.255,54', '+668,36+53,23%', '18.091.076', '+11.036.770+61,01%'],
  ['gr', '40,37', '+21,49+53,23%', '581.642', '+354.840+61,01%']])
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [[''],
  ['Emas 24 KaratHarga Emas 1 Gram', ''],
  ['USD', '61,85↓', '-0,02-0,03%'],
  ['KURS', '15.055,55↑', '+42,70+0,28%'],
  ['IDR', '931.258,36↑', '+2.361,25+0,25%'],
  ['Rabu, 05 Juli 2023 21:14']],
 [[''],
  ['Emas 1 Gram (IDR)Emas 1 Gram (USD)Kurs USD-IDR',
   'Hari Ini',
   '1 Bulan',
   '1 Tahun',
   '5 Tahun',
   'Max',
   '']],
 [['Pergerakkan Harga Emas 1 Gram'],
  ['', 'Penutupan Kemarin', 'Pergerakkan Hari Ini', 'Rata-rata'],
  ['USD', '61,87', '61,85 - 61,87', '61,86'],
  ['KURS', '15.012,85', '15.012,85 - 15.055,55', '15.034,20'],
  ['IDR', '928.897,11', '928.897,11 - 931.258,36', '930.077,74'],
  [''],
  ['', 'Awal Tahun', 'Pergerakkan YTD', '+/- YTD'],
  ['USD', '58,64', '58,23 - 65,97', '+3,21 (5,47%)'],
  ['KURS', '15.538,50', '14.669,40 - 15.629,15', '-482,95(-3,11%)'],
  ['IDR', '911.153,72', '888.842,84 - 982.694,10', '+20.104,64 (2,21%)'],
  [''],
  ['', 'Tahun Lalu / 52 Minggu', 'Pergerakkan 52 Minggu', '+/- 52 Minggu'],
  ['USD', '58,09', '52,31 - 65,97', '+3,76 (6,47%)'],
  ['KURS', '14.991,05', '14.653,00 - 15.785,40', '+64,50 (0,43%)'],
  ['IDR', '870.771,79', '795.009,21 - 982.694,10', '+60.486,57 (6,95%)']])
```

## input_char

`input_char(prompt=None, prompt_ending='', newline_after_input=True, echo_char=True, default=None)`

Meminta masukan satu huruf tanpa menekan Enter.  

```py  
input_char("Input char : ")  
input_char("Input char : ", default='Y')  
input_char("Input Char without print : ", echo_char=False)  
```

## iopen

`iopen(path, data=None, regex=None, css_select=None, xpath=None, file_append=False)`

Membaca atau Tulis pada path yang bisa merupakan FILE maupun URL.  

Baca File :  
- Membaca seluruh file.  
- Jika berhasil content dapat diparse dengan regex.  
- Apabila File berupa html, dapat diparse dengan css atau xpath.  

Tulis File :  
- Menulis pada file.  
- Jika file tidak ada maka akan dibuat.  
- Jika file memiliki content maka akan di overwrite.  

Membaca URL :  
- Mengakses URL dan mengembalikan isi html nya berupa teks.  
- Content dapat diparse dengan regex, css atau xpath.  

Tulis URL :  
- Mengirimkan data dengan metode POST ke url.  
- Jika berhasil dan response memiliki content, maka dapat diparse dengan regex, css atau xpath.  


```python  
# FILE  
print(iopen("__iopen.txt", "mana aja"))  
print(iopen("__iopen.txt", regex="(\w+)"))  
# URL  
print(iopen("https://www.google.com/", css_select="a"))  
print(iopen("https://www.google.com/", dict(coba="dulu"), xpath="//a"))  
```

Output:
```py
8
['mana', 'aja']
[<Element a at 0x79514bd220>, <Element a at 0x79513a77a0>, <Element a at 0x79513a7980>, <Element a at 0x79513a7cf0>, <Element a at 0x79513a7d90>, <Element a at 0x79513a7ed0>, <Element a at 0x79513a7ca0>, <Element a at 0x79513a5ea0>, <Element a at 0x79513a63a0>, <Element a at 0x79513a6350>, <Element a at 0x79513a6710>, <Element a at 0x79513a6ee0>, <Element a at 0x79513a40f0>, <Element a at 0x79513a4320>, <Element a at 0x79513a4230>, <Element a at 0x79513a70c0>, <Element a at 0x79513a4a00>, <Element a at 0x79513a4a50>]
False
```

## iprint

`iprint(*args, color=None, sort_dicts=False, **kwargs)`

Improve print function dengan menambahkan color dan pretty print  
Color menggunakan colorama Fore + Back + Style  

```python  
iprint('yang ini', {'12':12,'sdsd':{'12':21,'as':[88]}}, color=colorama.Fore.BLUE + colorama.Style.BRIGHT)  
```

Output:
```py
[34m[1myang ini[0m [34m[1m{'12': 12, 'sdsd': {'12': 21, 'as': [88]}}[0m
```

## irange

`irange(start, finish, step=1)`

Meningkatkan fungsi range() dari python untuk pengulangan menggunakan huruf  

```python  
print(irange('a', 'c'))  
print(irange('z', 'a', 10))  
print(list(irange('a', 'z', 10)))  
print(list(irange(1, '7')))  
print(list(irange(10, 5)))  
```

Output:
```py
<generator object irange at 0x79512de680>
<generator object irange at 0x79512de680>
['a', 'k', 'u']
[1, 2, 3, 4, 5, 6, 7]
[10, 9, 8, 7, 6, 5]
```

## ireplace

`ireplace(string: str, replacements: dict, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL)`

STRing TRanslate mengubah string menggunakan kamus dari dict.  
Replacement dapat berupa text biasa ataupun regex pattern.  
Apabila replacement berupa regex, gunakan raw string `r"..."`  
Untuk regex capturing gunakan `(...)`, dan untuk mengaksesnya gunakan `\1`, `\2`, .., dst.  

```python  
text = 'aku ini mau ke sini'  
replacements = {  
    "sini": "situ",  
    r"(ini)": r"itu dan \1",  
}  
print(ireplace(text, replacements))  
```

Output:
```py
aku itu dan ini mau ke situ
```

## is_empty

`is_empty(variable, empty=[None, False, 0, 0, '0', '', '-0', '\n', '\t', set(), {}, [], ()])`

Mengecek apakah variable setara dengan nilai kosong pada empty.  

Pengecekan nilai yang setara menggunakan simbol '==', sedangkan untuk  
pengecekan lokasi memory yang sama menggunakan keyword 'is'  

```python  
print(is_empty("teks"))  
print(is_empty(True))  
print(is_empty(False))  
print(is_empty(None))  
print(is_empty(0))  
print(is_empty([]))  
```

Output:
```py
False
False
True
True
True
True
```

## is_iterable

`is_iterable(var, str_is_iterable=False)`

Mengecek apakah suatu variabel bisa dilakukan forloop atau tidak  

```python  
s = 'ini string'  
print(is_iterable(s))  

l = [12,21,2,1]  
print(is_iterable(l))  

r = range(100)  
print(is_iterable(r))  

d = {'a':1, 'b':2}  
print(is_iterable(d.values()))  
```

Output:
```py
False
True
True
True
```

## is_valid_url

`is_valid_url(path)`

Mengecek apakah path merupakan URL yang valid atau tidak.  
Cara ini merupakan cara yang paling efektif.  

```python  
print(is_valid_url("https://chat.openai.com/?model=text-davinci-002-render-sha"))  
print(is_valid_url("https://chat.openai.com/?model/=text-dav/inci-002-render-sha"))  
```

Output:
```py
True
True
```

## iscandir

`iscandir(folder_name='.', glob_pattern='*', recursive=True, scan_file=True, scan_folder=True)`

Mempermudah scandir untuk mengumpulkan folder dan file.  

```python  
print(iscandir())  
print(list(iscandir("./", recursive=False, scan_file=False)))  
```

Output:
```py
<generator object iscandir at 0x7954903640>
[PosixPath('.git'), PosixPath('.vscode'), PosixPath('pypipr')]
```

## isplit

`isplit(text, separator='', include_separator=False)`

Memecah text menjadi list berdasarkan separator.  

```python  
t = '/ini/contoh/path/'  
print(isplit(t, separator='/'))  
```

Output:
```py
['', 'ini', 'contoh', 'path', '']
```

## log

`log(text=None)`

Decorator untuk mempermudah pembuatan log karena tidak perlu mengubah fungsi yg sudah ada.  
Melakukan print ke console untuk menginformasikan proses yg sedang berjalan didalam program.  

```py  
@log  
def some_function():  
    pass  

@log()  
def some_function_again():  
    pass  

@log("Calling some function")  
def some_function_more():  
    pass  

some_function()  
some_function_again()  
some_function_more()  
```

## password_generator

`password_generator(length=8, characters=None)`

Membuat pssword secara acak  

```python  
print(password_generator())  
```

## pip_freeze_without_version

`pip_freeze_without_version(filename=None)`

Memberikan list dari dependencies yang terinstall tanpa version.  
Bertujuan untuk menggunakan Batteries Included Python.  

```py  
print(pip_freeze_without_version())  
```

## poetry_publish

`poetry_publish(token=None)`

Publish project to pypi,org  

```py  
poetry_publish()  
```

## poetry_update_version

`poetry_update_version(mayor=False, minor=False, patch=True)`

Update versi pada pyproject.toml menggunakan poetry  

```py  
poetry_update_version()  
```

## print_colorize

`print_colorize(text, color='\x1b[32m', bright='\x1b[1m', color_end='\x1b[0m', text_start='', text_end='\n')`

Print text dengan warna untuk menunjukan text penting  

```py  
print_colorize("Print some text")  
print_colorize("Print some text", color=colorama.Fore.RED)  
```

## print_dir

`print_dir(var, colorize=True)`

Print property dan method yang tersedia pada variabel  

```python  
p = pathlib.Path("https://www.google.com/")  
print_dir(p, colorize=False)  
```

Output:
```py
           __bytes__ : b'https:/www.google.com'
           __class__ : .
             __dir__ : ['__module__', '__doc__', '__slots__', '__new__', '_make_child_relpath', '__enter__', '__exit__', 'cwd', 'home', 'samefile', 'iterdir', '_scandir', 'glob', 'rglob', 'absolute', 'resolve', 'stat', 'owner', 'group', 'open', 'read_bytes', 'read_text', 'write_bytes', 'write_text', 'readlink', 'touch', 'mkdir', 'chmod', 'lchmod', 'unlink', 'rmdir', 'lstat', 'rename', 'replace', 'symlink_to', 'hardlink_to', 'link_to', 'exists', 'is_dir', 'is_file', 'is_mount', 'is_symlink', 'is_block_device', 'is_char_device', 'is_fifo', 'is_socket', 'expanduser', '__reduce__', '_parse_args', '_from_parts', '_from_parsed_parts', '_format_parsed_parts', '_make_child', '__str__', '__fspath__', 'as_posix', '__bytes__', '__repr__', 'as_uri', '_cparts', '__eq__', '__hash__', '__lt__', '__le__', '__gt__', '__ge__', 'drive', 'root', 'anchor', 'name', 'suffix', 'suffixes', 'stem', 'with_name', 'with_stem', 'with_suffix', 'relative_to', 'is_relative_to', 'parts', 'joinpath', '__truediv__', '__rtruediv__', 'parent', 'parents', 'is_absolute', 'is_reserved', 'match', '_cached_cparts', '_drv', '_hash', '_parts', '_pparts', '_root', '_str', '__getattribute__', '__setattr__', '__delattr__', '__ne__', '__init__', '__reduce_ex__', '__getstate__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__', '_flavour']
             __doc__ : Path subclass for non-Windows systems.

    On a POSIX system, instantiating a Path should return this object.
    
           __enter__ : https:/www.google.com
          __fspath__ : https:/www.google.com
        __getstate__ : (None, {'_drv': '', '_root': '', '_parts': ['https:', 'www.google.com'], '_str': 'https:/www.google.com'})
            __hash__ : 8092331206409743932
            __init__ : None
   __init_subclass__ : None
          __module__ : pathlib
          __reduce__ : (<class 'pathlib.PosixPath'>, ('https:', 'www.google.com'))
            __repr__ : PosixPath('https:/www.google.com')
          __sizeof__ : 72
           __slots__ : ()
             __str__ : https:/www.google.com
    __subclasshook__ : NotImplemented
      _cached_cparts : ['https:', 'www.google.com']
             _cparts : ['https:', 'www.google.com']
                _drv : 
            _flavour : <pathlib._PosixFlavour object at 0x795445f690>
               _hash : 8092331206409743932
              _parts : ['https:', 'www.google.com']
               _root : 
                _str : https:/www.google.com
            absolute : /data/data/com.termux/files/home/pypipr/https:/www.google.com
              anchor : 
            as_posix : https:/www.google.com
                 cwd : /data/data/com.termux/files/home/pypipr
               drive : 
              exists : False
          expanduser : https:/www.google.com
                home : /data/data/com.termux/files/home
         is_absolute : False
     is_block_device : False
      is_char_device : False
              is_dir : False
             is_fifo : False
             is_file : False
            is_mount : False
         is_reserved : False
           is_socket : False
          is_symlink : False
             iterdir : <generator object Path.iterdir at 0x795126d460>
            joinpath : https:/www.google.com
                name : www.google.com
              parent : https:
             parents : <PosixPath.parents>
               parts : ('https:', 'www.google.com')
             resolve : /data/data/com.termux/files/home/pypipr/https:/www.google.com
                root : 
                stem : www.google
              suffix : .com
            suffixes : ['.google', '.com']
```

## print_log

`print_log(text)`

Akan melakukan print ke console.  
Berguna untuk memberikan informasi proses program yg sedang berjalan.  

```py  
print_log("Standalone Log")  
```

## random_bool

`random_bool()`

Menghasilkan nilai random True atau False.  
Fungsi ini merupakan fungsi tercepat untuk mendapatkan random bool.  
Fungsi ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  

```python  
print(random_bool())  
```

Output:
```py
False
```

## set_timeout

`set_timeout(interval, func, args=None, kwargs=None)`

Menjalankan fungsi ketika sudah sekian detik.  
Apabila timeout masih berjalan tapi kode sudah selesai dieksekusi semua, maka  
program tidak akan berhenti sampai timeout selesai, kemudian fungsi dijalankan,  
kemudian program dihentikan.  

```python  
set_timeout(3, lambda: print("Timeout 3"))  
x = set_timeout(7, print, args=["Timeout 7"])  
print(x)  
print("menghentikan timeout 7")  
x.cancel()  
```

Output:
```py
<Timer(Thread-2, started 521026911488)>
menghentikan timeout 7
```

## sets_ordered

`sets_ordered(iterator)`

Hanya mengambil nilai unik dari suatu list  

```python  
array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(sets_ordered(array))  
print(list(sets_ordered(array)))  
```

Output:
```py
<generator object sets_ordered at 0x7951411b10>
[2, 3, 12, 42, 1, 43, 41, 4, 24, 32]
```

## str_cmp

`str_cmp(t1, t2)`

Membandingakan string secara incase-sensitive menggunakan lower().  
Lebih cepat dibandingkan upper(), casefold(), re.fullmatch(), len().  
perbandingan ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  

```python  
print(str_cmp('teks1', 'Teks1'))  
```

Output:
```py
True
```

## to_str

`to_str(value)`

Mengubah value menjadi string literal  

```python  
print(to_str(5))  
print(to_str([]))  
print(to_str(False))  
print(to_str(True))  
print(to_str(None))  
```

Output:
```py
5

False
True

```

# CLASS

## ComparePerformance

`ComparePerformance`

Menjalankan seluruh method dalam class,  
Kemudian membandingkan waktu yg diperlukan.  
Nilai 100 berarti yang tercepat.  
  
```python  
class ExampleComparePerformance(ComparePerformance):  
    # number = 1  
    z = 10  
  
    def a(self):  
        return (x for x in range(self.z))  
  
    def b(self):  
        return tuple(x for x in range(self.z))  
  
    def c(self):  
        return [x for x in range(self.z)]  
  
    def d(self):  
        return list(x for x in range(self.z))  
  
pprint.pprint(ExampleComparePerformance().compare_result(), depth=100)  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
```

Output:
```py
{'a': <generator object ExampleComparePerformance.a.<locals>.<genexpr> at 0x79533ac860>,
 'b': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
 'c': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 'd': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
{'a': 100, 'b': 118, 'c': 139, 'd': 144}
{'a': 100, 'b': 130, 'c': 128, 'd': 114}
{'a': 100, 'b': 119, 'c': 110, 'd': 112}
{'a': 100, 'b': 113, 'c': 100, 'd': 118}
{'a': 101, 'b': 123, 'c': 100, 'd': 120}
```

## PintUregQuantity

`PintUregQuantity`

## RunParallel

`RunParallel`

Menjalankan program secara bersamaan.  
  
- `class RunParallel` didesain hanya untuk pemrosesan data saja.  
- Penggunaannya `class RunParallel` dengan cara membuat instance sub class beserta data yg akan diproses, kemudian panggil fungsi yg dipilih `run_asyncio / run_multi_threading / run_multi_processing`, kemudian dapatkan hasilnya.  
- `class RunParallel` tidak didesain untuk menyimpan data, karena setiap module terutama module `multiprocessing` tidak dapat mengakses data kelas dari proses yg berbeda.  
- Semua methods akan dijalankan secara paralel kecuali method dengan nama yg diawali underscore `_`  
- Method untuk multithreading/multiprocessing harus memiliki 2 parameter, yaitu: `result: dict` dan `q: queue.Queue`. Parameter `result` digunakan untuk memberikan return value dari method, dan Parameter `q` digunakan untuk mengirim data antar proses.  
- Method untuk asyncio harus menggunakan keyword `async def`, dan untuk perpindahan antar kode menggunakan `await asyncio.sleep(0)`, dan keyword `return` untuk memberikan return value.  
- Return Value berupa dictionary dengan key adalah nama function, dan value adalah return value dari setiap fungsi  
- Menjalankan Multiprocessing harus berada dalam blok `if __name__ == "__main__":` karena area global pada program akan diproses lagi. Terutama pada sistem operasi windows.  
- `run_asyncio()` akan menjalankan kode dalam satu program, hanya saja alur program dapat berpindah-pindah menggunkan `await asyncio.sleep(0)`.  
- `run_multi_threading()` akan menjalankan program dalam satu CPU, hanya saja dalam thread yang berbeda. Walaupun tidak benar-benar berjalan secara bersamaan namun bisa meningkatkan kecepatan penyelesaian program, dan dapat saling mengakses resource antar program.  Akses resource antar program bisa secara langsung maupun menggunakan parameter yang sudah disediakan yaitu `result: dict` dan `q: queue.Queue`.  
- `run_multi_processing()` akan menjalankan program dengan beberapa CPU. Program akan dibuatkan environment sendiri yang terpisah dari program induk. Keuntungannya adalah program dapat benar-benar berjalan bersamaan, namun tidak dapat saling mengakses resource secara langsung. Akses resource menggunakan parameter yang sudah disediakan yaitu `result: dict` dan `q: queue.Queue`.  
  
```python  
class ExampleRunParallel(RunParallel):  
    z = "ini"  
  
    def __init__(self) -> None:  
        self.pop = random.randint(0, 100)  
  
    def _set_property_here(self, v):  
        self.prop = v  
  
    def a(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["a"] = "a"  
        q.put("from a 1")  
        q.put("from a 2")  
  
    def b(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["b"] = "b"  
        result["q_get"] = q.get()  
  
    def c(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["c"] = "c"  
        result["q_get"] = q.get()  
  
    async def d(self):  
        print("hello")  
        await asyncio.sleep(0)  
        print("hello")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["d"] = "d"  
        return result  
  
    async def e(self):  
        print("world")  
        await asyncio.sleep(0)  
        print("world")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["e"] = "e"  
        return result  
  
if __name__ == "__main__":  
    print(ExampleRunParallel().run_asyncio())  
    print(ExampleRunParallel().run_multi_threading())  
    print(ExampleRunParallel().run_multi_processing())  
```

Output:
```py
```

## html_dl

`html_dl`

Class ini digunakan untuk idumps dan iloads html

## html_ol

`html_ol`

Class ini digunakan untuk idumps dan iloads html

## html_table

`html_table`

Class ini digunakan untuk idumps dan iloads html

## html_ul

`html_ul`

Class ini digunakan untuk idumps dan iloads html
