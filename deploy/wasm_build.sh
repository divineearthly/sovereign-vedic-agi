#!/bin/bash
# Build Vedic AGI for browser

echo "Building Vedic AGI for WebAssembly..."

# Create web wrapper
cat > web/index.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
    <title>Vedic AGI — Browser Demo</title>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
</head>
<body>
    <h1>🕉️ Vedic AGI — Sovereign Intelligence</h1>
    <div id="output">Loading...</div>
    <script>
        async function main() {
            let pyodide = await loadPyodide();
            await pyodide.loadPackage("numpy");
            
            // Load Vedic AGI
            await pyodide.runPythonAsync(`
                import micropip
                await micropip.install('vedic-agi')
                from vedic_agi.core import sphota_attention
                print("✅ Vedic AGI loaded in browser!")
            `);
            document.getElementById("output").innerHTML = "✅ Ready";
        }
        main();
    </script>
</body>
</html>
HTML
echo "✅ Web demo created at web/index.html"
