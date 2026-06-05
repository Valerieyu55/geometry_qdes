import re

with open('debate2.html', 'r', encoding='utf-8', errors='replace') as f:
    d2_html = f.read()

with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    idx_html = f.read()

# 1. Extract three.js scripts
three_scripts = re.findall(r'<script src="https://[^>]*three[^>]*></script>', d2_html)
three_scripts_str = '\n    '.join(three_scripts)

if 'three.min.js' not in idx_html:
    idx_html = idx_html.replace('</head>', f'    {three_scripts_str}\n</head>')

# 2. Extract style
style_match = re.search(r'<style>(.*?)</style>', d2_html, re.DOTALL)
if style_match:
    d2_style = style_match.group(1).strip()
    # Remove html { font-size: 18px; } and body { ... } to avoid affecting index.html
    d2_style = re.sub(r'html\s*\{[^}]*\}', '', d2_style)
    d2_style = re.sub(r'body\s*\{[^}]*\}', '', d2_style)
    # Remove @import to prevent it from invalidating CSS if it's not at the top
    d2_style = re.sub(r'@import url\([^)]+\);', '', d2_style)
    
    idx_html = idx_html.replace('</style>', f'\n        /* Debate 2 Styles */\n        {d2_style}\n    </style>')

# 3. Extract main content
# Find the wrapper div
wrapper_start = d2_html.find('<div class="w-full max-w-5xl h-[85vh] min-h-[650px]')
if wrapper_start != -1:
    content_start = d2_html.find('>', wrapper_start) + 1
    # We want everything up to the closing div of the wrapper
    # The wrapper is followed by <script>
    script_start = d2_html.find('<!-- Three.js 3D', content_start)
    if script_start == -1:
        script_start = d2_html.find('<script>', content_start)
    
    # We need to find the last </div> before script_start
    inner_content = d2_html[content_start:script_start].strip()
    # Remove the last </div> which closes the wrapper
    last_div_idx = inner_content.rfind('</div>')
    if last_div_idx != -1:
        inner_content = inner_content[:last_div_idx].strip()
        
    # Replace the iframe in index.html with inner_content
    iframe_tag = '<iframe src="./debate2.html" class="w-full h-full border-none bg-transparent" allowfullscreen></iframe>'
    idx_html = idx_html.replace(iframe_tag, inner_content)

# 4. Extract script
script_match = re.search(r'<script>(.*?)</script>', d2_html[script_start:], re.DOTALL)
if script_match:
    d2_script = script_match.group(1).strip()
    
    # Update openD2Modal to reset to slide 0
    d2_script_reset = """
            // Reset the iframe to Slide 1 whenever opened
            const iframe = content.querySelector('iframe');
            if (iframe) {
                iframe.src = './debate2.html';
            }
"""
    new_reset = """
            // Reset to Slide 1
            if (typeof updateSlide === 'function') {
                currentSlide = 0;
                updateSlide();
            }
"""
    idx_html = idx_html.replace(d2_script_reset, new_reset)
    
    idx_html = idx_html.replace('</body>', f'\n    <!-- Debate 2 Logic -->\n    <script>\n{d2_script}\n    </script>\n</body>')

with open('index_merged.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)

print("Merged successfully to index_merged.html")
