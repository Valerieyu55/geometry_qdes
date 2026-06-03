import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add the new mode button
btn_cone = `<button onclick="setStep2Mode('cone')" id="btn-mode-cone" class="px-3 py-1.5 rounded text-slate-400 text-xs tech-font hover:text-cyan-300 transition-colors border border-transparent" data-i18n="modeCone">圓錐生成模式</button>`
btn_nets = `\n                                <button onclick="setStep2Mode('nets')" id="btn-mode-nets" class="px-3 py-1.5 rounded text-slate-400 text-xs tech-font hover:text-cyan-300 transition-colors border border-transparent">展開圖鑑模式</button>`
content = content.replace(btn_cone, btn_cone + btn_nets)

# 2. Add ID to teacher panel
teacher_panel_str = `<div class="h-28 border-t border-cyan-500/20 bg-slate-950/80 backdrop-blur-md flex flex-col justify-center items-center rounded-b-2xl relative z-20">`
new_teacher_panel_str = `<div id="s2-teacher-panel" class="h-28 border-t border-cyan-500/20 bg-slate-950/80 backdrop-blur-md flex flex-col justify-center items-center rounded-b-2xl relative z-20">`
content = content.replace(teacher_panel_str, new_teacher_panel_str)

# 3. Insert s2-nets-area right after s2-teacher-panel block
nets_area_html = """
                        <!-- Nets Area for Step 2 -->
                        <div id="s2-nets-area" class="flex-1 flex flex-col hidden relative z-10 px-6 pb-6 pt-2 overflow-hidden">
                            <div class="flex gap-2 p-2 bg-slate-900/60 rounded-xl border border-cyan-500/30 flex-wrap justify-center max-w-3xl mx-auto w-full z-20" id="s2-nets-tabs">
                                <!-- Tabs injected via JS -->
                            </div>
                            <div class="flex-1 glass-panel rounded-2xl flex flex-col items-center justify-center p-6 relative mt-4 max-w-3xl mx-auto w-full">
                                <div id="s2-nets-3d-container" class="w-full flex-1 flex items-center justify-center perspective-1000 cursor-grab relative z-10">
                                    <div id="s2-nets-scene" class="scene" style="transform-style: preserve-3d; transform: rotateX(-15deg) rotateY(-25deg);">
                                       <!-- 3D injected via JS -->
                                    </div>
                                </div>
                                <div class="w-full bg-slate-900/80 border border-slate-700 p-4 rounded-xl mt-4 z-20 shadow-lg relative">
                                    <div class="flex justify-between items-center mb-2">
                                        <span class="text-xs font-bold text-slate-400 tracking-widest">展開 / 摺疊程度</span>
                                        <span id="s2-nets-fp-val" class="text-cyan-400 font-mono text-sm font-bold">0%</span>
                                    </div>
                                    <input type="range" id="s2-nets-slider" min="0" max="100" value="0" oninput="updateNetsFold(this.value)" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500">
                                </div>
                                <p id="s2-nets-note" class="text-[11px] text-slate-400 mt-4 text-center tracking-wide z-20"></p>
                            </div>
                        </div>
"""
# find the end of view-step2
# The next view is id="view-step3"
view_step3_idx = content.find('<div id="view-step3"')
insert_idx = content.rfind('</div>', 0, view_step3_idx) - 4
content = content[:insert_idx] + nets_area_html + content[insert_idx:]

# 4. Modify setStep2Mode function
old_set_step2_mode = """        function setStep2Mode(mode) {
            step2Mode = mode;
            resetStep2Rotation();
            
            const btnCyl = document.getElementById('btn-mode-cyl');
            const btnCone = document.getElementById('btn-mode-cone');
            
            if(mode === 'cylinder') {
                btnCyl.className = 'px-3 py-1.5 rounded bg-cyan-500/20 text-cyan-300 text-xs tech-font border border-cyan-500/50';
                btnCone.className = 'px-3 py-1.5 rounded text-slate-400 text-xs tech-font hover:text-cyan-300 transition-colors border border-transparent';
                
                document.getElementById('planar-path').setAttribute('d', 'M0,0 L80,0 L80,160 L0,160 Z');
                document.getElementById('planar-gen').setAttribute('x1', '80');
                document.getElementById('planar-gen').setAttribute('y1', '0');
                document.getElementById('planar-gen').setAttribute('x2', '80');
                document.getElementById('planar-gen').setAttribute('y2', '160');
                document.getElementById('generatrix-label').style.top = '50%';
                document.getElementById('generatrix-label').style.left = '85px';
            } else {
                btnCone.className = 'px-3 py-1.5 rounded bg-cyan-500/20 text-cyan-300 text-xs tech-font border border-cyan-500/50';
                btnCyl.className = 'px-3 py-1.5 rounded text-slate-400 text-xs tech-font hover:text-cyan-300 transition-colors border border-transparent';
                
                document.getElementById('planar-path').setAttribute('d', 'M0,0 L80,160 L0,160 Z');
                document.getElementById('planar-gen').setAttribute('x1', '0');
                document.getElementById('planar-gen').setAttribute('y1', '0');
                document.getElementById('planar-gen').setAttribute('x2', '80');
                document.getElementById('planar-gen').setAttribute('y2', '160');
                document.getElementById('generatrix-label').style.top = '50%';
                document.getElementById('generatrix-label').style.left = '45px';
            }
            
            generateSolid(mode);
            switchLanguage(document.getElementById('lang-select').value);
        }"""

new_set_step2_mode = """        function setStep2Mode(mode) {
            step2Mode = mode;
            resetStep2Rotation();
            
            const btnCyl = document.getElementById('btn-mode-cyl');
            const btnCone = document.getElementById('btn-mode-cone');
            const btnNets = document.getElementById('btn-mode-nets');
            const sceneArea = document.getElementById('s2-scene-area');
            const teacherPanel = document.getElementById('s2-teacher-panel');
            const netsArea = document.getElementById('s2-nets-area');
            
            if(btnCyl) btnCyl.className = 'px-3 py-1.5 rounded text-slate-400 text-xs tech-font hover:text-cyan-300 transition-colors border border-transparent';
            if(btnCone) btnCone.className = 'px-3 py-1.5 rounded text-slate-400 text-xs tech-font hover:text-cyan-300 transition-colors border border-transparent';
            if(btnNets) btnNets.className = 'px-3 py-1.5 rounded text-slate-400 text-xs tech-font hover:text-cyan-300 transition-colors border border-transparent';
            
            if(mode === 'nets') {
                if(btnNets) btnNets.className = 'px-3 py-1.5 rounded bg-cyan-500/20 text-cyan-300 text-xs tech-font border border-cyan-500/50';
                if(sceneArea) sceneArea.classList.add('hidden');
                if(teacherPanel) teacherPanel.classList.add('hidden');
                if(netsArea) netsArea.classList.remove('hidden');
                initNetsGallery();
            } else {
                if(sceneArea) sceneArea.classList.remove('hidden');
                if(teacherPanel) teacherPanel.classList.remove('hidden');
                if(netsArea) netsArea.classList.add('hidden');
                
                if(mode === 'cylinder') {
                    if(btnCyl) btnCyl.className = 'px-3 py-1.5 rounded bg-cyan-500/20 text-cyan-300 text-xs tech-font border border-cyan-500/50';
                    document.getElementById('planar-path').setAttribute('d', 'M0,0 L80,0 L80,160 L0,160 Z');
                    document.getElementById('planar-gen').setAttribute('x1', '80');
                    document.getElementById('planar-gen').setAttribute('y1', '0');
                    document.getElementById('planar-gen').setAttribute('x2', '80');
                    document.getElementById('planar-gen').setAttribute('y2', '160');
                    document.getElementById('generatrix-label').style.top = '50%';
                    document.getElementById('generatrix-label').style.left = '85px';
                } else {
                    if(btnCone) btnCone.className = 'px-3 py-1.5 rounded bg-cyan-500/20 text-cyan-300 text-xs tech-font border border-cyan-500/50';
                    document.getElementById('planar-path').setAttribute('d', 'M0,0 L80,160 L0,160 Z');
                    document.getElementById('planar-gen').setAttribute('x1', '0');
                    document.getElementById('planar-gen').setAttribute('y1', '0');
                    document.getElementById('planar-gen').setAttribute('x2', '80');
                    document.getElementById('planar-gen').setAttribute('y2', '160');
                    document.getElementById('generatrix-label').style.top = '50%';
                    document.getElementById('generatrix-label').style.left = '45px';
                }
                generateSolid(mode);
            }
            switchLanguage(document.getElementById('lang-select').value);
        }"""
content = content.replace(old_set_step2_mode, new_set_step2_mode)

# 5. Add Nets logic at the end of <script>
js_code = """
        // --- Nets Gallery Logic ---
        const netShapesData = {
          cube: {
            name: '正方體', icon: '🧊',
            color: 'border-cyan-400', bgColor: 'bg-cyan-900/40', tagColor: 'bg-cyan-500',
            note: '💡 正方體有 11 種不同的展開圖！這只是最經典的十字型。'
          },
          triPrism: {
            name: '正三角柱', icon: '🔺',
            color: 'border-purple-400', bgColor: 'bg-purple-900/40', tagColor: 'bg-purple-500',
            note: '💡 三個長方形並排，兩端各接一個三角形底面。'
          },
          cylinder: {
            name: '圓柱', icon: '🛢️',
            color: 'border-emerald-400', bgColor: 'bg-emerald-900/40', tagColor: 'bg-emerald-500',
            note: '💡 側面展開後是一個長方形，寬 = 底圓的周長 2πr。'
          },
          cone: {
            name: '圓錐', icon: '🍦',
            color: 'border-red-400', bgColor: 'bg-red-900/40', tagColor: 'bg-red-500',
            note: '💡 側面展開後是一個扇形，弧長 = 底圓的周長，半徑 = 母線長。'
          },
          tetra: {
            name: '正四面體', icon: '🔻',
            color: 'border-indigo-400', bgColor: 'bg-indigo-900/40', tagColor: 'bg-indigo-500',
            note: '💡 將所有面攤平後，看起來就像一朵三瓣花。'
          },
          sqPyramid: {
            name: '四角錐', icon: '🏔️',
            color: 'border-amber-400', bgColor: 'bg-amber-900/40', tagColor: 'bg-amber-500',
            note: '💡 像埃及金字塔！正方形底面的每條邊各接一個等腰三角形。'
          }
        };

        let currentNetShape = 'cube';
        let currentFoldPercent = 0;
        let isNetsGalleryInit = false;

        function getFoldableFaceHTML(label, edge, w, h, foldPercent, colorClass, maxAngle=90, clipPath='none', childrenHTML='') {
            const angle = (foldPercent / 100) * maxAngle;
            let placement = ""; let origin = ""; let transform = "";
            if (edge === 'top') { placement = `bottom: 100%; left: 0;`; origin = 'bottom center'; transform = `rotateX(${-angle}deg)`; }
            else if (edge === 'bottom') { placement = `top: 100%; left: 0;`; origin = 'top center'; transform = `rotateX(${angle}deg)`; }
            else if (edge === 'left') { placement = `right: 100%; top: 0;`; origin = 'right center'; transform = `rotateY(${angle}deg)`; }
            else if (edge === 'right') { placement = `left: 100%; top: 0;`; origin = 'left center'; transform = `rotateY(${-angle}deg)`; }

            return `
            <div class="absolute transition-transform duration-500"
                 style="${placement} width: ${w}px; height: ${h}px; transform-origin: ${origin}; transform: ${transform}; transform-style: preserve-3d;">
                <div class="w-full h-full flex items-center justify-center font-bold text-[10px] tracking-[0.2em] text-white border ${colorClass} backdrop-blur-sm"
                     style="clip-path: ${clipPath}; -webkit-clip-path: ${clipPath};">
                    ${label}
                </div>
                ${childrenHTML}
            </div>`;
        }

        function renderNetsHTML(shapeId, fp) {
            const s = 70;
            let html = '';
            if (shapeId === 'cube') {
                html = `
                <div class="relative" style="width: ${s}px; height: ${s}px; transform-style: preserve-3d;">
                    <div class="absolute inset-0 border flex items-center justify-center font-bold text-[10px] tracking-[0.2em] text-white bg-cyan-500/20 border-cyan-400 backdrop-blur-sm">前</div>
                    ${getFoldableFaceHTML('左', 'left', s, s, fp, 'bg-cyan-500/20 border-cyan-400')}
                    ${getFoldableFaceHTML('右', 'right', s, s, fp, 'bg-cyan-500/20 border-cyan-400')}
                    ${getFoldableFaceHTML('底', 'bottom', s, s, fp, 'bg-cyan-500/20 border-cyan-400')}
                    ${getFoldableFaceHTML('頂', 'top', s, s, fp, 'bg-cyan-500/20 border-cyan-400', 90, 'none', 
                        getFoldableFaceHTML('後', 'top', s, s, fp, 'bg-cyan-500/40 border-cyan-300')
                    )}
                </div>`;
            } else if (shapeId === 'triPrism') {
                const triH = s * 0.866;
                html = `
                <div class="relative" style="width: ${s}px; height: ${s * 1.2}px; transform-style: preserve-3d;">
                    <div class="absolute inset-0 border flex items-center justify-center font-bold text-[10px] tracking-[0.2em] text-white bg-purple-500/20 border-purple-400 backdrop-blur-sm">側1</div>
                    ${getFoldableFaceHTML('側2', 'left', s, s * 1.2, fp, 'bg-purple-500/20 border-purple-400', 120)}
                    ${getFoldableFaceHTML('側3', 'right', s, s * 1.2, fp, 'bg-purple-500/20 border-purple-400', 120)}
                    ${getFoldableFaceHTML('△上', 'top', s, triH, fp, 'bg-purple-500/40 border-purple-300', 90, 'polygon(50% 0%, 0% 100%, 100% 100%)')}
                    ${getFoldableFaceHTML('△下', 'bottom', s, triH, fp, 'bg-purple-500/40 border-purple-300', 90, 'polygon(50% 100%, 0% 0%, 100% 0%)')}
                </div>`;
            } else if (shapeId === 'cylinder') {
                const h = s * 1.5; const r = s / 2; const nStrips = 30;
                const circ = Math.PI * s; const stripW = circ / nStrips; const angleStep = 360 / nStrips;
                const p = fp / 100;
                let strips = '';
                for (let i=0; i<nStrips; i++) {
                    const targetAngle = (i - nStrips / 2 + 0.5) * angleStep;
                    const rad = (targetAngle * Math.PI) / 180;
                    const xFlat = (i - nStrips / 2 + 0.5) * stripW;
                    const xCirc = r * Math.sin(rad);
                    const zCirc = r * (Math.cos(rad) - 1);
                    const curX = xFlat * (1 - p) + xCirc * p;
                    const curZ = zCirc * p;
                    const curAngle = targetAngle * p;
                    strips += `<div class="absolute border-y border-emerald-500/30 bg-emerald-500/20" style="left: calc(50% - ${(stripW + 0.5) / 2}px); top: 0; width: ${stripW + 0.5}px; height: ${h}px; transform-origin: center; transform: translate3d(${curX}px, 0, ${curZ}px) rotateY(${curAngle}deg); transform-style: preserve-3d; opacity: ${0.7 + Math.cos(rad)*0.3}"></div>`;
                }
                html = `
                <div class="relative" style="width: ${s}px; height: ${h}px; transform-style: preserve-3d;">
                    ${strips}
                    <div class="absolute transition-transform duration-500" style="left: calc(50% - ${s/2}px); top: 0; width: ${s}px; height: ${s}px; transform-origin: bottom center; transform: translate3d(0, -100%, 0) rotateX(${90*p}deg); transform-style: preserve-3d;">
                        <div class="w-full h-full bg-emerald-500/30 border border-emerald-400 rounded-full flex items-center justify-center text-[10px] font-bold text-white backdrop-blur-sm">○上</div>
                    </div>
                    <div class="absolute transition-transform duration-500" style="left: calc(50% - ${s/2}px); top: 100%; width: ${s}px; height: ${s}px; transform-origin: top center; transform: translate3d(0, 0, 0) rotateX(${-90*p}deg); transform-style: preserve-3d;">
                        <div class="w-full h-full bg-emerald-500/30 border border-emerald-400 rounded-full flex items-center justify-center text-[10px] font-bold text-white backdrop-blur-sm">○下</div>
                    </div>
                </div>`;
            } else if (shapeId === 'cone') {
                const hc = s * 1.5; const r = s / 2; const l = Math.sqrt(r*r + hc*hc);
                const nStrips = 30; const gamma = Math.asin(r/l) * (180/Math.PI);
                const omega = 360 * (r/l); const stripAngleFlat = omega / nStrips; const stripAngleCone = 360 / nStrips;
                const stripW = 2 * l * Math.tan((stripAngleFlat * Math.PI / 180) / 2);
                const p = fp / 100;
                let strips = '';
                for (let i=0; i<nStrips; i++) {
                    const flatA = (i - nStrips / 2 + 0.5) * stripAngleFlat;
                    const coneA = (i - nStrips / 2 + 0.5) * stripAngleCone;
                    const curRotY = p * (-coneA);
                    const curRotX = p * gamma;
                    const curRotZ = (1 - p) * flatA;
                    let label = i === 15 ? `<div class="absolute w-full bottom-2 flex justify-center text-[10px] font-bold text-white transform scale-75">側面</div>` : '';
                    strips += `<div class="absolute bg-red-500/30 transition-transform duration-500" style="left: calc(50% - ${(stripW + 0.5) / 2}px); top: 10%; width: ${stripW + 0.5}px; height: ${l}px; transform-origin: 50% 0%; transform: rotateY(${curRotY}deg) rotateX(${curRotX}deg) rotateZ(${curRotZ}deg); transform-style: preserve-3d; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); opacity: ${0.7 + Math.cos(coneA * Math.PI / 180)*0.3}">${label}</div>`;
                }
                html = `
                <div class="relative" style="width: ${s}px; height: ${hc + r}px; transform-style: preserve-3d;">
                    ${strips}
                    <div class="absolute transition-transform duration-500" style="left: calc(50% - ${s/2}px); top: 10%; width: ${s}px; height: ${s}px; transform-origin: top center; transform: rotateX(${p*gamma}deg) translateY(${l}px) rotateX(${p*(-90-gamma)}deg); transform-style: preserve-3d;">
                        <div class="w-full h-full bg-red-500/30 border border-red-400 rounded-full flex items-center justify-center text-[10px] font-bold text-white rotate-180 backdrop-blur-sm">○底</div>
                    </div>
                </div>`;
            } else if (shapeId === 'tetra') {
                const h = s * 0.866; const fold = (fp / 100) * 109.5;
                html = `
                <div class="relative flex items-center justify-center" style="width: ${s}px; height: ${h}px; transform-style: preserve-3d; transform: translateY(15px);">
                    <div class="relative" style="width: ${s}px; height: ${h}px; transform-style: preserve-3d;">
                        <div class="absolute inset-0 bg-indigo-500/20 border border-indigo-400 flex justify-center items-start pt-4 font-bold text-[10px] text-white backdrop-blur-sm" style="clip-path: polygon(50% 100%, 0% 0%, 100% 0%);">底△</div>
                        <div class="absolute transition-transform duration-500" style="left: 0; top: -${h}px; width: ${s}px; height: ${h}px; transform-origin: 0% 100%; transform: rotateZ(0deg) rotateX(${-fold}deg); transform-style: preserve-3d;">
                            <div class="w-full h-full bg-indigo-500/30 border-b border-indigo-400 flex justify-center items-end pb-2 font-bold text-[10px] text-white backdrop-blur-sm" style="clip-path: polygon(50% 0%, 0% 100%, 100% 100%);">側1</div>
                        </div>
                        <div class="absolute transition-transform duration-500" style="left: ${s/2}px; top: 0; width: ${s}px; height: ${h}px; transform-origin: 0% 100%; transform: rotateZ(240deg) rotateX(${-fold}deg); transform-style: preserve-3d;">
                            <div class="w-full h-full bg-indigo-500/30 border-b border-indigo-400 flex justify-center items-end pb-2 font-bold text-[10px] text-white backdrop-blur-sm" style="clip-path: polygon(50% 0%, 0% 100%, 100% 100%);">側2</div>
                        </div>
                        <div class="absolute transition-transform duration-500" style="left: ${s}px; top: -${h}px; width: ${s}px; height: ${h}px; transform-origin: 0% 100%; transform: rotateZ(120deg) rotateX(${-fold}deg); transform-style: preserve-3d;">
                            <div class="w-full h-full bg-indigo-500/30 border-b border-indigo-400 flex justify-center items-end pb-2 font-bold text-[10px] text-white backdrop-blur-sm" style="clip-path: polygon(50% 0%, 0% 100%, 100% 100%);">側3</div>
                        </div>
                    </div>
                </div>`;
            } else if (shapeId === 'sqPyramid') {
                const triH = s * 1.12; const cosGamma = (s / 2) / triH; const gamma = Math.acos(cosGamma) * (180 / Math.PI);
                const foldMax = 180 - gamma; const fold = (fp / 100) * foldMax;
                html = `
                <div class="relative flex items-center justify-center" style="width: ${s}px; height: ${s}px; transform-style: preserve-3d;">
                    <div class="relative" style="width: ${s}px; height: ${s}px; transform-style: preserve-3d;">
                        <div class="absolute inset-0 bg-amber-500/20 border border-amber-400 flex items-center justify-center font-bold text-[10px] text-white backdrop-blur-sm">底□</div>
                        <div class="absolute transition-transform duration-500" style="bottom: 100%; left: 0; width: ${s}px; height: ${triH}px; transform-origin: bottom center; transform: rotateX(${-fold}deg); transform-style: preserve-3d;">
                            <div class="w-full h-full bg-amber-500/30 border border-b-0 border-amber-400 flex justify-center items-end pb-2 font-bold text-[10px] text-white backdrop-blur-sm" style="clip-path: polygon(50% 0%, 0% 100%, 100% 100%);">側1</div>
                        </div>
                        <div class="absolute transition-transform duration-500" style="top: 100%; left: 0; width: ${s}px; height: ${triH}px; transform-origin: top center; transform: rotateX(${fold}deg); transform-style: preserve-3d;">
                            <div class="w-full h-full bg-amber-500/30 border border-t-0 border-amber-400 flex justify-center items-start pt-2 font-bold text-[10px] text-white backdrop-blur-sm" style="clip-path: polygon(50% 100%, 0% 0%, 100% 0%);">側2</div>
                        </div>
                        <div class="absolute transition-transform duration-500" style="right: 100%; top: 0; width: ${triH}px; height: ${s}px; transform-origin: right center; transform: rotateY(${fold}deg); transform-style: preserve-3d;">
                            <div class="w-full h-full bg-amber-500/30 border border-r-0 border-amber-400 flex justify-end items-center pr-2 font-bold text-[10px] text-white backdrop-blur-sm" style="clip-path: polygon(0% 50%, 100% 0%, 100% 100%);">側3</div>
                        </div>
                        <div class="absolute transition-transform duration-500" style="left: 100%; top: 0; width: ${triH}px; height: ${s}px; transform-origin: left center; transform: rotateY(${-fold}deg); transform-style: preserve-3d;">
                            <div class="w-full h-full bg-amber-500/30 border border-l-0 border-amber-400 flex justify-start items-center pl-2 font-bold text-[10px] text-white backdrop-blur-sm" style="clip-path: polygon(100% 50%, 0% 0%, 0% 100%);">側4</div>
                        </div>
                    </div>
                </div>`;
            }
            return html;
        }

        function initNetsGallery() {
            if(!isNetsGalleryInit) {
                // Setup drag
                const container = document.getElementById('s2-nets-3d-container');
                const scene = document.getElementById('s2-nets-scene');
                let isDragging = false; let lastX = 0; let lastY = 0;
                let rotX = -15; let rotY = -25;
                
                container.addEventListener('mousedown', e => {
                    isDragging = true; lastX = e.clientX; lastY = e.clientY; container.style.cursor = 'grabbing';
                });
                window.addEventListener('mousemove', e => {
                    if (!isDragging) return;
                    const dx = e.clientX - lastX; const dy = e.clientY - lastY;
                    rotY += dx * 0.5; rotX -= dy * 0.5;
                    lastX = e.clientX; lastY = e.clientY;
                    scene.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
                });
                window.addEventListener('mouseup', () => { isDragging = false; container.style.cursor = 'grab'; });
                
                // Add touch support
                container.addEventListener('touchstart', e => {
                    isDragging = true; lastX = e.touches[0].clientX; lastY = e.touches[0].clientY;
                });
                window.addEventListener('touchmove', e => {
                    if (!isDragging) return;
                    const dx = e.touches[0].clientX - lastX; const dy = e.touches[0].clientY - lastY;
                    rotY += dx * 0.5; rotX -= dy * 0.5;
                    lastX = e.touches[0].clientX; lastY = e.touches[0].clientY;
                    scene.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
                });
                window.addEventListener('touchend', () => { isDragging = false; });
                
                isNetsGalleryInit = true;
            }
            renderNetsUI();
        }

        function renderNetsUI() {
            const tabsContainer = document.getElementById('s2-nets-tabs');
            tabsContainer.innerHTML = '';
            Object.keys(netShapesData).forEach(key => {
                const shape = netShapesData[key];
                const isActive = key === currentNetShape;
                const btn = document.createElement('button');
                btn.className = `flex-1 flex flex-col items-center justify-center gap-1 min-w-[70px] p-2 rounded-lg text-sm font-black transition-all ${isActive ? `${shape.tagColor} text-white shadow-md scale-105 border-none` : 'bg-slate-800 text-slate-400 hover:bg-slate-700 border border-slate-700'}`;
                btn.innerHTML = `<span class="text-xl">${shape.icon}</span><span class="text-[10px] whitespace-nowrap tracking-wide">${shape.name}</span>`;
                btn.onclick = () => {
                    currentNetShape = key;
                    currentFoldPercent = 0;
                    document.getElementById('s2-nets-slider').value = 0;
                    document.getElementById('s2-nets-fp-val').textContent = '0%';
                    renderNetsUI();
                };
                tabsContainer.appendChild(btn);
            });
            
            const shape = netShapesData[currentNetShape];
            document.getElementById('s2-nets-scene').innerHTML = renderNetsHTML(currentNetShape, currentFoldPercent);
            document.getElementById('s2-nets-note').innerHTML = shape.note;
        }

        function updateNetsFold(val) {
            currentFoldPercent = parseInt(val);
            document.getElementById('s2-nets-fp-val').textContent = `${val}%`;
            // Re-render the 3D faces
            document.getElementById('s2-nets-scene').innerHTML = renderNetsHTML(currentNetShape, currentFoldPercent);
        }
"""
insert_idx_script = content.rfind('</script>')
content = content[:insert_idx_script] + js_code + content[insert_idx_script:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
