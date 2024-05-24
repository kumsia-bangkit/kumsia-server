## Install FastAPI

1. Buka Command Prompt (cmd) atau Terminal di dalam direktori proyek.

2. Buat Python *virtual environment* di dalamnya.

   ```shell
   python -m venv env
   ```

   > Catatan: sesuaikan dengan *executable* `python` yang ada di komputer kamu,
   > karena terkadang (misal: di Ubuntu atau macOS) Python 3 hanya bisa
   > dipanggil dengan `python3`, bukan `python`.

3. Aktifkan *virtual environment* yang telah dibuat.\
   Di Windows Powershell:

   ```shell
   .\env\Scripts\Activate.ps1
   ```
   Di Windows Git Bash:

   ```shell
   source ./env/Scripts/activate
   ```

   Di Linux/macOS:

   ```shell
   source ./env/bin/activate
   ```

   Jika berhasil, akan muncul `(env)` pada *prompt* cmd/terminal kamu.

4. Instal FastAPI pada *virtual environment* tersebut.

   ```shell
   pip install fastapi
   ```

## Run Proyek
```shell
fastapi dev app/main.py
```