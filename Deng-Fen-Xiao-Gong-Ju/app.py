import streamlit as st
import streamlit.components.v1 as components
import json
import os

SAVE_PATH = "numbers_dict.json"

# Initialize the number dictionary with all valid keys
VALID_KEYS = [
    1, 2, 5, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20,
    23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38,
    40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53,
    55, 56, 57, 58, 59, 60, 61, 62, 63, 64
]

def load_dict():
    """Load the dictionary from JSON file"""
    if os.path.exists(SAVE_PATH):
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {int(k): (int(v) if v is not None else None) for k, v in data.items()}
        except Exception:
            return None
    return None

def save_dict(numbers_dict):
    """Save the dictionary to JSON file"""
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in numbers_dict.items()}, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def initialize_dict():
    """Initialize dictionary with all keys set to None"""
    return {k: None for k in VALID_KEYS}

def auto_clear_on_startup():
    """Auto-clear all values on startup and save to file"""
    cleared_dict = initialize_dict()
    save_dict(cleared_dict)
    return cleared_dict

# Initialize session state
if "numbers_dict" not in st.session_state:
    # Auto-clear on startup
    st.session_state.numbers_dict = auto_clear_on_startup()
    st.session_state.startup_message = True
else:
    st.session_state.startup_message = False

if "message" not in st.session_state:
    st.session_state.message = None
if "message_type" not in st.session_state:
    st.session_state.message_type = "info"

# Page config
st.set_page_config(page_title="登分小工具", layout="wide")

# Title
st.title("登分小工具")

# Show startup message
if st.session_state.startup_message:
    st.info("✓ 系統已啟動，所有數值已自動清空")
    st.session_state.startup_message = False

# Instructions
with st.expander("📖 使用說明", expanded=False):
    st.markdown("""
    **如何使用：**
    - 輸入數字（前兩位座號，後2-3位為成績）
    - 例如：`1025` 表示10號25分
    - 例如：`45123` 表示將45號123分
    - 點擊「顯示所有對應」查看完整列表
    - 點擊「複製所有值」將所有值複製到剪貼簿
    - 點擊「清空所有值」重置所有數據
    """)

# Main input section
st.subheader("輸入成績")

with st.form(key="input_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input(
            "輸入 4-5 位數字",
            max_chars=5,
            placeholder="例如：1025 或 45123"
        )
    
    with col2:
        st.write("")  # Spacing
        submit_button = st.form_submit_button("提交", type="primary", use_container_width=True)

# Process input
if submit_button and user_input:
    user_input = user_input.strip()
    
    # Validate input
    if not user_input.isdigit() or len(user_input) not in [4, 5]:
        st.session_state.message = "❌ 格式不符"
        st.session_state.message_type = "error"
    else:
        key = int(user_input[:2])
        value = int(user_input[2:])
        
        if key not in VALID_KEYS:
            st.session_state.message = f"❌ 錯誤：座號 {key:02d} 不在系統中，請重新輸入"
            st.session_state.message_type = "error"
        else:
            st.session_state.numbers_dict[key] = value
            save_dict(st.session_state.numbers_dict)
            st.session_state.message = f"✅ 成功：座號 {key:02d} 已設定為 {value}"
            st.session_state.message_type = "success"
            st.rerun()

# Display message
if st.session_state.message:
    if st.session_state.message_type == "success":
        st.success(st.session_state.message)
    elif st.session_state.message_type == "error":
        st.error(st.session_state.message)
    else:
        st.info(st.session_state.message)
    st.session_state.message = None

# Action buttons
st.subheader("操作")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 顯示所有對應", use_container_width=True):
        st.session_state.show_all = True

with col2:
    values = ["" if st.session_state.numbers_dict[k] is None else str(st.session_state.numbers_dict[k]) 
              for k in sorted(VALID_KEYS)]
    
    if all(v == "" for v in values):
        st.button("📎 複製所有值", disabled=True, use_container_width=True)
        if st.session_state.get("show_copy_warning"):
            st.warning("⚠️ 沒有可複製的值")
    else:
        text = "\n".join(values)
        # Escape special characters for JavaScript
        text_escaped = text.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
        
        # Create a custom HTML button with direct clipboard access
        copy_button_html = f"""
        <div style="width: 100%;">
            <button id="copyBtn" style="
                width: 100%;
                padding: 0.5rem 1rem;
                background-color: #ff4b4b;
                color: white;
                border: none;
                border-radius: 0.5rem;
                font-size: 1rem;
                cursor: pointer;
                font-weight: 500;
            ">📎 複製所有值</button>
            <div id="copyStatus" style="margin-top: 0.5rem; font-size: 0.875rem;"></div>
            <textarea id="fallbackText" style="
                position: absolute;
                left: -9999px;
                width: 1px;
                height: 1px;
            ">{text_escaped}</textarea>
        </div>
        <script>
            const btn = document.getElementById('copyBtn');
            const status = document.getElementById('copyStatus');
            const fallbackText = document.getElementById('fallbackText');
            
            btn.addEventListener('click', async function() {{
                const text = `{text_escaped}`;
                let success = false;
                
                // Method 1: Try modern Clipboard API
                try {{
                    await navigator.clipboard.writeText(text);
                    success = true;
                }} catch (err) {{
                    // Method 2: Fallback to execCommand (works on mobile Safari)
                    try {{
                        fallbackText.value = text;
                        fallbackText.select();
                        fallbackText.setSelectionRange(0, 99999);
                        success = document.execCommand('copy');
                    }} catch (err2) {{
                        success = false;
                    }}
                }}
                
                if (success) {{
                    status.innerHTML = '<span style="color: #0e7c46;">✅ 值已複製到剪貼簿</span>';
                    btn.style.backgroundColor = '#0e7c46';
                    setTimeout(() => {{
                        btn.style.backgroundColor = '#ff4b4b';
                        status.innerHTML = '';
                    }}, 2000);
                }} else {{
                    status.innerHTML = '<span style="color: #ff8c00;">⚠️ 複製失敗，請使用下方文字框手動複製</span>';
                }}
            }});
        </script>
        """
        
        components.html(copy_button_html, height=100)
        
        # Always show the fallback text area for manual copy
        with st.expander("📝 手動複製（如果上方按鈕無效）"):
            st.text_area("所有值", value=text, height=200, label_visibility="collapsed")

with col3:
    if st.button("🗑️ 清空所有值", use_container_width=True):
        st.session_state.numbers_dict = initialize_dict()
        save_dict(st.session_state.numbers_dict)
        st.success("✅ 所有值已清空")
        st.rerun()

# Display all mappings in a table
if "show_all" in st.session_state and st.session_state.show_all:
    st.subheader("所有對應列表")
    
    # Create columns for better display
    cols = st.columns(4)
    sorted_keys = sorted(VALID_KEYS)
    
    for idx, key in enumerate(sorted_keys):
        value = st.session_state.numbers_dict[key]
        col_idx = idx % 4
        
        with cols[col_idx]:
            if value is not None:
                st.markdown(f"**{key:02d}** → `{value}`")
            else:
                st.markdown(f"**{key:02d}** → —")
    
    if st.button("隱藏列表"):
        st.session_state.show_all = False
        st.rerun()

# Statistics
st.divider()
filled_count = sum(1 for v in st.session_state.numbers_dict.values() if v is not None)
total_count = len(VALID_KEYS)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("總人數", total_count)
with col2:
    st.metric("已填寫", filled_count)
with col3:
    st.metric("未填寫", total_count - filled_count)

# Grid view
st.subheader("快速檢視")
st.caption("綠色表示已設定值，灰色表示未設定")

# Create a grid layout
cols_per_row = 10
rows = []
current_row = []

for key in sorted(VALID_KEYS):
    value = st.session_state.numbers_dict[key]
    if value is not None:
        current_row.append(f"🟢 {key:02d}")
    else:
        current_row.append(f"⚪ {key:02d}")
    
    if len(current_row) == cols_per_row:
        rows.append(current_row)
        current_row = []

if current_row:
    rows.append(current_row)

for row in rows:
    cols = st.columns(cols_per_row)
    for idx, item in enumerate(row):
        with cols[idx]:
            st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{item}</div>", 
                       unsafe_allow_html=True)

# Auto-focus input field after page load
components.html(
    """
    <script>
        // Wait for the page to fully load
        setTimeout(function() {
            // Find the input field and focus it
            const inputs = window.parent.document.querySelectorAll('input[type="text"]');
            if (inputs.length > 0) {
                inputs[0].focus();
            }
        }, 100);
    </script>
    """,
    height=0,
)
