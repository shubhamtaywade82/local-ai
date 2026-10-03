import json
import os
import shutil
import sqlite3
import time

DB_PATH = '/app/backend/data/webui.db'
TOOL_CODE_PATH = '/app/backend/openui-tool/openui.py'
TOOL_SPECS_PATH = '/app/backend/openui-tool/specs.json'
LOCALE_DIR = '/app/build/_app/immutable/chunks'


def sync_database_records():
    # Provision openui tool registration and global model defaults
    if not os.path.exists(DB_PATH) or not os.path.exists(TOOL_CODE_PATH):
        return

    with open(TOOL_CODE_PATH, 'r') as file_obj:
        tool_code = file_obj.read()

    tool_specs = '[]'
    if os.path.exists(TOOL_SPECS_PATH):
        with open(TOOL_SPECS_PATH, 'r') as file_obj:
            tool_specs = file_obj.read()

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
        tool_specs, meta, valves, now, 'openui', now
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


MIDDLEWARE_PATH = '/app/backend/open_webui/utils/middleware.py'


def patch_backend_middleware():
    # Ensure streaming chat response handler emits embeds via event_emitter
    if not os.path.exists(MIDDLEWARE_PATH):
        return

    with open(MIDDLEWARE_PATH, 'r') as file_obj:
        content = file_obj.read()

    target = '''                        await terminal_event_handler(
                            tool_function_name,
                            tool_function_params,
                            tool_result,
                            event_emitter,
                        )'''

    replacement = '''                        await terminal_event_handler(
                            tool_function_name,
                            tool_function_params,
                            tool_result,
                            event_emitter,
                        )

                        if tool_result_embeds and event_emitter:
                            await event_emitter(
                                {
                                    'type': 'embeds',
                                    'data': {
                                        'embeds': tool_result_embeds,
                                    },
                                }
                            )'''

    if target in content and replacement not in content:
        content = content.replace(target, replacement, 1)
        with open(MIDDLEWARE_PATH, 'w') as file_obj:
            file_obj.write(content)


def main():
    sync_database_records()
    patch_locale_bundle()
    patch_backend_middleware()
    print('OpenUI auto-import and default-enable provisioned successfully.')


if __name__ == '__main__':
    main()
