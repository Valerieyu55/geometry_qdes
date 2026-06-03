import re

with open('old_index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change default tab
content = content.replace("const [activeTab, setActiveTab] = useState('home');", "const [activeTab, setActiveTab] = useState('crossSection');")

# Remove the sidebar (from `<div className="w-full md:w-[320px] space-y-4 shrink-0">` to its closing tag)
# The sidebar ends before `<div className="flex-1 w-full max-w-4xl no-scrollbar overflow-y-auto">`
start_sidebar = content.find('<div className="w-full md:w-[320px] space-y-4 shrink-0">')
end_sidebar = content.find('<div className="flex-1 w-full max-w-4xl no-scrollbar overflow-y-auto">')

if start_sidebar != -1 and end_sidebar != -1:
    content = content[:start_sidebar] + content[end_sidebar:]

# Remove `max-w-4xl` and `max-w-[1440px]` so it fills the screen like platonic.html
content = content.replace('max-w-4xl', 'w-full')
content = content.replace('max-w-[1440px]', 'w-full')
content = content.replace('min-h-screen flex flex-col md:flex-row gap-4 p-4 md:p-8 w-full mx-auto', 'min-h-screen flex flex-col md:flex-row p-0 m-0 w-full')

with open('cross_section.html', 'w', encoding='utf-8') as f:
    f.write(content)
