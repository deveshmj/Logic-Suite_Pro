from flask import Flask, render_template_string

app = Flask(__name__)

# --- THE WEBSITE INTERFACE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logic Suite Pro | Localhost</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; overflow: hidden; }
        .canvas-area { background-image: radial-gradient(#334155 1px, transparent 1px); background-size: 30px 30px; position: relative; width: 100%; height: calc(100vh - 160px); cursor: crosshair; }
        
        /* Components */
        .gate { position: absolute; background: #1e293b; border: 2px solid #38bdf8; border-radius: 8px; padding: 10px; min-width: 100px; text-align: center; cursor: move; user-select: none; z-index: 10; }
        .gate-on { border-color: #22d3ee; box-shadow: 0 0 20px rgba(34, 211, 238, 0.5); background: #0c4a6e; }
        
        .bulb { border-radius: 50%; width: 60px; height: 60px; display: flex; items-center; justify-center; font-weight: bold; border: 3px solid #334155; }
        .bulb-on { background: #22d3ee; border-color: #fff; box-shadow: 0 0 30px #22d3ee; color: #000; }

        /* Ports */
        .port { width: 14px; height: 14px; background: #64748b; border-radius: 50%; position: absolute; z-index: 30; border: 2px solid #0f172a; }
        .port:hover { transform: scale(1.4); background: #22d3ee; }
        .port-in { left: -8px; top: 50%; transform: translateY(-50%); }
        .port-out { right: -8px; top: 50%; transform: translateY(-50%); background: #38bdf8; }
        
        svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5; }
        .toolbar-btn { transition: all 0.2s; font-weight: bold; }
        .toolbar-btn:hover { transform: translateY(-2px); filter: brightness(1.2); }
    </style>
</head>
<body>
    <header class="bg-slate-900 border-b border-slate-700 p-4 flex justify-between items-center shadow-2xl">
        <div>
            <h1 class="text-2xl font-bold text-cyan-400"><i class="fas fa-microchip mr-2"></i>LOGIC SUITE PRO</h1>
            <p class="text-xs text-slate-400">Methodology PS#08 | MJ Devesh, Amitabh J, Mrithula JP</p>
        </div>
        <div class="flex gap-4">
            <button onclick="switchMode('SIM')" id="btn-sim" class="px-6 py-2 rounded-full bg-cyan-600 text-white font-bold shadow-lg">SIMULATOR</button>
            <button onclick="switchMode('PRO')" id="btn-pro" class="px-6 py-2 rounded-full bg-slate-800 text-slate-400 font-bold border border-slate-700">PRO DESIGNER</button>
        </div>
    </header>

    <main id="workspace" class="canvas-area">
        <svg id="connections-svg"></svg>
        <div id="canvas-content"></div>
    </main>

    <footer id="toolbar" class="bg-slate-900 border-t border-slate-700 p-4 fixed bottom-0 w-full hidden">
        <div class="max-w-5xl mx-auto flex justify-around items-center">
            <div class="flex gap-2 bg-slate-800 p-2 rounded-lg">
                <button onclick="addGate('AND')" class="toolbar-btn bg-slate-700 px-4 py-2 rounded text-cyan-400">AND</button>
                <button onclick="addGate('OR')" class="toolbar-btn bg-slate-700 px-4 py-2 rounded text-cyan-400">OR</button>
                <button onclick="addGate('XOR')" class="toolbar-btn bg-slate-700 px-4 py-2 rounded text-cyan-400">XOR</button>
                <button onclick="addGate('NOT')" class="toolbar-btn bg-slate-700 px-4 py-2 rounded text-cyan-400">NOT</button>
            </div>
            <button onclick="addInput()" class="toolbar-btn bg-purple-600 px-6 py-2 rounded text-white">+ INPUT</button>
            <button onclick="addOutput()" class="toolbar-btn bg-amber-500 px-6 py-2 rounded text-black">+ OUTPUT BULB</button>
            <button onclick="clearCanvas()" class="toolbar-btn bg-red-600 px-6 py-2 rounded text-white">CLEAR</button>
        </div>
    </footer>

    <script>
        let mode = 'SIM';
        let wires = [];
        let wireStart = null;

        function switchMode(newMode) {
            mode = newMode;
            document.getElementById('btn-sim').className = mode === 'SIM' ? 'px-6 py-2 rounded-full bg-cyan-600 text-white font-bold shadow-lg' : 'px-6 py-2 rounded-full bg-slate-800 text-slate-400 font-bold border border-slate-700';
            document.getElementById('btn-pro').className = mode === 'PRO' ? 'px-6 py-2 rounded-full bg-purple-600 text-white font-bold shadow-lg' : 'px-6 py-2 rounded-full bg-slate-800 text-slate-400 font-bold border border-slate-700';
            document.getElementById('toolbar').style.display = mode === 'PRO' ? 'block' : 'none';
            clearCanvas();
            if (mode === 'SIM') setupSimulator();
        }

        function addInput(x=100, y=100, label="INPUT") {
            const id = 'node-' + Math.random().toString(36).substr(2, 9);
            const div = document.createElement('div');
            div.className = 'gate w-16 h-16 flex items-center justify-center font-bold text-2xl';
            div.style.left = x + 'px'; div.style.top = y + 'px';
            div.id = id;
            div.dataset.state = "0";
            div.dataset.type = "INPUT";
            div.innerHTML = `0<div class="port port-out" onmousedown="startWire(event, '${id}')"></div><span class="absolute -top-6 text-[10px] text-slate-400 w-20 text-center">${label}</span>`;
            
            div.onclick = (e) => {
                if(e.target.classList.contains('port')) return;
                div.dataset.state = div.dataset.state === "0" ? "1" : "0";
                div.innerHTML = `${div.dataset.state}<div class="port port-out" onmousedown="startWire(event, '${id}')"></div><span class="absolute -top-6 text-[10px] text-slate-400 w-20 text-center">${label}</span>`;
                div.classList.toggle('gate-on', div.dataset.state === "1");
                updateLogic();
            };
            makeDraggable(div);
            document.getElementById('canvas-content').appendChild(div);
            return id;
        }

        function addGate(type, x=400, y=300, label="") {
            const id = 'gate-' + Math.random().toString(36).substr(2, 9);
            const div = document.createElement('div');
            div.className = 'gate';
            div.style.left = x + 'px'; div.style.top = y + 'px';
            div.id = id;
            div.dataset.type = type;
            div.dataset.state = "0";
            
            const inputs = type === 'NOT' ? 1 : 2;
            let ports = `<div class="port port-out" onmousedown="startWire(event, '${id}')"></div>`;
            for(let i=0; i<inputs; i++) {
                const top = inputs === 1 ? '50%' : (i === 0 ? '30%' : '70%');
                ports += `<div class="port port-in" style="top: ${top}" onmouseup="endWire('${id}', ${i})"></div>`;
            }
            div.innerHTML = `<span class="text-cyan-400 font-bold">${type}</span>${ports}<span class="absolute -top-6 text-[10px] text-slate-400 w-full left-0">${label}</span>`;
            makeDraggable(div);
            document.getElementById('canvas-content').appendChild(div);
            return id;
        }

        function addOutput(x=800, y=300, label="OUTPUT") {
            const id = 'out-' + Math.random().toString(36).substr(2, 9);
            const div = document.createElement('div');
            div.className = 'gate bulb w-16 h-16 flex items-center justify-center';
            div.style.left = x + 'px'; div.style.top = y + 'px';
            div.id = id;
            div.dataset.type = "OUTPUT";
            div.dataset.state = "0";
            div.innerHTML = `0<div class="port port-in" onmouseup="endWire('${id}', 0)"></div><span class="absolute -top-6 text-[10px] text-slate-400 w-20 text-center">${label}</span>`;
            makeDraggable(div);
            document.getElementById('canvas-content').appendChild(div);
            return id;
        }

        function setupSimulator() {
            const inA = addInput(150, 200, "INPUT A");
            const inB = addInput(150, 400, "INPUT B");
            const xorGate = addGate('XOR', 450, 200, "SUM LOGIC");
            const andGate = addGate('AND', 450, 400, "CARRY LOGIC");
            const sumOut = addOutput(750, 200, "SUM BIT");
            const cryOut = addOutput(750, 400, "CARRY BIT");

            wires.push({ from: inA, to: xorGate, portIdx: 0 });
            wires.push({ from: inB, to: xorGate, portIdx: 1 });
            wires.push({ from: inA, to: andGate, portIdx: 0 });
            wires.push({ from: inB, to: andGate, portIdx: 1 });
            wires.push({ from: xorGate, to: sumOut, portIdx: 0 });
            wires.push({ from: andGate, to: cryOut, portIdx: 0 });
            updateLogic();
        }

        function startWire(e, id) {
            e.stopPropagation();
            const rect = document.getElementById(id).getBoundingClientRect();
            wireStart = { id, x: rect.right, y: rect.top + rect.height/2 };
            document.onmousemove = (moveE) => {
                drawWires();
                const svg = document.getElementById('connections-svg');
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', wireStart.x); line.setAttribute('y1', wireStart.y);
                line.setAttribute('x2', moveE.pageX); line.setAttribute('y2', moveE.pageY);
                line.setAttribute('stroke', '#22d3ee'); line.setAttribute('stroke-width', '2');
                svg.appendChild(line);
            };
            document.onmouseup = () => { document.onmousemove = null; wireStart = null; drawWires(); };
        }

        function endWire(targetId, portIdx) {
            if(wireStart && wireStart.id !== targetId) {
                wires = wires.filter(w => !(w.to === targetId && w.portIdx === portIdx));
                wires.push({ from: wireStart.id, to: targetId, portIdx: portIdx });
                updateLogic();
            }
        }

        function updateLogic() {
            for(let loop=0; loop<5; loop++) {
                document.querySelectorAll('.gate').forEach(g => {
                    if(g.dataset.type === 'INPUT') return;
                    const inputs = wires.filter(w => w.to === g.id);
                    const v1 = inputs.find(w => w.portIdx === 0) ? (document.getElementById(inputs.find(w => w.portIdx === 0).from).dataset.state === "1") : false;
                    const v2 = inputs.find(w => w.portIdx === 1) ? (document.getElementById(inputs.find(w => w.portIdx === 1).from).dataset.state === "1") : false;
                    
                    let res = false;
                    const t = g.dataset.type;
                    if(t === 'AND') res = v1 && v2;
                    else if(t === 'OR') res = v1 || v2;
                    else if(t === 'XOR') res = v1 !== v2;
                    else if(t === 'NOT') res = !v1;
                    else if(t === 'OUTPUT') res = v1;

                    g.dataset.state = res ? "1" : "0";
                    g.innerHTML = g.innerHTML.replace(/>[01]</, `>${res?1:0}<`);
                    if(res) g.classList.add('gate-on', 'bulb-on'); else g.classList.remove('gate-on', 'bulb-on');
                });
            }
            drawWires();
        }

        function drawWires() {
            const svg = document.getElementById('connections-svg');
            svg.innerHTML = '';
            wires.forEach(w => {
                const f = document.getElementById(w.from), t = document.getElementById(w.to);
                if(!f || !t) return;
                const fR = f.getBoundingClientRect(), tR = t.getBoundingClientRect();
                const x1 = fR.right, y1 = fR.top + fR.height/2, x2 = tR.left;
                const totalIn = t.dataset.type === 'NOT' || t.dataset.type === 'OUTPUT' ? 1 : 2;
                const y2 = tR.top + (totalIn === 1 ? tR.height/2 : (w.portIdx === 0 ? tR.height*0.3 : tR.height*0.7));
                
                const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                const active = f.dataset.state === "1";
                path.setAttribute('d', `M ${x1} ${y1} C ${x1+40} ${y1}, ${x2-40} ${y2}, ${x2} ${y2}`);
                path.setAttribute('stroke', active ? '#22d3ee' : '#334155');
                path.setAttribute('stroke-width', '3'); path.setAttribute('fill', 'none');
                svg.appendChild(path);
            });
        }

        function makeDraggable(el) {
            el.onmousedown = (e) => {
                if(e.target.classList.contains('port')) return;
                let sx = e.clientX - el.offsetLeft, sy = e.clientY - el.offsetTop;
                document.onmousemove = (me) => {
                    el.style.left = me.pageX - sx + 'px';
                    el.style.top = me.pageY - sy + 'px';
                    drawWires();
                };
                document.onmouseup = () => document.onmousemove = null;
            };
        }

        function clearCanvas() {
            document.getElementById('canvas-content').innerHTML = '';
            document.getElementById('connections-svg').innerHTML = '';
            wires = [];
        }

        setupSimulator();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, port=5000)