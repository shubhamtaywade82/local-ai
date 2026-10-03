import json
import os
import shutil
import sqlite3
import time

DB_PATH = '/app/backend/data/webui.db'
TOOL_CODE_PATH = '/app/backend/openui-tool/openui.py'
LOCALE_DIR = '/app/build/_app/immutable/chunks'


def sync_database_records():
    # Provision openui tool registration and global model defaults
    if not os.path.exists(DB_PATH) or not os.path.exists(TOOL_CODE_PATH):
        return

    with open(TOOL_CODE_PATH, 'r') as file_obj:
        tool_code = file_obj.read()

    now = int(time.time())
    valves = json.dumps({'cdn_base_url': 'http://localhost:8081'})
    meta = json.dumps({'description': 'Renders interactive generative UI components using OpenUI Lang.'})

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM user WHERE role = 'admin' LIMIT 1")
    admin_row = cursor.fetchone()
    admin_id = admin_row[0] if admin_row else 'default'

    cursor.execute("""
        INSERT OR REPLACE INTO tool (id, user_id, name, content, specs, meta, valves, updated_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM tool WHERE id = ?), ?))
    """, (
        'openui', admin_id, 'OpenUI - Generative UI', tool_code,
        '[{"name": "render_openui"}]', meta, valves, now, 'openui', now
    ))

    # Apply OpenUI tool attachment to all models by default
    default_metadata = json.dumps({
        'capabilities': {'tools': True},
        'toolIds': ['openui'],
        'tools': ['openui']
    })
    cursor.execute("""
        INSERT OR REPLACE INTO config (key, value, updated_at)
        VALUES ('models.default_metadata', ?, ?)
    """, (default_metadata, now))

    conn.commit()
    conn.close()


def patch_locale_bundle():
    # Upstream en-GB locale bundle leaves shortcut keys as empty strings
    gb_chunk = os.path.join(LOCALE_DIR, 'Ci6R2QNF.js')
    us_chunk = os.path.join(LOCALE_DIR, 'B9zysbjG.js')
    if os.path.exists(us_chunk) and os.path.exists(gb_chunk):
        shutil.copyfile(us_chunk, gb_chunk)


def main():
    sync_database_records()
    patch_locale_bundle()
    print('OpenUI auto-import and default-enable provisioned successfully.')


if __name__ == '__main__':
    main()
