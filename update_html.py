import os
import re

directories = ['Laangke', 'Lakonea', 'Malalanda']

html_add = """                    <div class="chart-card chart-full">
                        <h3 class="chart-title">Lapangan Usaha</h3>
                        <div class="chart-container" style="height: 300px;"><canvas id="chartLapanganUsaha"></canvas></div>
                    </div>
                    <div class="chart-card">
                        <h3 class="chart-title">Agama / Kepercayaan</h3>
                        <div class="chart-container"><canvas id="chartAgama"></canvas></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Unduh Data Agregat -->"""

js_vars_old = "let chartPendObj, chartPekObj, chartPenObj, chartPiramidaObj, chartDisabilitasObj;"
js_vars_new = "let chartPendObj, chartPekObj, chartPenObj, chartPiramidaObj, chartDisabilitasObj, chartUsahaObj, chartAgamaObj;"

js_add = """            // Disabilitas & Jaminan Sosial
            if (chartDisabilitasObj) chartDisabilitasObj.destroy();
            const disabYa = dataIndividu.filter(i => String(i.punya_disabilitas || '').trim() !== '' && i.punya_disabilitas !== 'Tidak').length;
            const jamkesYa = dataIndividu.filter(i => String(i.peserta_jaminan_kesehatan || '').toLowerCase() === 'ya').length;
            const jamsosYa = dataIndividu.filter(i => String(i.peserta_jamsostek || '').toLowerCase() === 'ya').length;
            chartDisabilitasObj = new Chart(document.getElementById('chartDisabilitas'), {
                type: 'bar',
                data: {
                    labels: ['Disabilitas', 'Jaminan Kesehatan', 'Jaminan Naker'],
                    datasets: [
                        { label: 'Ya', data: [disabYa, jamkesYa, jamsosYa], backgroundColor: '#5a7d6a' },
                        { label: 'Tidak', data: [dataInd.length - disabYa, dataInd.length - jamkesYa, dataInd.length - jamsosYa], backgroundColor: '#a39080' }
                    ]
                },
                options: { ...JSON.parse(JSON.stringify(opt)), scales: { x: { stacked: true }, y: { stacked: true } } }
            });

            // Lapangan Usaha
            if (chartUsahaObj) chartUsahaObj.destroy();
            const usahas = {}; dataInd.forEach(i => { const v = String(i.lapangan_usaha || 'Belum Terdata').trim(); usahas[v] = (usahas[v] || 0) + 1; });
            chartUsahaObj = new Chart(document.getElementById('chartLapanganUsaha'), {
                type: 'bar', data: { labels: Object.keys(usahas), datasets: [{ label: 'Jumlah Individu', data: Object.values(usahas), backgroundColor: '#5a7d6a' }] }, options: { ...JSON.parse(JSON.stringify(opt)), indexAxis: 'y', plugins: { legend: { display: false } } }
            });

            // Agama
            if (chartAgamaObj) chartAgamaObj.destroy();
            const agamas = {}; dataInd.forEach(i => { const v = String(i.agama_individu || 'Belum Terdata').trim(); agamas[v] = (agamas[v] || 0) + 1; });
            chartAgamaObj = new Chart(document.getElementById('chartAgama'), {
                type: 'pie', data: { labels: Object.keys(agamas), datasets: [{ data: Object.values(agamas), backgroundColor: ['#5a7d6a', '#c49a6c', '#b85c4d', '#a39080', '#8c5a3c', '#d4a27a'], borderWidth: 0 }] }, options: JSON.parse(JSON.stringify(opt))
            });

            lucide.createIcons();
        }"""

for d in directories:
    file_path = os.path.join(d, 'index.html')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace HTML
        content = re.sub(
            r'\s*</div>\s*</div>\s*</section>\s*<!-- Unduh Data Agregat -->',
            '\n' + html_add,
            content, count=1
        )
        
        # Replace JS vars
        content = content.replace(js_vars_old, js_vars_new)
        
        # Replace JS logic
        # We find the end of renderDashboardIndividu block:
        # // Disabilitas & Jaminan Sosial
        # ...
        # lucide.createIcons();
        # }
        content = re.sub(
            r'\s*// Disabilitas & Jaminan Sosial.*?\s*lucide\.createIcons\(\);\s*}',
            '\n' + js_add,
            content, flags=re.DOTALL
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")
