import json


def build_quiz_html(quiz_items, dataset_key, denktijd_ms=5000, luistertijd_ms=4000):
    """
    Bouwt een HTML/JS-component die:
    - per vraag: vraag-audio afspeelt, wacht (denktijd), antwoord-audio afspeelt
    - dan luistert (Web Speech API) of je 'goed' of 'fout' zegt
    - valt terug op manuele knoppen als spraakherkenning niet lukt/beschikbaar is
    - aan het einde de resultaten als CSV laat downloaden (bestandsnaam bevat dataset_key)

    quiz_items: lijst van dicts met keys 'vraag', 'antwoord', 'vraag_b64', 'antwoord_b64'
    dataset_key: veilige naam (geen spaties) om de resultaten-CSV te herkennen bij het
                 terug uploaden in de app
    """
    data_json = json.dumps(quiz_items)

    html = f"""
    <div id="quiz-app" style="font-family: sans-serif; padding: 10px;">
      <div id="status" style="font-size:18px; margin-bottom:10px;">Klaar om te starten.</div>
      <div id="vraagnummer" style="font-weight:bold; margin-bottom:10px;"></div>
      <button id="startBtn" style="padding:8px 16px; font-size:16px;">Start quiz</button>
      <div id="manualButtons" style="display:none; margin-top:10px;">
        <button id="goedBtn" style="background:#4CAF50;color:white;padding:8px 16px;margin-right:8px;border:none;border-radius:4px;">Goed &#10003;</button>
        <button id="foutBtn" style="background:#f44336;color:white;padding:8px 16px;border:none;border-radius:4px;">Fout &#10007;</button>
      </div>
      <div id="samenvatting" style="margin-top:20px; font-size:16px;"></div>
      <a id="downloadLink" style="display:none; padding:8px 16px; background:#2196F3; color:white; text-decoration:none; border-radius:4px;">Download resultaten (CSV)</a>
    </div>

    <script>
    const quizData = {data_json};
    const datasetKey = "{dataset_key}";
    const denktijdMs = {denktijd_ms};
    const luistertijdMs = {luistertijd_ms};
    let idx = 0;
    let results = [];
    let recognition = null;

    const statusEl = document.getElementById('status');
    const vraagnummerEl = document.getElementById('vraagnummer');
    const startBtn = document.getElementById('startBtn');
    const manualButtons = document.getElementById('manualButtons');
    const goedBtn = document.getElementById('goedBtn');
    const foutBtn = document.getElementById('foutBtn');
    const samenvattingEl = document.getElementById('samenvatting');
    const downloadLink = document.getElementById('downloadLink');

    const SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognitionCtor) {{
        recognition = new SpeechRecognitionCtor();
        recognition.lang = 'nl-BE';
        recognition.continuous = false;
        recognition.interimResults = false;
    }} else {{
        statusEl.innerText = "Spraakherkenning niet ondersteund in deze browser (gebruik Chrome of Edge). Je kan manueel 'Goed'/'Fout' klikken.";
    }}

    function playAudio(b64) {{
        return new Promise((resolve) => {{
            const audio = new Audio("data:audio/mpeg;base64," + b64);
            audio.onended = resolve;
            audio.onerror = resolve;
            audio.play().catch(resolve);
        }});
    }}

    function wachten(ms) {{
        return new Promise((resolve) => setTimeout(resolve, ms));
    }}

    function vraagManueel() {{
        return new Promise((resolve) => {{
            manualButtons.style.display = 'block';
            goedBtn.onclick = () => {{ manualButtons.style.display = 'none'; resolve(true); }};
            foutBtn.onclick = () => {{ manualButtons.style.display = 'none'; resolve(false); }};
        }});
    }}

    function luisterNaarFeedback() {{
        return new Promise((resolve) => {{
            if (!recognition) {{
                resolve(null);
                return;
            }}
            statusEl.innerText = "Luisteren... zeg 'goed' of 'fout'";
            let resolved = false;
            const timeoutId = setTimeout(() => {{
                if (!resolved) {{
                    resolved = true;
                    try {{ recognition.stop(); }} catch (e) {{}}
                    resolve(null);
                }}
            }}, luistertijdMs);

            recognition.onresult = (event) => {{
                if (resolved) return;
                const transcript = event.results[0][0].transcript.toLowerCase();
                let val = null;
                if (transcript.includes('goed') || transcript.includes('juist') || transcript.includes('correct')) {{
                    val = true;
                }} else if (transcript.includes('fout') || transcript.includes('verkeerd')) {{
                    val = false;
                }}
                resolved = true;
                clearTimeout(timeoutId);
                resolve(val);
            }};
            recognition.onerror = () => {{
                if (!resolved) {{
                    resolved = true;
                    clearTimeout(timeoutId);
                    resolve(null);
                }}
            }};
            try {{
                recognition.start();
            }} catch (e) {{
                resolved = true;
                clearTimeout(timeoutId);
                resolve(null);
            }}
        }});
    }}

    async function speelVraagAf(item) {{
        vraagnummerEl.innerText = "Vraag " + (idx + 1) + " / " + quizData.length;
        statusEl.innerText = "Vraag...";
        await playAudio(item.vraag_b64);
        statusEl.innerText = "Bedenktijd...";
        await wachten(denktijdMs);
        statusEl.innerText = "Antwoord...";
        await playAudio(item.antwoord_b64);

        let correct = await luisterNaarFeedback();
        if (correct === null) {{
            statusEl.innerText = "Niet verstaan. Was je antwoord goed of fout?";
            correct = await vraagManueel();
        }}

        results.push({{vraag: item.vraag, correct: correct, timestamp: new Date().toISOString()}});
        idx += 1;
        if (idx < quizData.length) {{
            await speelVraagAf(quizData[idx]);
        }} else {{
            afronden();
        }}
    }}

    function afronden() {{
        const aantalGoed = results.filter(r => r.correct).length;
        statusEl.innerText = "Klaar!";
        vraagnummerEl.innerText = "";
        samenvattingEl.innerText = aantalGoed + " / " + results.length + " goed.";

        let csv = "vraag,correct,timestamp\\n";
        results.forEach(r => {{
            const vraagVeilig = '"' + r.vraag.replace(/"/g, '""') + '"';
            csv += vraagVeilig + "," + r.correct + "," + r.timestamp + "\\n";
        }});
        const blob = new Blob([csv], {{type: 'text/csv'}});
        const url = URL.createObjectURL(blob);
        const nu = new Date().toISOString().replace(/[:.]/g, '-');
        downloadLink.href = url;
        downloadLink.download = datasetKey + "_" + nu + ".csv";
        downloadLink.style.display = 'inline-block';
    }}

    startBtn.onclick = async () => {{
        startBtn.style.display = 'none';
        idx = 0;
        results = [];
        if (quizData.length > 0) {{
            await speelVraagAf(quizData[0]);
        }}
    }};
    </script>
    """
    return html
