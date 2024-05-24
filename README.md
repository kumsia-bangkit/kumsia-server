## Install FastAPI

1. Buka Command Prompt (cmd) atau Terminal di dalam direktori proyek.

2. Buat Python *virtual environment* di dalamnya.

   ```shell
   python -m venv env
   ```

   > Catatan: sesuaikan dengan *executable* `python` yang ada di komputer kamu,
   > karena terkadang (misal: di Ubuntu atau macOS) Python 3 hanya bisa
   > dipanggil dengan `python3`, bukan `python`.

2. Instal project libraries pada *virtual environment* tersebut.

   ```shell
   ./env/Scripts/activate
   pip install -r requirements.txt
   ```
   
3. Aktifkan *virtual environment* yang telah dibuat dan menjalankan server uvicorn
   ```
   cd app
   ./runserver.sh
   ```
   * Menggunakan git bash, untuk menjalankan shell script