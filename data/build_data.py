import json
R="2026-10-28"
sea_rows_raw = """Qwen 3.5 122B MoE|Alibaba|76.31|-1.72|1.80|64.19|88.70|85.99|86.35|91.94|73.43|43.58
Gemma 4 31B|Google|76.27|-1.70|1.77|65.45|90.72|83.96|85.29|93.09|74.15|41.21
Qwen 3.6 27B|Alibaba|76.26|-1.76|1.72|71.14|89.19|84.00|86.08|92.32|71.78|39.31
SEA-LION v4.5 (Qwen) 27B|AISG|75.23|-1.73|1.67|67.57|88.32|83.31|82.12|92.44|72.29|40.57
Muse Glimmer 30B|Meta|74.14|-1.83|1.79|53.14|88.57|82.38|85.45|91.68|72.50|45.25
SEA-LION v4.8 (Nemotron) 120B MoE|AISG|73.25|-1.71|1.74|59.32|81.75|81.83|84.33|88.67|70.74|46.14
GPT OSS 120B MoE (mxfp4)|OpenAI|69.68|-1.82|1.98|54.19|80.29|74.95|83.22|90.96|69.77|34.39
Mistral Medium 3.5 128B|Mistral AI|68.93|-1.70|1.66|33.04|80.25|79.98|82.84|91.94|71.48|42.96
Nemotron 3 Super 120B MoE|NVIDIA|68.66|-1.71|1.80|54.88|74.55|80.14|81.37|86.21|68.72|34.73
Apertus 1.5 70B|Swiss AI|65.54|-1.90|1.72|50.35|81.21|60.77|69.47|91.32|64.72|40.91
GLM 4.7 Flash 30B MoE|Z.ai|65.50|-1.76|1.79|48.26|75.75|70.57|72.34|88.91|66.36|36.30
SEA-LION v4.5 (Gemma E2B) 5B MoE|AISG|62.28|-1.83|1.81|45.42|82.06|53.28|75.93|90.30|64.40|24.58
SEA-LION v4.8 (Nemotron) 30B MoE|AISG|62.09|-1.70|1.63|41.47|71.33|76.10|83.37|85.86|55.17|21.35
Gemma 4 (E2B) 5B|Google|61.46|-1.88|1.80|40.89|80.30|53.33|76.10|90.00|64.23|25.37
Nemotron 3.5 Lightning 30B MoE|NVIDIA|58.76|-1.68|1.75|30.77|59.30|71.22|82.80|81.16|57.31|28.78
Olmo 3.1 32B|AI2|58.14|-2.02|2.01|51.19|70.87|39.05|71.11|86.14|56.10|32.55
MERaLiON 2 10B|A*STAR|55.29|-1.90|1.95|26.16|62.90|50.06|54.75|86.16|64.74|42.24
Tiny Aya Water 3B|Cohere Labs|32.71|-1.47|1.54|1.49|63.94|31.66|29.21|59.17|25.67|17.83"""
sea=[]
for l in sea_rows_raw.split("\n"):
    p=l.split("|")
    sea.append(dict(model=p[0],org=p[1],ms=float(p[2]),ci=f"{p[3]} / +{p[4]}".replace("--","-"),
      cultural=float(p[5]),instruct=float(p[6]),knowledge=float(p[7]),chat=float(p[8]),nlg=float(p[9]),nlu=float(p[10]),safety=float(p[11])))
for r in sea: r["ci"]="±%.2f"%((abs(float(r["ci"].split(" / ")[0]))+float(r["ci"].split("+")[1]))/2)

pend=[("Gemini 3.1 Pro","Google",91.5,91,96,89,93,89),("GPT-5.5","OpenAI",89.3,89,93,85,90,89),("Claude Opus 4.8","Anthropic",88.7,86,90,86,92,89),("Kimi K3 (via Ollama Cloud)","Moonshot",87.5,89,91,84,90,83),("Qwen 3.7 Max","Alibaba",86.6,83,92,86,91,81),("DeepSeek V4 Pro 0813 (via Ollama Cloud)","DeepSeek",85.5,86,89,82,87,84),("Qwen 3.5 397B (via Ollama Cloud)","Alibaba",85.4,85,90,81,87,84),("ILMU GLM-5.1","YTL AI Labs",84.0,85,86,80,85,84),("DeepSeek V4 Pro","DeepSeek",83.8,85,89,80,84,81),("ILMU v3.1","YTL AI Labs",83.1,84,87,80,84,81),("MiniMax M3 (via Ollama Cloud)","MiniMax",82.8,85,85,79,87,78),("Grok 4.3","xAI",82.3,81,84,80,83,83),("GLM-5.2","Z.ai",81.8,83,86,84,81,75),("Mistral Large 3 (via Ollama Cloud)","Mistral",81.5,82,86,79,82,77),("Kimi K2.6","Moonshot",80.7,85,86,75,81,76),("Mistral Large 2512","Mistral",80.4,79,83,80,82,77),("MiniMax M3","MiniMax",79.6,82,84,77,79,76),("Llama 4 Maverick","Meta",78.1,84,79,76,78,74),("ILMU Vision v1.3","YTL AI Labs",74.9,79,75,73,74,74),("ILMU Mini v3.3","YTL AI Labs",71.8,74,72,72,71,70),("GLM-5.3 (via Ollama Cloud)","Z.ai",71.6,65,74,70,76,74)]
pen=[dict(model=a,org=b,acc=c,stem=d,bahasa=e,social=f,human=g,other=h) for a,b,c,d,e,f,g,h in pend]

ilmu=[("ILMU (ILMU v1 — model evaluated in the report)","YTL AI Labs",87.20,True),("GPT-4o","OpenAI",84.97,False),("DeepSeek-V3","DeepSeek",80.56,False),("GPT-5","OpenAI",79.53,False),("Sahabat-AI-v2-70B","GoTo / Indosat",78.31,False),("Llama-3.1-70B","Meta",78.07,False),("SEA-LION v3-70B","AISG",78.03,False),("Mallam 2.5 Small","Mesolitica",71.35,False),("Merdeka-LLM (HR 3B)","Agmo",57.28,False),("Falcon3-10B","—",56.38,False)]
ilm=[dict(model=a,org=b,acc=c,vendor=d) for a,b,c,d in ilmu]
# fix: org attributions for Sahabat-AI not in source; use blank
for r in ilm:
    if r["model"].startswith("Sahabat"): r["org"]="—"
    if r["model"].startswith("ILMU"): r["model"]="ILMU"
    if r["model"].startswith("Mallam"): r["note"]="Tech report Table 2 shows 71.35; system card subject table shows 71.53."

asr=[("Aisyah 1.0 Pro","Revolab",4.89,6.58,5.79,0.62,True),("Scribe v2","ElevenLabs",4.79,8.29,6.67,0.70,False),("Gemini 2.5 Pro","Google",5.30,8.49,7.00,1.00,False),("Qwen-Audio 3.0 ASR Flash","Alibaba",7.22,10.87,9.17,1.11,False),("Ilmu ASR v4.2","YTL AI Labs",7.78,10.97,9.48,0.87,False),("Aisyah 1.0 Flash","Revolab",7.98,11.81,10.03,0.72,True),("Gemini 2.5 Flash","Google",9.05,12.25,10.76,2.48,False),("Whisper large-v3","OpenAI",15.62,18.76,17.30,2.73,False),("Qwen3-ASR-1.7B (official)","Alibaba",15.26,21.20,18.43,1.09,False),("Universal 2","AssemblyAI",14.86,22.25,18.80,0.70,False),("Universal 3.5 Pro","AssemblyAI",14.88,22.23,18.80,0.71,False),("Qwen3-ASR-0.6B (official)","Alibaba",20.73,27.21,24.19,1.25,False),("Gemini 3.6 Flash","Google",15.01,32.87,24.55,14.35,False),("Nova 3","Deepgram",25.63,37.55,31.99,0.94,False)]
asrr=[dict(model=a,org=b,pub=c,priv=d,comb=e,ins=f,vendor=g) for a,b,c,d,e,f,g in asr]

data={
 "site":{"name":"Malay AI Scoreboard","status":"DRAFT – not launched","retrieved":R,
  "disclaimer":"We do not compute our own scores yet. Every number below belongs to the source named next to it. We never merge scores from different sources into one ranking."},
 "tabs":[
 {"id":"chat","label":"Chat (LLMs)","intro":"How well do chat models handle Bahasa Malaysia? Three sources, three different tests (one of them is the vendor’s own claim). Pick one below.",
  "boards":[
   {"id":"seahelm","title":"SEA-HELM — Malay competency score","owner":"AI Singapore (SEA-HELM leaderboard)","owner_type":"Third-party academic/public benchmark","date":"2026-09-18","retrieved":R,
    "url":"https://leaderboard.sea-lion.ai/detailed/MS","metric":"MS = Malay competency average (0–100, higher is better); ± is half the 95% bootstrap CI shown by the source.",
    "caveat":"Only open-weight models of ≤200B parameters are on this leaderboard (no GPT, Claude or Gemini API models). SEA-LION is made by AI Singapore, which also runs the leaderboard.",
    "columns":[["model","Model"],["org","Maker"],["ms","MS (Malay)"],["ci","±95% CI"],["knowledge","Knowledge"],["instruct","Inst. following"],["chat","Multi-turn chat"],["nlu","NLU"],["nlg","NLG"],["cultural","Cultural"],["safety","Safety"]],
    "primary":"ms","rows":sea},
   {"id":"malaymmlu-third","title":"MalayMMLU — independent 1,100-question run (pendakwah.tech)","owner":"pendakwah.tech (independent site; we have not verified who runs it)","owner_type":"Third-party","date":"2026-09 (page notes models added 2026-09-02; exact last-update date not shown)","retrieved":R,
    "url":"https://pendakwah.tech/bahasa/mmlu/","metric":"Accuracy % on a fixed stratified sample of 1,100 MalayMMLU questions (220 per category), 0-shot, temperature 0, generate-and-parse method.",
    "caveat":"Different method from ILMU's claim (first-token logprob), so absolute numbers can differ by several points. Models reached via OpenRouter / Ollama Cloud / ILMU API. Random guessing is ~25%. Small sample = wide error bars (not published by the source).",
    "columns":[["model","Model"],["org","Maker"],["acc","Accuracy %"],["stem","STEM"],["bahasa","Language"],["social","Social sci."],["human","Humanities"],["other","Others"]],
    "primary":"acc","rows":pen},
   {"id":"ilmu-claim","title":"MalayMMLU — ILMU's own claim (vendor-reported)","owner":"YTL AI Labs / ILMU (the vendor being ranked)","owner_type":"VENDOR CLAIM — not independently verified by us","date":"ILMU technical report & system card (publication date not shown on pages retrieved)","retrieved":R,
    "url":"https://www.ilmu.ai/assets/ilmu-technical-report.pdf","url2":"https://www.ilmu.ai/assets/ilmu-system-card.pdf","metric":"MalayMMLU macro-average accuracy %, zero-shot, first-token accuracy, 24,213 questions.",
    "caveat":"Self-reported by the model's maker, and the compared models are older (e.g. GPT-4o). The MalayMMLU benchmark itself comes from UM × YTL AI Labs, which also makes ILMU. Independent commentators have questioned whether first-token scoring favours some models; we list only what ILMU published.",
    "columns":[["model","Model"],["org","Maker"],["acc","MalayMMLU %"]],"primary":"acc","rows":ilm}
  ],
  "prices":{"title":"Published API prices in RM (ILMU only, so far)","source":"ILMU API docs","url":"https://docs.ilmu.ai/docs/models/pricing","retrieved":R,
   "columns":[["model","Model"],["input","Input / 1M tokens"],["output","Output / 1M tokens"]],
   "rows":[{"model":"ilmu-v3.1","input":"RM 4.00","output":"RM 16.00"},{"model":"ilmu-mini-v3.3","input":"RM 0.20","output":"RM 1.20"},{"model":"ilmu-vision-v1.3","input":"RM 1.60","output":"RM 4.80"}],
   "note":"RM prices for the other vendors are coming soon (we will convert from official USD price pages and show the exchange rate and date used)."}},
 {"id":"stt","label":"Speech-to-text","intro":"Word error rate (WER, lower is better) on Malaysian speech including Manglish-style code-switching.",
  "boards":[
   {"id":"revolab","title":"Revolab Malaysian ASR Leaderboard","owner":"Revolab","owner_type":"VENDOR-RUN — Revolab ranks its own Aisyah models alongside others (marked)","date":"2026-08-12","retrieved":R,
    "url":"https://www.revolab.ai/blogs/malaysian-asr-leaderboard/","metric":"WER % on the Revolab ASR Benchmark: 820 public + 1,079 private samples = 1,899 total across 12 Malaysian speech domains. 'Ins' = insertion rate (hallucinated words). Ranked here by combined WER, as the source does.",
    "caveat":"Run by a vendor with models on the board. Revolab says its data is public on HuggingFace and code is on GitHub so results can be audited; we have not yet reproduced them.",
    "columns":[["model","Model"],["org","Maker"],["pub","Public WER %"],["priv","Private WER %"],["comb","Combined WER %"],["ins","Insertion %"]],
    "primary":"comb","asc":True,"rows":asrr}
  ],
  "prices":{"title":"Published API prices in RM (ILMU only, so far)","source":"ILMU API docs","url":"https://docs.ilmu.ai/docs/models/pricing","retrieved":R,
   "columns":[["model","Model"],["price","Price"],["derived","Per hour of audio (our arithmetic)"]],
   "rows":[{"model":"ilmu-asr-v4.2","price":"RM 0.0002 / second","derived":"≈ RM 0.72"}],
   "note":"RM prices for other vendors are coming soon."}},
 {"id":"tts","label":"Text-to-speech","intro":"No Malay-specific TTS ranking we can verify yet.",
  "boards":[],
  "coming_soon":{"headline":"Coming soon — being benchmarked","body":"We found no public Bahasa Malaysia TTS ranking we can trust and verify. Voice Arena publishes a 'Bahasa' TTS leaderboard (blind native-speaker voting), but it does not clearly state whether that is Malaysian Malay or Indonesian, so we are not copying its numbers here until we confirm. Our own blind listening test (native Malaysian raters, formal BM + casual Manglish sentences) is planned — see the methodology page.",
   "links":[["Voice Arena TTS leaderboard (language: Bahasa)","https://voicearena.com/tts-leaderboard/"],["Voice Arena methodology","https://voicearena.com/tts-methodology"]]},
  "prices":{"title":"Published API prices in RM (ILMU only, so far)","source":"ILMU API docs","url":"https://docs.ilmu.ai/docs/models/pricing","retrieved":R,
   "columns":[["model","Model"],["price","Price"]],
   "rows":[{"model":"ilmu-tts-v2 / ilmu-tts-v2.1","price":"RM 0.08 per 1,000 characters"}],
   "note":"Prices only. No quality score for ILMU TTS is shown because we have none from a source yet."}}
 ]}
two=lambda cols:{c[0]:2 for c in cols if c[0] not in("model","org","ci")}
for t in data["tabs"]:
    for bd in t["boards"]:
        bd["dec"]={"acc":1} if bd["id"]=="malaymmlu-third" else two(bd["columns"])
json.dump(data,open("data/data.json","w"),ensure_ascii=False,indent=1)
print(len(sea),len(pen),len(asrr))
