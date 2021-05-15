import requests
from bs4 import BeautifulSoup
import os
import csv

URL = 'https://jdihn.go.id/search/pusat?page='
DIRECTORY = 'downloads/'
OUTPUT = 'jdihn.csv'
START_PAGE = 1
END_PAGE = 6131

def write_csv(tipe_dokumen, judul_dokumen, status, nomor_peraturan, jenis_peraturan, tempat_penetapan, tanggal_penetapan, tanggal_pengundangan, sumber, sumber_detail, urusan_pemerintah, bidang_hukum, bahasa, pemrakarsa, penandatangan, peraturan_terkait, dokumen_terkait, hasil_uji_mk, pengarang, subjek, file_url, file_size, link):
    with open(OUTPUT, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([tipe_dokumen, judul_dokumen, status, nomor_peraturan, jenis_peraturan, tempat_penetapan, tanggal_penetapan, tanggal_pengundangan, sumber, sumber_detail, urusan_pemerintah, bidang_hukum, bahasa, pemrakarsa, penandatangan, peraturan_terkait, dokumen_terkait, hasil_uji_mk, pengarang, subjek, file_url, file_size, link])

def write_csv_header():
    with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['tipe_dokumen', 'judul_dokumen', 'status', 'nomor_peraturan', 'jenis_peraturan', 'tempat_penetapan', 'tanggal_penetapan', 'tanggal_pengundangan', 'sumber', 'sumber_detail', 'urusan_pemerintah', 'bidang_hukum', 'bahasa', 'pemrakarsa', 'penandatangan', 'peraturan_terkait', 'dokumen_terkait', 'hasil_uji_mk', 'pengarang', 'subjek', 'file_url', 'file_size', 'link'])

def main():
    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)

    write_csv_header()

    for i in range(START_PAGE, END_PAGE+1, 1):
        url = "{}{}".format(URL, i)
        res = requests.get(url)
        
        page = BeautifulSoup(res.text, 'html.parser')
        items = page.select('.item')
        print("Crawling: {}".format(url))
        for (index, item) in enumerate(items):
            sumber = item.select('small')[0].get_text()
            link = item.select('a')[1].get('href')

            detail = requests.get(link)
            detail_page = BeautifulSoup(detail.text, 'html.parser')

            tipe_dokumen = detail_page.select('h5')[0].get_text()
            judul_dokumen = detail_page.select('h3')[1].get_text()
            status = detail_page.select('.btn-warning')[0].get_text()

            ps = detail_page.select('p')
            nomor_peraturan = ps[0].get_text()
            jenis_peraturan = ps[1].get_text()
            tempat_penetapan = ps[2].get_text()
            tanggal_penetapan = ps[3].get_text()
            tanggal_pengundangan = ps[4].get_text()
            sumber_detail = ps[5].get_text()
            urusan_pemerintah = ps[6].get_text()
            bidang_hukum = ps[7].get_text()
            bahasa = ps[8].get_text()
            pemrakarsa = ps[9].get_text()
            penandatangan = ps[10].get_text()
            peraturan_terkait = ps[11].get_text()
            dokumen_terkait = ps[12].get_text()
            hasil_uji_mk = ps[13].get_text()
            pengarang = ps[14].get_text()
            subjek = ps[15].get_text()

            try:
                file_url = detail_page.select('embed')[0].get('src')
                file_response = requests.head(file_url)
                file_size = file_response.headers.get('content-length', 0)
            except:
                file_url = None
                file_size = 0

            print("--> Writing {} row".format(index+1))
            write_csv(tipe_dokumen, judul_dokumen, status, nomor_peraturan, jenis_peraturan, tempat_penetapan, tanggal_penetapan, tanggal_pengundangan, sumber, sumber_detail, urusan_pemerintah, bidang_hukum, bahasa, pemrakarsa, penandatangan, peraturan_terkait, dokumen_terkait, hasil_uji_mk, pengarang, subjek, file_url, file_size, link)

if __name__ == "__main__":
    main()